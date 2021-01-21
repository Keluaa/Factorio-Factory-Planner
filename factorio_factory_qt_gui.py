
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTreeWidgetItem, QHeaderView
from PyQt5.QtCore import QRegExp, pyqtSlot, Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QRegExpValidator, QKeyEvent
from gui_factorio_planner import Ui_MainWindow


from factorio_factory_calculator import *


app = QApplication([])


class SearchFilter(QObject):

    new_search_signal = pyqtSignal(str)
    clear_list_signal = pyqtSignal()
    insert_item_to_list_signal = pyqtSignal(int, str)

    def __init__(self, items: Iterable[str]):
        super().__init__()
        self.key_words = []
        self.stop_search = False
        self.new_search_signal.connect(self.new_search)
        self.items = [(item, tuple(item.lower().strip().split())) for item in items]

    def __del__(self):
        self.stop_search = True
        self.thread().wait(5)

    @pyqtSlot(str)
    def new_search(self, string: str):
        self.key_words = [word for word in string.lower().strip().split() if len(word) > 0]
        self.search()

    @pyqtSlot()
    def search(self):
        self.clear_list_signal.emit()
        score_position = {}
        key_words = self.key_words
        for key in key_words:
            for item_name, item_words in self.items:
                for i, item_word in enumerate(item_words):
                    if not item_word.startswith(key):
                        continue

                    if i in score_position:
                        p = score_position[i]
                        for score, position in score_position.items():
                            if position >= p:
                                score_position[score] += 1
                    else:
                        p = 0
                        for score, position in score_position.items():
                            if score < i and position > p:
                                p = position
                            score_position[score] += 1
                        score_position[i] = p + 1

                    self.insert_item_to_list_signal.emit(p, item_name)
                    break


