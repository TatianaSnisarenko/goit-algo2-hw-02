import unittest
from task_one import optimize_printing


class TestOptimizePrinting(unittest.TestCase):
    def test_optimize_printing_same_priority(self):
        print_jobs = [
            {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
            {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
        ]
        constraints = {"max_volume": 300, "max_items": 2}
        result = optimize_printing(print_jobs, constraints)
        self.assertEqual(result["print_order"], ["M1", "M2", "M3"])
        self.assertEqual(result["total_time"], 270)

    def test_optimize_printing_different_priorities(self):
        print_jobs = [
            {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
            {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
        ]
        constraints = {"max_volume": 300, "max_items": 2}
        result = optimize_printing(print_jobs, constraints)
        self.assertEqual(result["print_order"], ["M2", "M1", "M3"])
        self.assertEqual(result["total_time"], 270)

    def test_optimize_printing_exceeds_volume_limit(self):
        print_jobs = [
            {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
            {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
            {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
        ]
        constraints = {"max_volume": 300, "max_items": 2}
        result = optimize_printing(print_jobs, constraints)
        self.assertEqual(result["print_order"], ["M1", "M2", "M3"])
        self.assertEqual(result["total_time"], 450)

    def test_one_of_jobs_ecxeeds_printer_volume_limit(self):
        print_jobs = [
            {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
            {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
            {"id": "M3", "volume": 380, "priority": 2, "print_time": 120},
        ]
        constraints = {"max_volume": 300, "max_items": 2}
        with self.assertRaises(ValueError) as context:
            optimize_printing(print_jobs, constraints)
        self.assertRegex(
            str(context.exception), "Об'єм моделі .* перевищує ліміт принтера"
        )

    def test_optimize_printing_invalid_constraints(self):
        print_jobs = [
            {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        ]
        constraints = {"max_volume": 0, "max_items": 2}
        with self.assertRaises(ValueError) as context:
            optimize_printing(print_jobs, constraints)
        self.assertRegex(
            str(context.exception), "Обмеження принтера мають бути більшими за нуль"
        )

    def test_optimize_printing_invalid_items_limit(self):
        print_jobs = [
            {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        ]
        constraints = {"max_volume": 300, "max_items": 0}
        with self.assertRaises(ValueError) as context:
            optimize_printing(print_jobs, constraints)
        self.assertRegex(
            str(context.exception), "Обмеження принтера мають бути більшими за нуль"
        )


if __name__ == "__main__":
    unittest.main()
