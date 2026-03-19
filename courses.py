from __future__ import annotations


class Course:
    def __init__(self, course_id: str, name: str):
        self.id: str = course_id
        self.name: str = name

        self.raw_score: int = 0
        self.grade: float | None = None

        self.prerequisites: set[Course] = set()
        self.dependents: set[Course] = set()

        self.year: int | None = None
        self.semester: int | None = None

    def compute_grade(self, alpha: float) -> None:
        if not self.prerequisites:
            self.grade = self.raw_score / 10
            return

        prerequisites_average = 0.0
        for prereq in self.prerequisites:
            if (grade := prereq.grade) is not None:
                prerequisites_average += grade
            else:
                raise ValueError(
                    f"Cannot compute {self.name}: prerequisite not evaluated yet"
                )
        prerequisites_average /= len(self.prerequisites)

        self.grade = (alpha * self.raw_score / 10) + (
            (1 - alpha) * prerequisites_average
        )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Course) and self.id == other.id

    def __repr__(self) -> str:
        grade_str = f"{self.grade:.2f}" if self.grade is not None else "None"
        return f"{self.id} {self.name}: score={self.raw_score}, grade={grade_str}"
