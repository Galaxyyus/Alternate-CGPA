from __future__ import annotations


class Course:
    def __init__(self, course_id: str, name: str, category: str | None = None):
        self.id: str = course_id
        self.name: str = name
        self.category: str | None = category

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

        prerequisites_sum = 0.0
        for prereq in self.prerequisites:
            if (grade := prereq.grade) is not None:
                prerequisites_sum += grade
            else:
                raise ValueError(f"Cannot compute {self.name}: prerequisite not evaluated yet")

        self.grade = ((self.raw_score / 10) + alpha * prerequisites_sum) / (1 + len(self.prerequisites) * alpha)

    def print_details(self, alpha: float) -> None:
        print(f"\nCourse: {self.id} ({self.name})")
        print(f"Category: {self.category}")
        print(f"Raw Score: {self.raw_score}")
        print(f"Final Grade: {self.grade:.2f}" if self.grade is not None else "Final Grade: None")

        if not self.prerequisites:
            print("Prerequisites: None")
            return

        print("Prerequisites :")
        weight_per_prereq = alpha / (1 + alpha * len(self.prerequisites))
        total_prereq_influence = 0.0

        for prereq in self.prerequisites:
            grade = prereq.grade if prereq.grade is not None else 0.0
            influence = grade * weight_per_prereq
            total_prereq_influence += influence
            print(f"  - {prereq.id} ({prereq.name}): Grade {grade:.2f} -> Contributes {influence:.2f}")

        base_contribution = self.raw_score / (10 * (1 + alpha * len(self.prerequisites)))
        print(f"Base score contribution : {base_contribution:.2f}")
        print(f"Prerequisite contribution : {total_prereq_influence:.2f}")

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Course) and self.id == other.id

    def __repr__(self) -> str:
        grade_str = f"{self.grade:.2f}" if self.grade is not None else "None"
        return f"{self.id} {self.name}: score={self.raw_score}, grade={grade_str}"
