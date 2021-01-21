
from typing import Tuple
from math import gcd


def approx(r: float, max_iter: int = 1000) -> Tuple[int, int, float]:
    """
    Inefficient algorithm used to approximate a rational into its numerator / denominator.
    Since float.as_integer_ratio() does sometimes return VERY BAD results (like for 0.4 or 0.3 and their multiples),
    and since this algorithm can only return low values for n and d, it is sometimes preferable over the Python
    function.

    It works by starting with 1/2, and then by adding 1 to the numerator if the fraction is less than r, or by adding 1
    to the denominator if the fraction is more than r. We do this until the fraction is equal to r or when we reached
    max_iter iterations.
    To make the algorithm more efficient, any number superior to 2 is divided by a power of 10 to make it have only 1
    digit before the dot, as it more efficient at getting to little values (e.g. if r = 10e6 and max_iter = 10e3, it is
    impossible for n/d to reach 10e6 in less than 1000 iterations).

    :param r: rational to approximate
    :param max_iter: maximum of iterations, or the precision of the approximation in general
    :return: numerator, denominator, error (r - n/d)
    """
    if r == int(r):
        return int(r), 1, 0
    if r > 2:
        factor = 10**(str(r).index("."))
        r /= factor
    else:
        factor = 1

    n = 1.0
    d = 2.0

    iterations = 0
    while iterations < max_iter:
        f = n / d
        if f < r:
            n += 1
        elif f == r:
            break
        else:  # f > r
            d += 1

        iterations += 1

    e = r - n / d
    n = int(n * factor)
    d = int(d)

    cd = gcd(n, d)
    n /= cd
    d /= cd

    return int(n), int(d), e


if __name__ == "__main__":
    a, b, err = approx(0.18)
    print("a = {}\nb = {}\ne = {}\ntest = {}".format(a, b, err, float(a) / b))
