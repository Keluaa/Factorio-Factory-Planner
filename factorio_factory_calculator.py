
from __future__ import annotations

from typing import *

import openpyxl as xl
from openpyxl.worksheet.table import Table

from rational_approximation import approx

wb = xl.load_workbook(r"Factorio - Factory Calculator.xlsm", keep_vba=True)


class Machine:
    machines: List[Machine] = []

    @staticmethod
    def from_str(machine_str: str) -> Machine:
        for machine in Machine.machines:
            if machine.name == machine_str:
                return machine
        else:
            raise ValueError("Unknown machine: '{}'".format(machine_str))

    @staticmethod
    def update_counts():
        for machine in Machine.machines:
            machine.count = 0

        for used_recipe in Recipe.used_recipes:
            used_recipe.machine.count += used_recipe.usage

    @staticmethod
    def get_pollution_production() -> float:
        pollution = 0
        for machine in Machine.machines:
            pollution += machine._get_pollution_production()
        return pollution

    @staticmethod
    def get_energy_consumption() -> float:
        energy = 0
        for machine in Machine.machines:
            energy += machine._get_energy_consumption()
        return energy

    def __init__(self, name: str, speed: float, pollution: float, energy: float):
        self.name = name
        self.speed = speed
        self.pollution = pollution
        self.energy = energy
        self.count = 0

        Machine.machines.append(self)

    def _get_pollution_production(self):
        # to do after update_count
        return self.count * self.pollution

    def _get_energy_consumption(self):
        # to do after update_count
        return self.count * self.energy


class Item:
    items: List[Item] = []
    needs: List[Tuple[Item, float]] = []
    categories: List[str] = []

    produced: Dict[Item, Dict[str, Union[float, bool]]] = {}
    byproducts: Dict[Item, float] = {}

    @staticmethod
    def items_names() -> Generator[str, None, None]:
        for item in Item.items:
            yield item.name

    @staticmethod
    def from_str(item_str) -> Item:
        for item in Item.items:
            if item.name == item_str:
                return item
        else:
            raise ValueError("Unknown item: '{}'".format(item_str))

    @staticmethod
    def print_items_list():
        print("Produced Items:")
        for item, productivity in Item.produced.items():
            print("\t'{}': \t\t{} - \t used: {}".format(item.name, productivity["rate"], productivity["used"]))

        print("Byproducts:")
        for item, productivity in Item.byproducts.items():
            print("\t'{}': \t\t{}".format(item.name, productivity))

    @staticmethod
    def get_category(category: str) -> List[Item]:
        for item in Item.items:
            if item.category == category:
                yield item.name

    def __init__(self, name: str, category: str):
        self.recipes: List[Recipe] = []
        self.name = name
        self.category = category

        Item.items.append(self)

    def __str__(self):
        return "Item '{}' with {} recipes".format(self.name, len(self.recipes))

    def add_to_produced_items(self, rate: float, used: bool):
        if self in Item.produced:
            Item.produced[self]["rate"] += rate
            Item.produced[self]["used"] |= used
        else:
            Item.produced[self] = {"rate": rate, "used": used}

    def add_to_byproducts(self, rate: float):
        if self in Item.byproducts:
            Item.byproducts[self] += rate
        else:
            Item.byproducts[self] = rate


