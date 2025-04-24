from typing import List, Dict

from numpy import inf


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Ініціалізація кешу для мемоізації
    memo = {}

    def helper(n):
        # Якщо результат вже є в кеші
        if n in memo:
            return memo[n]

        # Базовий випадок: якщо довжина стрижня 0, прибуток 0
        if n == 0:
            return 0, []

        max_profit = -inf
        best_cuts = []

        # Перебір усіх можливих розрізів
        for i in range(1, n + 1):
            if i <= len(prices):
                current_profit, cuts = helper(n - i)
                current_profit += prices[i - 1]

                # Оновлення максимального прибутку
                if current_profit > max_profit:
                    max_profit = current_profit
                    best_cuts = cuts + [i]

        # Збереження результату в кеш
        memo[n] = (max_profit, best_cuts)
        return memo[n]

    # Виклик рекурсивної функції
    max_profit, cuts = helper(length)

    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": len(cuts) - 1}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Ініціалізація таблиць для збереження максимального прибутку та розрізів
    dp = [0] * (length + 1)  # dp[i] зберігає максимальний прибуток для довжини i
    cuts = [0] * (length + 1)  # cuts[i] зберігає оптимальний розріз для довжини i

    # Заповнення таблиці dp
    for i in range(1, length + 1):  # Для кожної довжини стрижня
        max_profit = -inf
        for j in range(1, i + 1):  # Для кожного можливого розрізу
            if j <= len(prices):
                current_profit = prices[j - 1] + dp[i - j]
                if current_profit > max_profit:
                    max_profit = current_profit
                    cuts[i] = j  # Зберігаємо оптимальний розріз
        dp[i] = max_profit  # Зберігаємо максимальний прибуток для довжини i

    # Відновлення списку розрізів
    result_cuts = []
    n = length
    while n > 0:
        result_cuts.append(cuts[n])
        n -= cuts[n]

    return {
        "max_profit": dp[length],
        "cuts": result_cuts,
        "number_of_cuts": len(result_cuts) - 1,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        # Тест 2: Оптимально не різати
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        # Тест 3: Всі розрізи по 1
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
