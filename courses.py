from __future__ import annotations


class Course:
    def __init__(self, name: str, raw_score: int):
        if not (0 <= raw_score <= 100):
            raise ValueError("raw_score must be between 0 and 100")

        self.name: str = name

        self.raw_score: int = raw_score
        self.grade: float | None = None

        self.prerequisites: set[Course] = set()
        self.dependents: set[Course] = set()

    def compute_effective(self, alpha: float) -> None:
        if not self.prerequisites:
            self.grade = self.raw_score / 10
            return

        prerequisites_average = 0
        for parent in self.prerequisites:
            if (grade := parent.grade) is not None:
                prerequisites_average += grade
            else:
                raise ValueError(f"Cannot compute {self.name}: prerequisite not evaluated yet")
        prerequisites_average /= len(self.prerequisites)

        self.grade = (alpha * self.raw_score / 10) + ((1 - alpha) * prerequisites_average)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Course) and self.name == other.name

    def __repr__(self):
        return f"{self.name}: score={self.raw_score}, grade={self.grade: .2f}"
