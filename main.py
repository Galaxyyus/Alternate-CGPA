from grade_engine import GradeEngine

def main() -> None:
    # alpha: float = float(input("Enter the alpha factor: "))
    alpha: float = 0.7
    
    course_file = "course.json"
    score_file = "score.json"

    engine = GradeEngine(alpha, course_file, score_file)
    
    running: bool = True
    while running:
        print("\n" + "-" * 50)
        print(f"Data Source: {course_file} / {score_file}")
        print("-" * 50)
        print("1. Get CGPA")
        print("2. Get CGPA up to a certain year/semester")
        print("3. Get course details")
        print("4. Switch Data Source")
        print("5. Exit")
        print("-" * 50)
        
        choice: str = input("Enter your choice: ")
        
        if choice == "1":
            cgpa = engine.get_cgpa()
            print(f"CGPA : {cgpa:.2f}")
        elif choice == "2":
            year_input: str = input("Enter year (leave empty for overall): ")
            semester_input: str = input("Enter semester (leave empty for overall): ")
            
            up_to_year = int(year_input) if year_input.strip() else None
            up_to_semester = int(semester_input) if semester_input.strip() else None
            
            cgpa = engine.get_cgpa(up_to_year=up_to_year, up_to_semester=up_to_semester)
            
            msg = "Overall CGPA"
            if up_to_year and up_to_semester:
                msg = f"CGPA up to Year {up_to_year}, Semester {up_to_semester}"
            elif up_to_year:
                msg = f"CGPA up to Year {up_to_year}"
            elif up_to_semester:
                msg = f"CGPA up to Semester {up_to_semester}"
            
            print(f"{msg}: {cgpa:.2f}")
                
        elif choice == "3":
            course_identifier: str = input("Enter course ID or name: ")
            engine.print_course_details(course_identifier)
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