class FactoryGUI(QMainWindow, Ui_MainWindow):

    print_factory_on_compute: bool

    def __init__(self, print_factory_on_compute=False):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.print_factory_on_compute = print_factory_on_compute

        # init Factorio data
        load_items()
        load_machines_table()
        load_recipes()
        Recipe.create_ingredients_lists()
        self.needs = {}

        # init GUI
        self.Items_Categories.addItems(["All"] + sorted(Item.categories))
        self.Items_Categories.setCurrentIndex(0)
        self.Items_Categories.currentIndexChanged.connect(self.change_category)
        self.current_category = None
        self.change_category("All")

        self.item_words_index: Dict[str, int] = {}
        self.Item_Search.textChanged.connect(self.search_item)
        self.search_thread = self.search_object = None

        validator = QRegExpValidator(QRegExp(r"[0-9]{1,6}([\.,][0-9]{0,3})?"), self.Item_Count)
        self.Item_Count.setValidator(validator)
        self.Item_Count.setText("1.0")

        self.Item_Add.clicked.connect(self.add_item)
        self.Need_Remove.clicked.connect(self.remove_need)
        self.Compute_Button.clicked.connect(self.compute)

        self.Needs_List.setColumnWidth(0, 75)
        self.Needs_List.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.Needs_List.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.Needs_List.horizontalHeader().setStretchLastSection(True)

        self.Results.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    @pyqtSlot(int)
    def change_category(self, category: Union[str, int]):
        if type(category) is int:
            category = self.Items_Categories.itemText(category)

        if self.current_category == category:
            return
        self.current_category = category

        self.Items_List.clear()

        if category != "All":
            self.Items_List.addItems(sorted(Item.get_category(category)))
        else:
            self.Items_List.addItems(sorted(Item.items_names()))

    @pyqtSlot(str)
    def search_item(self, text: str):
        if len(text) == 0:
            self.change_category(self.Items_Categories.currentText())
            return
        else:
            self.current_category = "Search"

        if self.search_object is None:
            self.search_object = SearchFilter(Item.items_names())
            self.search_thread = QThread()
            self.search_object.clear_list_signal.connect(self.clear_items_list)
            self.search_object.insert_item_to_list_signal.connect(self.insert_item_to_list)
            self.search_object.moveToThread(self.search_thread)
            self.search_thread.start()

        self.search_object.new_search_signal.emit(text)

    @pyqtSlot()
    def clear_items_list(self):
        self.Items_List.clear()

    @pyqtSlot(int, str)
    def insert_item_to_list(self, position: int, text: str):
        self.Items_List.insertItem(position, text)

    @pyqtSlot()
    def add_item(self):
        """
        Adds an item to the list of items produced by the factory
        """
        item = self.Items_List.currentItem()
        if not item:
            return
        item_name = item.text()

        count = self.Item_Count.text()
        if not count:
            return
        else:
            count = float(count.replace(",", "."))

        if item_name in self.needs:
            self.needs[item_name]["count"] += count
            count = self.needs[item_name]["count"]
            self.Needs_List.setItem(self.needs[item_name]["pos"], 0, QTableWidgetItem(str(count)))
        else:
            pos = self.Needs_List.rowCount()
            self.needs[item_name] = {"count": count, "pos": pos}
            self.Needs_List.insertRow(pos)
            self.Needs_List.setItem(pos, 0, QTableWidgetItem(str(count)))
            self.Needs_List.setItem(pos, 1, QTableWidgetItem(item_name))

        self.mark_factory_results_as_invalid()

    @pyqtSlot()
    def remove_need(self):
        row = self.Needs_List.currentRow()
        if row < 0:
            return
        item_name = self.Needs_List.item(row, 1).text()

        self.Needs_List.removeRow(row)
        del self.needs[item_name]

        self.mark_factory_results_as_invalid()

    @pyqtSlot()
    def compute(self):
        reset_factory()

        Item.needs = [(Item.from_str(item), need["count"]) for item, need in self.needs.items()]
        try:
            factory_recipes = compute_factory()
        except Exception:
            import traceback
            print("Error when computing factory:", traceback.format_exc())
            return

        if self.print_factory_on_compute:
            print_factory()

        self.Results.clear()

        total = QTreeWidgetItem(["Total"])
        self.Results.addTopLevelItem(total)

        for used_recipe in Recipe.used_recipes:
            rounded_usage = round(used_recipe.usage, 5)
            n, d, _ = approx(rounded_usage)
            total.addChild(QTreeWidgetItem([used_recipe.name + ": {} / {} ({:.2f})".format(n, d, rounded_usage)]))

        # items produced
        items_root = QTreeWidgetItem(["Items"])
        self.Results.addTopLevelItem(items_root)

        for item, productivity in Item.produced.items():
            items_root.addChild(QTreeWidgetItem(["{}: {:.2f}".format(item.name, productivity["rate"])]))

        # byproducts
        if len(Item.byproducts) > 0:
            byproducts_root = QTreeWidgetItem(["Byproducts"])
            self.Results.addTopLevelItem(byproducts_root)
            for item, count in Item.byproducts.items():
                byproducts_root.addChild(QTreeWidgetItem(["{}: {:.2f}".format(item.name, count)]))

        # structure
        structure_root = QTreeWidgetItem(["Structure"])
        self.Results.addTopLevelItem(structure_root)

        def recursive_structure(root, recipe_result: Dict[str, Any]):
            child = QTreeWidgetItem([recipe_result["item"]])
            if "rate" in recipe_result:
                n, d, _ = approx(recipe_result["count"])
                child.addChild(QTreeWidgetItem(["Count: {} / {} ({:.2f}) - Rate: {:.2f}"
                                               .format(n, d, recipe_result["count"], recipe_result["rate"])]))

            root.addChild(child)

            if recipe_result["recipe"] is not None:
                recipe_entry = QTreeWidgetItem(["Recipe"])
                child.addChild(recipe_entry)
                recipe_entry.addChild(QTreeWidgetItem([recipe_result["recipe"]]))

            if "ingredients" in recipe_result and len(recipe_result["ingredients"]) > 0:
                ingredients = QTreeWidgetItem(["Ingredients"])
                child.addChild(ingredients)
                for ingredient in recipe_result["ingredients"]:
                    recursive_structure(ingredients, ingredient)

        for recipe in factory_recipes:
            recursive_structure(structure_root, recipe)

        # Machines (energy + pollution)
        machines_root = QTreeWidgetItem(["Machines"])
        self.Results.addTopLevelItem(machines_root)

        machines_list = QTreeWidgetItem(["Machines List"])
        machines_root.addChild(machines_list)
        for machine in Machine.machines:
            if machine.count > 0:
                machine_entry = QTreeWidgetItem(["{}: {:.2f}".format(machine.name, machine.count)])
                machines_list.addChild(machine_entry)

        machines_root.addChild(QTreeWidgetItem(["Energy: {:.2f}".format(Machine.get_energy_consumption())]))
        machines_root.addChild(QTreeWidgetItem(["Pollution: {:.2f}".format(Machine.get_pollution_production())]))

        self.unmark_factory_results_as_invalid()

    def keyPressEvent(self, event: QKeyEvent):
        if (self.Items_List.hasFocus() or self.Item_Count.hasFocus() or self.Item_Add.hasFocus()) \
                and event.key() == Qt.Key_Return:
            self.add_item()
        elif self.Needs_List.hasFocus() and event.key() == Qt.Key_Delete:
            self.remove_need()
        elif self.Item_Search.hasFocus() and event.key() == Qt.Key_Escape:
            self.Item_Search.clear()

    def mark_factory_results_as_invalid(self):
        self.Compute_Button.setStyleSheet("background-color: orange")

    def unmark_factory_results_as_invalid(self):
        self.Compute_Button.setStyleSheet("")


if __name__ == '__main__':
    window = FactoryGUI(print_factory_on_compute=True)
    window.show()
    app.exec_()
