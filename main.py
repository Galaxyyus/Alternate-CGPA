from grade_engine import GradeEngine


def main() -> None:
    alpha: float = 0.3

    course_file = "course.json"
    score_file = "score.json"

    engine = GradeEngine(alpha, course_file, score_file)

    running: bool = True
    while running:
        print("\n" + "-" * 50)
        print(f"Data Source: {course_file} / {score_file}")
        print("-" * 50)
        print("1. Get Grade up to a certain year/semester")
        print("2. Get course details")
        print("3. Calculate Old CGPA")
        print("4. Switch Data Source")
        print("5. Exit")
        print("-" * 50)

        choice: str = input("Enter your choice: ")

        if choice == "1":
            year_input: str = input("Enter year (leave empty for overall): ")
            semester_input: str = input("Enter semester (leave empty for overall): ")

            up_to_year = int(year_input) if year_input.strip() else None
            up_to_semester = int(semester_input) if semester_input.strip() else None

            if up_to_semester and up_to_year:
                print("Invalid Input! Enter only one field.")
                continue

            grade = engine.get_grade(up_to_year=up_to_year, up_to_semester=up_to_semester)

            msg = "Overall Grade"
            if up_to_year:
                msg = f"Grade up to Year {up_to_year}"
            elif up_to_semester:
                msg = f"Grade up to Semester {up_to_semester}"

            print(f"{msg}: {grade:.2f}")

        elif choice == "2":
            course_identifier: str = input("Enter course ID or name: ")
            engine.print_course_details(course_identifier)
        elif choice == "3":
            year_input: str = input("Enter year (leave empty for overall): ")
            semester_input: str = input("Enter semester (leave empty for overall): ")

            up_to_year = int(year_input) if year_input.strip() else None
            up_to_semester = int(semester_input) if semester_input.strip() else None

            if up_to_semester and up_to_year:
                print("Invalid Input! Enter only one field.")
                continue

            old_cgpa = engine.get_old_cgpa(up_to_year=up_to_year, up_to_semester=up_to_semester)
            print(f"Old CGPA: {old_cgpa:.2f}")
        elif choice == "4":
            if course_file == "course.json":
                course_file, score_file = "course_alt.json", "score_alt.json"
            else:
                course_file, score_file = "course.json", "score.json"

            print(f"Switching to {course_file} and {score_file}...")
            engine = GradeEngine(alpha, course_file, score_file)
        elif choice == "5":
            running = False
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
