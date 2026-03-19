from collections import deque

from courses import Course


class CourseGraph:
    def __init__(self):
        self.courses = {}

    def add_course(self, name, raw_grade):
        if name not in self.courses:
            self.courses[name] = Course(name, raw_grade)

    def add_dependency(self, parent, child):
        self.courses[parent].dependents.add(self.courses[child])
        self.courses[child].prerequisites.add(self.courses[parent])

    def topological_sort(self):
        in_degree = {c: len(c.prerequisites) for c in self.courses.values()}
        queue = deque()

        for course, deg in in_degree.items():
            if deg == 0:
                queue.append(course)

        topo_order = []

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
