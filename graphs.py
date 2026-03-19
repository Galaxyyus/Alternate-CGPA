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

    def compute(self, alpha):
        topo_order = self.topological_sort()

        for course in topo_order:
            course.compute_effective(alpha)

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


def build_graph_from_file(filename: str) -> CourseGraph:
    graph = CourseGraph()

    with open(filename, "r") as f:
        lines = [line.strip() for line in f]

    i = 0
    temp_dependencies = []

    while i < len(lines):
        if lines[i] == "":
            i += 1
            continue

        if not lines[i].startswith("COURSE"):
            raise ValueError(f"Invalid format near line {i + 1}")

        _, pascal_name = lines[i].split()
        course_name = pascal_to_space(pascal_name)

        marks = int(lines[i + 1])

        deps_line = ""
        if i + 2 < len(lines):
            deps_line = lines[i + 2]

        dependencies = []
        if deps_line != "" and not deps_line.startswith("COURSE"):
            dependencies = deps_line.split()
            i += 3
        else:
            i += 2

        graph.add_course(course_name, marks)

        for dep in dependencies:
            dep_name = pascal_to_space(dep)
            temp_dependencies.append((dep_name, course_name))

    for prereq, dependent in temp_dependencies:
        graph.add_dependency(prereq, dependent)

    return graph


def pascal_to_space(name: str) -> str:
    result = []
    for i, ch in enumerate(name):
        if i > 0 and ch.isupper():
            result.append(" ")
        result.append(ch)
    return "".join(result)
