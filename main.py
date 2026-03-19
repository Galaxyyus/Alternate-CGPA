from graphs import CourseGraph
from scoring import GradeEngine


def build_example_graph():
    graph = CourseGraph()

    # Bucket 1
    graph.add_course("Programming", 6)
    graph.add_course("Data Structures", 7)
    graph.add_course("Algorithms", 9)

    graph.add_dependency("Programming", "Data Structures")
    graph.add_dependency("Data Structures", "Algorithms")

    # Bucket 2
    graph.add_course("Calculus", 8)
    graph.add_course("Linear Algebra", 7)
    graph.add_course("Probability", 9)

    graph.add_dependency("Calculus", "Linear Algebra")
    graph.add_dependency("Linear Algebra", "Probability")

    # Bucket 3
    graph.add_course("Supervised Learning", 7)
    graph.add_course("Neural Networks", 8)
    graph.add_course("ML Deployment", 9)

    graph.add_dependency("Supervised Learning", "Neural Networks")
    graph.add_dependency("Neural Networks", "ML Deployment")

    # Cross-bucket dependency
    graph.add_dependency("Probability", "ML Deployment")

    return graph


def main():
    graph = build_example_graph()

    scorer = GradeEngine(graph, alpha=0.7)
    scorer.compute()

    # If you only want the first two independent buckets:
    # filter explicitly by name
    selected = [
        graph.courses["Algorithms"],
        graph.courses["Probability"],
    ]

    total = sum(course.effective_grade for course in selected)
    cgpa = total / len(selected)

    print(f"CGPA (Top 2 Buckets): {cgpa:.2f}")


if __name__ == "__main__":
    main()