class Recipe:
    recipes: List[Recipe] = []
    used_recipes: List[Recipe] = []

    @staticmethod
    def create_ingredients_lists():
        for recipe in Recipe.recipes:
            recipe._create_ingredients_recipes_list()

    @staticmethod
    def choose_recipe(item: Item) -> Union[Recipe, None]:
        possible_recipes = len(item.recipes)
        if possible_recipes == 0:
            return None  # base item, no recipes needed
        elif possible_recipes == 1:
            return item.recipes[0]
        else:
            # TODO, choose between all possible recipes the best one
            # raise NotImplementedError("multiple recipes for one item: '{}'".format(item.name))
            if item.recipes[0].name.startswith("Empty"):
                return item.recipes[1]
            return item.recipes[0]

    @staticmethod
    def find_special_recipes():
        """
        Find all recipes cycles and branches
        """
        for item in Item.items:
            if len(item.recipes) > 1:
                pass  # TODO : make branched recipe

            marked_recipes = []
            recipes_to_parse = item.recipes
            while len(recipes_to_parse) > 0:
                recipe = recipes_to_parse.pop()
                if recipe not in marked_recipes:
                    marked_recipes.append(recipe)
                else:
                    pass  # TODO : CYCLE DETECTED

                for ingredient in recipe.ingredients:
                    for recipe in ingredient.recipes:
                        recipes_to_parse.append(recipe)

    @staticmethod
    def produce_item(item: Item, rate: float, recipe: Recipe = None) -> Dict[str, Any]:
        result = {"item": item.name, "recipe": None}
        if item in Item.byproducts:
            if Item.byproducts[item] <= rate:
                rate -= Item.byproducts[item]
                result["from_byproducts"] = Item.byproducts[item]
                Item.byproducts[item] = 0
            else:
                Item.byproducts[item] -= rate
                result["from_byproducts"] = rate
                rate = 0
        if rate > 0:
            if recipe is None:
                recipe = Recipe.choose_recipe(item)
            if recipe is not None:
                result["recipe"] = recipe.name
                result["rate"] = rate
                result["count"] = rate * recipe.time / recipe.machine.speed
                result["ingredients"] = recipe.produce(item, rate)
        return result

    @staticmethod
    def print_result():
        print("Used Recipes:")
        for recipe in Recipe.used_recipes:
            print("\t" + str(recipe).replace("\n", "\n\t"))

    def __init__(self, name: str, products: List[str], products_count: List[float],
                 ingredients: List[str], ingredients_count: List[float],
                 time: float, machine: str):
        self.name = name
        self.products: List[Item] = [Item.from_str(product) for product in products]
        self.products_count: List[float] = products_count
        self.ingredients: List[Item] = [Item.from_str(ingredient) for ingredient in ingredients]
        self.ingredients_count: List[float] = ingredients_count
        self.ingredients_recipes: List[Union[Recipe, None]] = []
        self.time = time
        self.machine: Machine = Machine.from_str(machine)
        self.used = False
        self.usage = 0.0

        Recipe.recipes.append(self)

        for product in self.products:
            product.recipes.append(self)

    def __str__(self):
        ingredients_names = [ingredient.name for ingredient in self.ingredients]
        products_names = [product.name for product in self.products]
        return "Recipe '{}': \n\tingredients: {}\n\tproducts: {}\n\tusage: {}" \
            .format(self.name, ", ".join(ingredients_names), ", ".join(products_names), self.usage)

    def _create_ingredients_recipes_list(self):
        for ingredient in self.ingredients:
            self.ingredients_recipes.append(Recipe.choose_recipe(ingredient))

    def get_product_yield(self, product: Item) -> float:
        return self.products_count[self.products.index(product)]

    def get_ingredient_need(self, ingredient: Item) -> float:
        return self.ingredients_count[self.ingredients.index(ingredient)]

    def produce(self, product: Item, product_rate: float) -> List[Dict[str, Any]]:
        if not self.used:
            self.used = True
            Recipe.used_recipes.append(self)

        recipe_added_rate = product_rate / self.get_product_yield(product)  # recipes / sec
        recipe_count = recipe_added_rate * self.time / self.machine.speed  # number of recipes used
        self.usage += recipe_count

        ingredients_results = []

        for i, (ingredient, ingredient_recipe, ingredient_count) in \
                enumerate(zip(self.ingredients, self.ingredients_recipes, self.ingredients_count)):
            if ingredient_recipe is not None:
                ingredients_results.append(
                    Recipe.produce_item(ingredient, ingredient_count * recipe_added_rate, ingredient_recipe))
                ingredient.add_to_produced_items(0, True)
            else:
                ingredients_results.append(Recipe.produce_item(ingredient, ingredient_count * recipe_added_rate))

        for recipe_product, product_count in zip(self.products, self.products_count):
            recipe_product.add_to_produced_items(recipe_added_rate * product_count, recipe_product == product)
            if recipe_product in self.ingredients:
                # add only the excess to the byproducts
                consumed_count = self.get_ingredient_need(recipe_product)
                if consumed_count > product_count:
                    recipe_product.add_to_byproducts(recipe_added_rate * (product_count - consumed_count))
            else:
                recipe_product.add_to_byproducts(recipe_added_rate * product_count)

        return ingredients_results


