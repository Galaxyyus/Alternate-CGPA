from __future__ import annotations
import math


class Course:
    def __init__(self, name: str, raw_score: int):
        if not (0 <= raw_score <= 100):
            raise ValueError("raw_score must be between 0 and 100")

        self.name: str = name

        self.raw_score: int = raw_score
        self.raw_grade: int = self._compute_raw_grade(raw_score)
        self.effective_grade: int | None = None

        self.prerequisites: set[Course] = set()
        self.dependents: set[Course] = set()

    def _compute_raw_grade(self, score: float) -> int:
        grade = int(score // 10) + 1
        return min(grade, 10)

    def compute_effective(self, alpha: float) -> None:
        if not self.prerequisites:
            self.effective_grade = self.raw_grade
            return

        parent_avg = 0
        for parent in self.prerequisites:
            if (grade := parent.effective_grade) is not None:
                parent_avg += grade
            else:
                raise ValueError(f"Cannot compute {self.name}: prerequisite not evaluated yet")

        parent_avg /= len(self.prerequisites)

        value = alpha * self.raw_grade + (1 - alpha) * parent_avg

        self.effective_grade = math.ceil(value)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Course) and self.name == other.name

    def __repr__(self):
        return f"{self.name}: score={self.raw_score}, raw_grade={self.raw_grade}, effective={self.effective_grade}"
