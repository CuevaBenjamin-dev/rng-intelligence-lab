"""E02: controles sintéticos y prueba condicional de orden temporal."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite
from random import Random

from src.statistical_audit import (
    ALPHA,
    MAX_NUMBER,
    MIN_NUMBER,
    _validate_positive_int,
    _validate_seed,
    frequencies,
)

REPEAT_PROBABILITY = 0.02
PERMUTATIONS = 199


@dataclass(frozen=True)
class PermutationResult:
    observed_repeats: int
    extreme_permutations: int
    permutations: int
    p_value: float

    @property
    def rejects(self) -> bool:
        return self.p_value <= ALPHA


def generate_sticky_uniform(
    count: int, seed: int, repeat_probability: float = REPEAT_PROBABILITY
) -> list[int]:
    """Cadena estacionaria uniforme con repeticiones adicionales conocidas."""
    _validate_positive_int(count, "count")
    _validate_seed(seed)
    if count < 2:
        raise ValueError("count must be at least 2")
    if (isinstance(repeat_probability, bool)
            or not isinstance(repeat_probability, (int, float))
            or not isfinite(repeat_probability)
            or not 0 <= repeat_probability <= 1):
        raise ValueError("repeat_probability must be between 0 and 1")

    rng = Random(seed)
    values = [rng.randint(MIN_NUMBER, MAX_NUMBER)]
    for _ in range(count - 1):
        if rng.random() < repeat_probability:
            values.append(values[-1])
        else:
            values.append(rng.randint(MIN_NUMBER, MAX_NUMBER))
    return values


def _count_repeats(values: Sequence[int]) -> int:
    return sum(left == right for left, right in zip(values, values[1:]))


def adjacent_repeat_count(values: Sequence[int]) -> int:
    """Cuenta pares consecutivos iguales tras validar la secuencia."""
    if len(values) < 2:
        raise ValueError("values must contain at least 2 observations")
    frequencies(values)
    return _count_repeats(values)


def permutation_test(
    values: Sequence[int], seed: int, permutations: int = PERMUTATIONS
) -> PermutationResult:
    """Prueba unilateral de repeticiones mediante barajado condicionado en conteos."""
    _validate_seed(seed)
    _validate_positive_int(permutations, "permutations")
    if permutations < 19:
        raise ValueError("at least 19 permutations are needed at alpha=0.05")
    observed = adjacent_repeat_count(values)
    rng = Random(seed)
    extreme = 0
    for _ in range(permutations):
        shuffled = list(values)
        rng.shuffle(shuffled)
        extreme += _count_repeats(shuffled) >= observed
    return PermutationResult(observed, extreme, permutations,
                             (extreme + 1) / (permutations + 1))
