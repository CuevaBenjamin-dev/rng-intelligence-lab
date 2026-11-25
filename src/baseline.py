"""E00: local synthetic control. Not a cryptographic RNG or real-system audit."""
from collections import Counter
from random import Random

MIN_NUMBER = 1
MAX_NUMBER = 36


def generate_uniform(count: int, seed: int = 42) -> list[int]:
    if count < 1:
        raise ValueError("count must be positive")
    rng = Random(seed)
    return [rng.randint(MIN_NUMBER, MAX_NUMBER) for _ in range(count)]


def accuracy(actual: list[int], predicted: list[int]) -> float:
    if not actual or len(actual) != len(predicted):
        raise ValueError("expected nonempty sequences of equal length")
    return sum(a == p for a, p in zip(actual, predicted)) / len(actual)


def evaluate(count: int = 10_000, seed: int = 42) -> dict:
    if count < 5:
        raise ValueError("count must be at least 5")
    values = generate_uniform(count, seed)
    split = int(count * 0.8)
    train, test = values[:split], values[split:]
    frequencies = Counter(train)
    # Deterministic tie-breaking, using training observations only.
    mode = min(frequencies, key=lambda n: (-frequencies[n], n))
    rng = Random(seed + 1)
    uniform_predictions = [rng.randint(MIN_NUMBER, MAX_NUMBER) for _ in test]
    return {
        "train_count": len(train),
        "test_count": len(test),
        "theoretical_uniform": 1 / MAX_NUMBER,
        "uniform_accuracy": accuracy(test, uniform_predictions),
        "historical_mode": mode,
        "frequency_accuracy": accuracy(test, [mode] * len(test)),
    }


def main() -> None:
    result = evaluate()
    print("E00 | CONTROL SINTETICO | Sin datos del cliente")
    print(f"Entrenamiento: {result['train_count']} | Prueba: {result['test_count']}")
    print(f"Referencia teorica uniforme: {result['theoretical_uniform']:.2%}")
    print(f"Selector uniforme independiente: {result['uniform_accuracy']:.2%}")
    print(f"Referencia de frecuencia historica: {result['frequency_accuracy']:.2%}")
    print("Una diferencia muestral no demuestra predictibilidad ni seguridad.")


if __name__ == "__main__":
    main()
