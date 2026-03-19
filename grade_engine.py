import file_loader

class GradeEngine:
    def __init__(self, alpha: float) -> None:
        self.alpha = alpha

        graph = file_loader.load_courses_structure("course.json")
        file_loader.load_grades("score.json", graph)
        self.graph = graph

        topo_order = graph.topological_sort()
        for course in topo_order:
            course.compute_grade(self.alpha)

    def get_cgpa(self) -> float:
        evaluated_courses = [course for course in self.graph.courses.values() if course.grade is not None]

        if not evaluated_courses:
            print("No courses evaluated.")
            return 0.0

        terminal_courses = [course for course in evaluated_courses if not course.dependents]

        if not terminal_courses:
            print("No terminal evaluated courses found. Cannot compute CGPA.")
            return 0.0

        total = sum(course.grade * self.graph.credit_map[course.category] for course in terminal_courses)
        cgpa = total / sum(self.graph.credit_map[course.category] for course in terminal_courses)

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
