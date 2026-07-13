"""Небольшие функции для тренировки базового Python."""

from typing import List


def weight_gain(start_weight: float, current_weight: float) -> float:
    """Вернуть изменение веса в килограммах."""
    return current_weight - start_weight


def average_gain_per_week(
    start_weight: float, current_weight: float, weeks: float
) -> float:
    """Вернуть среднее изменение веса за неделю."""
    if weeks <= 0:
        raise ValueError("Количество недель должно быть больше нуля")
    return weight_gain(start_weight, current_weight)/weeks


def completed_rate(sessions: List[bool]) -> float:
    """Вернуть долю выполненных занятий в процентах."""
    if len(sessions) == 0:
        return 0.0
    return sum(sessions)/len(sessions)*100


if __name__ == "__main__":
    print("Прирост веса:", weight_gain(61, 70), "кг")
