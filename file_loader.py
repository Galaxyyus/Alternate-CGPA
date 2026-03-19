import json
from graphs import CourseGraph


def load_courses_structure(filename: str) -> CourseGraph:
    with open(filename, "r") as f:
        data = json.load(f)

    graph = CourseGraph()

    courses_data = data["courses"]
    years_data = data["years"]

    # Create all courses node
    for course_id, info in courses_data.items():
        name = info["name"]
        graph.add_course(course_id, name)

    # Add Dependencies
    for course_id, info in courses_data.items():
        for prereq_id in info["prerequisites"]:
            if prereq_id not in courses_data:
                raise ValueError(f"Invalid prerequisite {prereq_id} for {course_id}")
            graph.add_dependency(prereq_id, course_id)

    # Attack semester and year metadata
    for year, semesters in years_data.items():
        for semester, course_ids in semesters.items():
            for cid in course_ids:
                if cid not in courses_data:
                    raise ValueError(
                        f"{cid} listed in semester {semester}, year {year} but not defined in courses section."
                    )
                graph.courses[cid].year = int(year)
                graph.courses[cid].semester = int(semester)

    graph.validate()
    return graph


def load_grades(filename: str, graph: CourseGraph) -> None:
    with open(filename, "r") as f:
        grades = json.load(f)

    for course_id, score in grades.items():
        if course_id not in graph.courses:
            raise ValueError(f"Grade for unknown course {course_id}")

        graph.courses[course_id].raw_score = score
