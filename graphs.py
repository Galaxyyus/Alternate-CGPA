from collections import deque
from courses import Course


class CourseGraph:
    """Manages the curriculum as a Directed Acyclic Graph (DAG) for prerequisite tracking."""

    def __init__(self, categories: dict[str, int] | None = None) -> None:
        """
        Initialize the CourseGraph.

        Args:
            categories: A mapping of category names to their credit/weight value.
        """
        self.courses: dict[str, Course] = {}
        # Stores weights for different categories (e.g., {'Core Subject': 5})
        self.credit_map: dict[str, int] = categories if categories is not None else {}

    def add_course(self, course_id: str, name: str, category: str | None = None) -> None:
        """Adds a new course node to the graph if it doesn't already exist."""
        if course_id not in self.courses:
            self.courses[course_id] = Course(course_id, name, category)

    def add_dependency(self, prerequisites: str, dependent: str) -> None:
        """
        Links two courses in the DAG.
        
        Args:
            prerequisites: The ID of the course that must be taken first.
            dependent: The ID of the course that requires the prerequisite.
        """
        self.courses[prerequisites].dependents.add(self.courses[dependent])
        self.courses[dependent].prerequisites.add(self.courses[prerequisites])

    def compute(self, alpha: float) -> None:
        """
        Runs the grading computation across all courses in topological order.
        
        This ensures that prerequisites are always calculated before their dependents.
        """
        topo_order = self.topological_sort()

        for course in topo_order:
            course.compute_grade(alpha)

    def validate(self) -> None:
        """Validates the graph by checking for cycles via a trial topological sort."""
        self.topological_sort()

    def topological_sort(self) -> list[Course]:
        """
        Performs a Kahn's Algorithm topological sort on the graph.
        
        Returns:
            A list of Course objects in a mathematically safe evaluation order.
        
        Raises:
            ValueError: If a cycle is detected (e.g., Course A depends on Course B, 
                       and Course B depends on Course A).
        """
        # Track number of incoming edges for each node
        in_degree = {c: len(c.prerequisites) for c in self.courses.values()}
        queue: deque[Course] = deque()

        # Nodes with 0 prerequisites can be processed immediately
        for course, deg in in_degree.items():
            if deg == 0:
                queue.append(course)

        topo_order: list[Course] = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)

            # Reduce the dependency count for all courses that require this one
            for dependent in node.dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # If not all nodes were sorted, there must be a cycle
        if len(topo_order) != len(self.courses):
            raise ValueError("Graph contains a cycle - curriculum structure is invalid")

        return topo_order
