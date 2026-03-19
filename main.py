from graphs import build_graph_from_file
# from scoring import GradeEngine


def main():
    alpha: float = float(input("Enter the alpha factor: "))

    graph = build_graph_from_file("courses.txt")
    graph.compute(alpha)

    selected = [
        graph.courses["Algorithms"],
        graph.courses["Probability"],
    ]

    total = sum(course.grade for course in selected)
    cgpa = total / len(selected)

    print(f"CGPA : {cgpa:.2f}")

    print(selected[0])
    print(selected[1])


if __name__ == "__main__":
    main()