class RecipeCycle(Recipe):
    pass


class BranchingRecipe(Recipe):
    """
    TODO : faire le résultat de produce juste un lien du type 'branch n°2' et avoir un dossier réservé aux branches dans
     le résultat de la factory. On calcule alors les branches à la fin lorsque toutes les ingrédients et leurs quantités
     ont été déterminés.
    """

    def __init__(self, branches: List[Recipe]):
        super().__init__("", [], [], [], [], 0, "")  # empty init
        self.branches = branches

        # unlink all branches and replace them by the branched recipe
        for branch in self.branches:
            Recipe.recipes.remove(branch)
            for product in branch.products:
                product.recipes.remove(branch)
                if self not in product.recipes:
                    product.recipes.append(self)

        Recipe.recipes.append(self)

    def __str__(self):
        return "Branched Recipe: \n\t" + "\n\t".join([str(recipe).replace("\n", "\n\t") for recipe in self.branches])

    # def


"""
Recipes loops:
Uranium -> Enriched Uranium + Uranium
Enriched Uranium -> Fuel Cell -> Depleted Fuel Cell -> Uranium -> Enriched Uranium  

Multiple Ways To get to product:
Heavy Oil + Light Oil + Petroleum Gas -> Light Oil -> Petroleum Gas (3 * 2 recipes branches possible)
"""


def get_table_from_name(sheet: Any, table_name: str) -> Table:
    # noinspection PyProtectedMember
    for tbl in wb[sheet]._tables:
        if tbl.displayName == table_name:
            return tbl
    raise KeyError("No Table named '{}' in the sheet '{}'".format(table_name, sheet))


def iter_table(sheet: Any, table_name: str, ignore_headers=True,
               skip_empty_row=True) -> Generator[Tuple[int, Any], None, None]:
    for i, row in enumerate(wb[sheet][get_table_from_name(sheet, table_name).ref]):
        if ignore_headers and i == 0:
            continue  # skip columns labels
        if skip_empty_row and row[0].value is None:
            continue  # skip empty rows, but don't stop the loop to keep the table input user friendly
        yield i, row


def load_needs():
    for i, row in iter_table("Input", "Needs"):
        Item.needs.append((Item.from_str(row[0].value), row[1].value / row[2].value))


def load_items():
    headers = []
    for i, row in iter_table("Data", "Item_List", ignore_headers=False, skip_empty_row=False):
        if i == 0:
            headers = [cell.value for cell in row]
            Item.categories = headers
        else:
            for j, cell in enumerate(row):
                if cell.value is not None:
                    Item(cell.value, headers[j])


def load_machines_table():
    for i, row in iter_table("Data", "Machines"):
        Machine(row[0].value, row[1].value, row[2].value, row[3].value)


def load_recipes():
    for i, row in iter_table("Recipes", "Recipes"):
        ingredients = []
        ingredients_count = []
        for j in range(3, 15, 2):
            if row[j].value is None or row[j].value <= 0:
                break
            ingredients_count.append(row[j].value)
            ingredients.append(row[j + 1].value)

        products = []
        products_count = []
        for j in range(15, 21, 2):
            if row[j].value is None or row[j].value <= 0:
                break
            products_count.append(row[j].value)
            products.append(row[j + 1].value)

        Recipe(row[0].value, products, products_count, ingredients, ingredients_count, row[1].value, row[2].value)


def compute_factory():
    recipes_structure = []
    for item, rate in Item.needs:
        recipes_structure.append(Recipe.produce_item(item, rate))
    Machine.update_counts()

    return recipes_structure


def reset_factory():
    for recipe in Recipe.recipes:
        recipe.usage = 0
        recipe.used = False

    Recipe.used_recipes.clear()

    Item.needs.clear()
    Item.produced.clear()
    Item.byproducts.clear()


