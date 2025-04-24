from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(
    print_jobs: List[PrintJob], constraints: PrinterConstraints
) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворення і сортування словників у об'єкти
    jobs = sorted((PrintJob(**job) for job in print_jobs), key=lambda x: x.priority)

    # Перевірка обмежень принтера
    printer = PrinterConstraints(**constraints)
    if printer.max_volume <= 0 or printer.max_items <= 0:
        raise ValueError("Обмеження принтера мають бути більшими за нуль.")

    print_order = []
    total_time = 0
    used = [False] * len(jobs)

    i = 0
    while i < len(jobs):
        group = []
        volume_sum = 0
        count = 0
        skipped_priority = -1

        # Групування завдань, які відповідають обмеженням об'єму та кількості
        max_time = 0
        for j in range(i, len(jobs)):
            if not used[j] and jobs[j].priority >= skipped_priority:
                if (
                    volume_sum + jobs[j].volume <= printer.max_volume
                    and count + 1 <= printer.max_items
                ):
                    group.append(jobs[j])
                    volume_sum += jobs[j].volume
                    count += 1
                    used[j] = True
                    max_time = max(max_time, jobs[j].print_time)

            else:
                if jobs[j].priority > skipped_priority:
                    skipped_priority = jobs[j].priority

        if (
            not group
        ):  # якщо не вдалося зібрати групу (можливо модель перевищує ліміт сама)
            for j in range(len(jobs)):
                if not used[j] and jobs[j].volume > printer.max_volume:
                    raise ValueError(
                        f"Об'єм моделі {jobs[j].volume} для {jobs[j].id} перевищує ліміт принтера.  Ліміт: {printer.max_volume}."
                    )

        # Фіксація групи в результат
        print_order.extend([job.id for job in group])
        total_time += max_time

        i += 1
        while i < len(jobs) and used[i]:
            i += 1

    return {"print_order": print_order, "total_time": total_time}


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
