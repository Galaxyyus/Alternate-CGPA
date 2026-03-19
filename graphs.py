from collections import deque
from courses import Course


class CourseGraph:
    def __init__(self, categories: dict[str, int] | None = None) -> None:
        self.courses: dict[str, Course] = {}
        self.credit_map: dict[str, int] = categories if categories is not None else {}

    def add_course(self, course_id: str, name: str, category: str | None = None) -> None:
        if course_id not in self.courses:
            self.courses[course_id] = Course(course_id, name, category)

    def add_dependency(self, prerequisites: str, dependent: str) -> None:
        self.courses[prerequisites].dependents.add(self.courses[dependent])
        self.courses[dependent].prerequisites.add(self.courses[prerequisites])

    def compute(self, alpha: float) -> None:
        topo_order = self.topological_sort()

        for course in topo_order:
            course.compute_grade(alpha)

    def validate(self) -> None:
        """Validates the graph to ensure there are no cycles."""
        self.topological_sort()

    def topological_sort(self) -> list[Course]:
        in_degree = {c: len(c.prerequisites) for c in self.courses.values()}
        queue: deque[Course] = deque()

        for course, deg in in_degree.items():
            if deg == 0:
                queue.append(course)

        topo_order: list[Course] = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)

            for dependent in node.dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(topo_order) != len(self.courses):
            raise ValueError("Graph contains a cycle")

        return topo_order
