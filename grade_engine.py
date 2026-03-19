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

    def print_cgpa(self) -> None:
        evaluated_courses = [course for course in self.graph.courses.values() if course.grade is not None]

        if not evaluated_courses:
            print("No courses evaluated.")
            return

        total = sum(course.grade for course in evaluated_courses)
        cgpa = total / len(evaluated_courses)

        print(f"CGPA : {cgpa:.2f}\n")
