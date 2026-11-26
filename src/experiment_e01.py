"""E01: repetición local de pruebas de uniformidad con datos sintéticos."""

from collections.abc import Callable
from dataclasses import dataclass
from random import Random

from src.statistical_audit import (
    ALPHA,
    BIASED_NUMBER,
    CHI_SQUARE_CRITICAL_VALUE,
    DEGREES_OF_FREEDOM,
    MIN_NUMBER,
    MAX_NUMBER,
    _validate_positive_int,
    _validate_seed,
    frequencies,
    generate_biased,
    generate_uniform,
    pearson_chi_square_uniform,
    reject_uniformity,
)

RUN_COUNT = 100
OBSERVATIONS_PER_RUN = 3_600
MASTER_SEED = 20261125


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    runs: int
    observations_per_run: int
    rejections: int
    absolute_frequencies: dict[int, int]
    relative_frequencies: dict[int, float]

    @property
    def rejection_rate(self) -> float:
        return self.rejections / self.runs


def run_scenario(
    name: str,
    generator: Callable[[int, int], list[int]],
    runs: int = RUN_COUNT,
    observations_per_run: int = OBSERVATIONS_PER_RUN,
    seed: int = MASTER_SEED,
) -> ScenarioResult:
    """Ejecuta corridas con subsemillas distintas y agrega sus frecuencias."""
    _validate_positive_int(runs, "runs")
    _validate_positive_int(observations_per_run, "observations_per_run")
    _validate_seed(seed)
    if observations_per_run < 180:
        raise ValueError("observations_per_run must be at least 180")
    if not name:
        raise ValueError("name must be nonempty")

    master = Random(seed)
    aggregate = {number: 0 for number in range(MIN_NUMBER, MAX_NUMBER + 1)}
    rejections = 0
    for _ in range(runs):
        values = generator(observations_per_run, master.getrandbits(64))
        if len(values) != observations_per_run:
            raise ValueError("generator returned an unexpected number of observations")
        absolute, _ = frequencies(values)
        statistic = pearson_chi_square_uniform(absolute)
        rejections += reject_uniformity(statistic)
        for number, count in absolute.items():
            aggregate[number] += count

    total = runs * observations_per_run
    relative = {number: count / total for number, count in aggregate.items()}
    return ScenarioResult(name, runs, observations_per_run, rejections,
                          aggregate, relative)


def main() -> None:
    uniform = run_scenario("uniforme", generate_uniform, seed=MASTER_SEED)
    biased = run_scenario("sesgado", generate_biased, seed=MASTER_SEED + 1)
    print("E01 | CONTROL SINTÉTICO | Sin datos del cliente")
    print(f"{RUN_COUNT} corridas por escenario × {OBSERVATIONS_PER_RUN} observaciones "
          f"| gl={DEGREES_OF_FREEDOM} | α={ALPHA}")
    print(f"Valor crítico χ² (NIST, 3 decimales): {CHI_SQUARE_CRITICAL_VALUE:.3f}")
    print("Escenario | Rechazos | Tasa | Frecuencia absoluta de 1 | Frecuencia relativa de 1")
    for result in (uniform, biased):
        print(f"{result.name:8} | {result.rejections:3}/{result.runs} | "
              f"{result.rejection_rate:6.1%} | "
              f"{result.absolute_frequencies[BIASED_NUMBER]:6} | "
              f"{result.relative_frequencies[BIASED_NUMBER]:6.2%}")
    print("Frecuencias agregadas por categoría (absoluta, relativa):")
    print("Número | Uniforme | Sesgado")
    for number in range(MIN_NUMBER, MAX_NUMBER + 1):
        print(f"{number:>6} | "
              f"{uniform.absolute_frequencies[number]:>6}, {uniform.relative_frequencies[number]:6.2%} | "
              f"{biased.absolute_frequencies[number]:>6}, {biased.relative_frequencies[number]:6.2%}")
    print("Las tasas de 100 corridas fluctúan; el test solo evalúa la distribución marginal.")


if __name__ == "__main__":
    main()
