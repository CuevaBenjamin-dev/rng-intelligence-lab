"""E02: calibración reproducible de una prueba de dependencia temporal."""

from collections.abc import Callable
from dataclasses import dataclass
from math import sqrt
from random import Random
from statistics import NormalDist

from src.statistical_audit import (
    ALPHA,
    BIASED_NUMBER,
    CATEGORY_COUNT,
    MAX_NUMBER,
    MIN_NUMBER,
    _validate_positive_int,
    _validate_seed,
    frequencies,
    generate_uniform,
)
from src.temporal_audit import (
    PERMUTATIONS,
    REPEAT_PROBABILITY,
    generate_sticky_uniform,
    permutation_test,
)

RUN_COUNT = 100
OBSERVATIONS_PER_RUN = 3_600
NEGATIVE_SEED = 20261127
POSITIVE_SEED = 20261128


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    runs: int
    observations_per_run: int
    rejections: int
    total_repeats: int
    absolute_frequencies: dict[int, int]

    @property
    def rejection_rate(self) -> float:
        return self.rejections / self.runs

    @property
    def mean_repeats(self) -> float:
        return self.total_repeats / self.runs

    @property
    def category_one_rate(self) -> float:
        return self.absolute_frequencies[BIASED_NUMBER] / (
            self.runs * self.observations_per_run
        )

    @property
    def rejection_interval(self) -> tuple[float, float]:
        return wilson_interval(self.rejections, self.runs)


def wilson_interval(successes: int, trials: int) -> tuple[float, float]:
    """Intervalo de puntuación de Wilson al 95 % para una tasa binomial."""
    _validate_positive_int(trials, "trials")
    if (isinstance(successes, bool) or not isinstance(successes, int)
            or not 0 <= successes <= trials):
        raise ValueError("successes must be an integer between 0 and trials")
    z = NormalDist().inv_cdf(0.975)
    rate = successes / trials
    denominator = 1 + z * z / trials
    center = (rate + z * z / (2 * trials)) / denominator
    margin = z * sqrt(rate * (1 - rate) / trials + z * z / (4 * trials**2))
    margin /= denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def run_scenario(
    name: str,
    generator: Callable[[int, int], list[int]],
    runs: int = RUN_COUNT,
    observations_per_run: int = OBSERVATIONS_PER_RUN,
    permutations: int = PERMUTATIONS,
    seed: int = NEGATIVE_SEED,
) -> ScenarioResult:
    """Evalúa corridas con subsemillas separadas para datos y permutaciones."""
    _validate_positive_int(runs, "runs")
    _validate_positive_int(observations_per_run, "observations_per_run")
    _validate_seed(seed)
    if observations_per_run < 2:
        raise ValueError("observations_per_run must be at least 2")
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a nonempty string")

    master = Random(seed)
    aggregate = {number: 0 for number in range(MIN_NUMBER, MAX_NUMBER + 1)}
    rejections = 0
    repeats = 0
    for _ in range(runs):
        values = generator(observations_per_run, master.getrandbits(64))
        if len(values) != observations_per_run:
            raise ValueError("generator returned an unexpected number of observations")
        absolute, _ = frequencies(values)
        for number, count in absolute.items():
            aggregate[number] += count
        test = permutation_test(values, master.getrandbits(64), permutations)
        rejections += test.rejects
        repeats += test.observed_repeats
    return ScenarioResult(name, runs, observations_per_run, rejections,
                          repeats, aggregate)


def main() -> None:
    negative = run_scenario("independiente", generate_uniform,
                            seed=NEGATIVE_SEED)
    positive = run_scenario("dependiente", generate_sticky_uniform,
                            seed=POSITIVE_SEED)
    print("E02 | CONTROL SINTÉTICO | Sin datos del cliente")
    print(f"{RUN_COUNT} corridas por escenario × {OBSERVATIONS_PER_RUN} observaciones; "
          f"{PERMUTATIONS} permutaciones por corrida; α={ALPHA}")
    print(f"Semillas maestras: control={NEGATIVE_SEED}, dependiente={POSITIVE_SEED}; "
          f"probabilidad de repetición adicional={REPEAT_PROBABILITY:.2%}")
    print("Escenario | Rechazos | Tasa (IC Wilson 95 %) | Repeticiones medias "
          "| Frecuencia agregada de 1")
    for result in (negative, positive):
        low, high = result.rejection_interval
        print(f"{result.name:12} | {result.rejections:3}/{result.runs} | "
              f"{result.rejection_rate:5.1%} ({low:5.1%}–{high:5.1%}) | "
              f"{result.mean_repeats:7.1f} | "
              f"{result.absolute_frequencies[BIASED_NUMBER]}/"
              f"{result.runs * result.observations_per_run} "
              f"({result.category_one_rate:.2%})")
    print(f"Referencia marginal uniforme por categoría: {1 / CATEGORY_COUNT:.2%}.")
    print("La prueba detecta exceso de repeticiones bajo intercambiabilidad; "
          "no demuestra independencia general ni seguridad criptográfica.")


if __name__ == "__main__":
    main()