"""
def write_recipes_list():
    used_recipes_table = get_table_from_name("Input", "Used_Recipes_List")

    first_cell: Cell = wb["Input"]["G2"]
    # clear the table
    for i, row in iter_table("Input", "Used_Recipes_List", skip_empty_row=False):
        if i == 1:
            first_cell = row[0]  # the table may have changed

        for cell in row:
            cell.value = None

    # fill the table
    i = 0
    for i, (recipe, count) in enumerate(used_recipes.items()):
        first_cell.offset(i, 0).value = recipe
        first_cell.offset(i, 1).value = count

    # update the size of the table
    used_recipes_table.ref = first_cell.offset(-1, 0).coordinate + ":" + first_cell.offset(i, 1).coordinate


def write_recipes_layers():
    table_style = None
    first_table_range = ""
    to_remove = []
    # noinspection PyProtectedMember
    for i, tbl in enumerate(wb["Input"]._tables):
        if "Used_Recipes_Layers" in tbl.displayName:
            if tbl.displayName == "Used_Recipes_Layers_1":
                # keep the style and the first cell of the first table
                first_table_range = tbl.ref
                table_style = tbl.tableStyleInfo

            # clear all tables
            for row in wb["Input"][tbl.ref]:
                for cell in row:
                    cell.value = None

            # remove all the tables
            to_remove.append(i)

    for index in sorted(to_remove)[::-1]:
        # noinspection PyProtectedMember
        del wb["Input"]._tables[index]

    if table_style is None:
        raise KeyError("No tables of the sheet '{}' are named '{}'".format("Input", "Used_Recipes_Layers_1"))

    first_cell: Cell = wb["Input"][first_table_range][0][0]  # first row, first cell

    j = 0
    previous_length = 0
    for i, layer in enumerate(layered_used_recipes):
        first_cell = first_cell.offset(previous_length, 0)  # size of the previous table
        first_cell.value = "Layer " + str(i + 1)
        first_cell.offset(0, 1).value = "Count"

        # fill the table
        for j, (recipe, count) in enumerate(layer.items()):
            first_cell.offset(j + 1, 0).value = recipe
            first_cell.offset(j + 1, 1).value = count

        # create the table object
        ref = first_cell.coordinate + ":" + first_cell.offset(1 + len(layer), 1).coordinate  # new size of the table
        table = Table(displayName="Used_Recipes_Layers_" + str(i + 1), ref=ref)
        table.tableStyleInfo = table_style  # keep the style of the first table
        wb["Input"].add_table(table)

        # update the size of the table
        table.ref = first_cell.coordinate + ":" + first_cell.offset(j + 1, 1).coordinate

        previous_length = len(layer) + 1 + 1  # account for the columns headers and the spacing between the tables

    # add a named range to better get all of the layers tables
    last_cell = first_cell.offset(j + 1, 1)
    layers_range = "Input!" + "$" + first_cell.column_letter + "$" + "1" \
                      + ":" + "$" + last_cell.column_letter  + "$" + str(last_cell.row)

    wb.defined_names.append(DefinedName(name="Used_Recipes_Layers", attr_text=layers_range))
"""


def print_factory():
    used_recipes_str = "Used Recipes: \n"
    for used_recipe in Recipe.used_recipes:
        rounded_usage = round(used_recipe.usage, 4)
        n, d, _ = approx(rounded_usage)
        used_recipes_str += "{:>40} - {} / {} ({})\n" \
            .format(used_recipe.name, n, d, rounded_usage)

    produced_items_str = "Produced Items: \n"
    for produced_item, productivity in Item.produced.items():
        produced_items_str += "{:>40} - {:^5} - used: {}\n" \
            .format(produced_item.name, productivity["rate"], productivity["used"])

    byproducts_str = "Byproducts: \n"
    for byproduct, rate in Item.byproducts.items():
        byproducts_str += "{:>40} - {}\n".format(byproduct.name, rate)

    print(used_recipes_str)
    print(produced_items_str)
    print(byproducts_str)

    print("Pollution / min:", Machine.get_pollution_production())
    print("Energy consumption (kW):", Machine.get_energy_consumption())


def run():
    load_items()
    load_needs()
    load_machines_table()
    load_recipes()

    Recipe.create_ingredients_lists()

    for reice in Item.from_str("Petroleum Gas").recipes:
        print(reice)

    print(Recipe.produce_item(Item.from_str("Petroleum Gas"), 12))

    # compute_factory()

    # print_factory()

    # write_recipes_list()
    # write_recipes_layers()

    # wb.save(r"C:\Users\7\Desktop\Factorio - Factory Calculator_lol.xlsm")


if __name__ == "__main__":
    run()
