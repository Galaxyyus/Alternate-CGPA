import json
from graphs import CourseGraph


def load_courses_structure(filename: str) -> CourseGraph:
    """
    Parses a curriculum JSON file to build the CourseGraph.
    
    The JSON should contain:
    - 'categories': Mapping of category names to weights.
    - 'courses': Detailed course info including names and prerequisite IDs.
    - 'years': Chronological mapping (Year -> Semester -> [Course IDs]).

    Args:
        filename: Path to the course structure JSON file.
        
    Returns:
        A fully hydrated CourseGraph with all dependencies and metadata.
    """
    with open(filename, "r") as f:
        data = json.load(f)

    # Initialize graph with category weights
    categories = data.get("categories", {})
    graph = CourseGraph(categories)

    courses_data = data["courses"]
    years_data = data["years"]

    # Step 1: Create all course nodes
    for course_id, info in courses_data.items():
        name = info["name"]
        category = info.get("category")
        graph.add_course(course_id, name, category)

    # Step 2: Establish Prerequisite/Dependent links
    for course_id, info in courses_data.items():
        for prereq_id in info["prerequisites"]:
            if prereq_id not in courses_data:
                raise ValueError(f"Invalid prerequisite {prereq_id} for {course_id}")
            graph.add_dependency(prereq_id, course_id)

    # Step 3: Attach chronological metadata (Year/Semester)
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
    """
    Loads student performance data from a grades JSON file into the graph.
    
    Args:
        filename: Path to the score/grade JSON file (CourseID -> RawScore).
        graph: The CourseGraph to hydrate with scores.
    """
    with open(filename, "r") as f:
        grades = json.load(f)

    for course_id, score in grades.items():
        if course_id not in graph.courses:
            raise ValueError(f"Grade for unknown course {course_id}")

        graph.courses[course_id].raw_score = score
