import file_loader


class GradeEngine:
    def __init__(self, alpha: float, course_file: str = "course.json", score_file: str = "score.json") -> None:
        self.alpha = alpha

        graph = file_loader.load_courses_structure(course_file)
        file_loader.load_grades(score_file, graph)
        self.graph = graph

        topo_order = graph.topological_sort()
        for course in topo_order:
            course.compute_grade(self.alpha)

    def get_cgpa(self, up_to_year: int | None = None, up_to_semester: int | None = None) -> float:
        evaluated_courses = [course for course in self.graph.courses.values() if course.grade is not None]

        if up_to_year is not None:
            evaluated_courses = [c for c in evaluated_courses if c.year is not None and c.year <= up_to_year]
        if up_to_semester is not None:
            evaluated_courses = [c for c in evaluated_courses if c.semester is not None and c.semester <= up_to_semester]

        if not evaluated_courses:
            return 0.0

        # Identify failures and reporting root causes
        failed_in_scope = [c for c in evaluated_courses if c.is_failed]
        if failed_in_scope:
            print("\n!!! FAILURES DETECTED !!!")
            root_failures = set()
            for c in failed_in_scope:
                root_failures.update(c.get_root_failures())
            
            print("To pass, the student must retake the following 'root' failed exams:")
            for rf in sorted(root_failures, key=lambda x: (x.year or 0, x.semester or 0)):
                print(f"  - {rf.id}: {rf.name} (Year {rf.year}, Sem {rf.semester}) [Raw Score: {rf.raw_score}]")
            print("--------------------------\n")

        terminal_courses = [course for course in evaluated_courses if not any(dep in evaluated_courses for dep in course.dependents)]

        if not terminal_courses:
            return 0.0

        total = sum(course.grade * self.graph.credit_map[course.category] for course in terminal_courses)  # type: ignore
        cgpa = total / sum(self.graph.credit_map[course.category] for course in terminal_courses)  # type: ignore

        return cgpa

    def print_course_details(self, course_identifier: str) -> None:
        target_course = None
        for cid, course in self.graph.courses.items():
            if cid == course_identifier or course.name == course_identifier:
                target_course = course
                break

        if not target_course:
            print(f"Course '{course_identifier}' not found.")
            return

        target_course.print_details(self.alpha)
