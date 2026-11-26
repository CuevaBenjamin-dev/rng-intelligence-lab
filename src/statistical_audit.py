"""Controles estadísticos E01 para secuencias sintéticas de enteros 1..36."""

from collections.abc import Iterable, Mapping
from math import isfinite
from random import Random

MIN_NUMBER = 1
MAX_NUMBER = 36
CATEGORY_COUNT = MAX_NUMBER - MIN_NUMBER + 1
BIASED_NUMBER = 1
BIASED_PROBABILITY = 0.08
OTHER_PROBABILITY = (1.0 - BIASED_PROBABILITY) / (CATEGORY_COUNT - 1)
DEGREES_OF_FREEDOM = CATEGORY_COUNT - 1
ALPHA = 0.05
# NIST/SEMATECH, tabla de cola superior, gl=35, alfa=0.05 (3 decimales).
# https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm
CHI_SQUARE_CRITICAL_VALUE = 49.802


def _validate_positive_int(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_seed(seed: int) -> None:
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")


def generate_uniform(count: int, seed: int) -> list[int]:
    """Genera valores uniformes sintéticos con una semilla explícita."""
    _validate_positive_int(count, "count")
    _validate_seed(seed)
    rng = Random(seed)
    return [rng.randint(MIN_NUMBER, MAX_NUMBER) for _ in range(count)]


def biased_probabilities() -> tuple[float, ...]:
    """Devuelve las probabilidades predefinidas para las 36 categorías."""
    return (BIASED_PROBABILITY,) + (OTHER_PROBABILITY,) * (CATEGORY_COUNT - 1)


def generate_biased(count: int, seed: int) -> list[int]:
    """Genera valores con P(1)=0.08 y el 0.92 restante repartido por igual."""
    _validate_positive_int(count, "count")
    _validate_seed(seed)
    rng = Random(seed)
    return rng.choices(range(MIN_NUMBER, MAX_NUMBER + 1),
                       weights=biased_probabilities(), k=count)


def frequencies(values: Iterable[int]) -> tuple[dict[int, int], dict[int, float]]:
    """Cuenta todas las categorías, incluso las que no aparecen."""
    absolute = {number: 0 for number in range(MIN_NUMBER, MAX_NUMBER + 1)}
    total = 0
    for value in values:
        if isinstance(value, bool) or not isinstance(value, int) or value not in absolute:
            raise ValueError("values must contain integers from 1 to 36")
        absolute[value] += 1
        total += 1
    if total == 0:
        raise ValueError("values must be nonempty")
    relative = {number: count / total for number, count in absolute.items()}
    return absolute, relative


def pearson_chi_square_uniform(absolute: Mapping[int, int]) -> float:
    """Calcula Σ(O-E)²/E con E=n/36; exige E>=5 para la aproximación."""
    if set(absolute) != set(range(MIN_NUMBER, MAX_NUMBER + 1)):
        raise ValueError("absolute must contain exactly categories 1 to 36")
    if any(isinstance(count, bool) or not isinstance(count, int) or count < 0
           for count in absolute.values()):
        raise ValueError("absolute counts must be nonnegative integers")
    expected = sum(absolute.values()) / CATEGORY_COUNT
    if expected < 5:
        raise ValueError("expected count per category must be at least 5")
    return sum((count - expected) ** 2 / expected for count in absolute.values())


def reject_uniformity(statistic: float) -> bool:
    """Aplica la regla de rechazo unilateral superior a alfa=0.05."""
    if isinstance(statistic, bool) or not isinstance(statistic, (int, float)):
        raise ValueError("statistic must be a finite nonnegative number")
    if not isfinite(statistic) or statistic < 0:
        raise ValueError("statistic must be a finite nonnegative number")
    return statistic >= CHI_SQUARE_CRITICAL_VALUE
