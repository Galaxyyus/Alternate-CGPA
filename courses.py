from __future__ import annotations


class Course:
    """Represents a single course within the academic curriculum graph."""

    def __init__(self, course_id: str, name: str, category: str | None = None):
        """
        Initialize a Course object.
        Args:
            course_id: Unique identifier for the course (e.g., 'CS1101').
            name: Human-readable name of the course.
            category: The category this course belongs to (e.g., 'Core Subject').
        """
        self.id: str = course_id
        self.name: str = name
        self.category: str | None = category

        self.raw_score: int = 0
        self.grade: float | None = None
        self.is_failed: bool = False
        self.failure_type: str | None = None

        self.prerequisites: set[Course] = set()
        self.dependents: set[Course] = set()

        self.year: int | None = None
        self.semester: int | None = None

    def compute_grade(self, alpha: float) -> None:
        """
        Calculates the course grade based on prerequisites and raw score.

        The algorithm uses an 'alpha' factor to balance between the student's 
        current performance and their historical foundation (prerequisites).
        Formula: Grade = (RawScore/10 + alpha * Sum(PrereqGrades)) / (1 + alpha * NumPrereqs)
        
        Args:
            alpha: Weighting factor for prerequisite influence.
        """
        self.is_failed = False
        self.failure_type = None

        # Excellence Bypass: Raw score >= 85 -> Grade directly, ignore prereqs
        if self.raw_score >= 85:
            self.grade = self.raw_score / 10
            return
        # Raw score < 40 -> Fail
        if self.raw_score < 40:
            self.is_failed = True
            self.failure_type = "SELF_FAIL"
            self.grade = 3.0  # Normalized failing grade
            return

        # Check for prerequisite failures
        failed_prereqs = [p for p in self.prerequisites if p.is_failed]
        if failed_prereqs:
            self.is_failed = True
            self.failure_type = "PREREQ_FAIL"
            self.grade = 3.0
            return

        # Normal case
        if not self.prerequisites:
            self.grade = self.raw_score / 10
            return

        # DAG Propagation: Calculate grade influenced by prerequisites
        prerequisites_sum = 0.0
        for prereq in self.prerequisites:
            if (grade := prereq.grade) is not None:
                prerequisites_sum += grade
            else:
                raise ValueError(f"Cannot compute {self.name}: prerequisite not evaluated yet")

        # The core Alternate grade formula
        self.grade = ((self.raw_score / 10) + alpha * prerequisites_sum) / (1 + len(self.prerequisites) * alpha)

    def get_root_failures(self) -> set[Course]:
        """
        Recursively identifies the original 'SELF_FAIL' courses that caused this failure.
        
        Returns:
            A set of Course objects that are the primary point of failure.
        """
        if not self.is_failed:
            return set()
        if self.failure_type == "SELF_FAIL":
            return {self}

        # If it's a PREREQ_FAIL, trace back through prerequisites
        roots = set()
        for prereq in self.prerequisites:
            roots.update(prereq.get_root_failures())
        return roots

    def print_details(self, alpha: float) -> None:
        """
        Prints a detailed breakdown of the course's grade components.
        
        Args:
            alpha: Prerequisite influence factor used in computation.
        """
        print(f"\nCourse: {self.id} ({self.name})")
        print(f"Category: {self.category}")
        print(f"Raw Score: {self.raw_score}")
        print(f"Final Grade: {self.grade:.2f}" if self.grade is not None else "Final Grade: None")

        if not self.prerequisites:
            print("Prerequisites: None")
            return

        if self.raw_score <= 85:
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
        else:
            print("Marks Threshold Crossed!!!")
            print("Graded only on the basis of raw score")

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Determines equality based on unique course ID."""
        return isinstance(other, Course) and self.id == other.id

    def __repr__(self) -> str:
        """String representation for debugging and list printing."""
        grade_str = f"{self.grade:.2f}" if self.grade is not None else "None"
        return f"{self.id} {self.name}: score={self.raw_score}, grade={grade_str}"
