from grade_engine import GradeEngine

def main() -> None:
    # alpha: float = float(input("Enter the alpha factor: "))
    alpha: float = 0.7

    engine = GradeEngine(alpha)
    
    running: bool = True
    while running:
        print("\n" + "-" * 50)
        print("1. Get CGPA")
        print("2. Get CGPA up to a certain year/semester")
        print("3. Get course details")
        print("4. Exit")
        print("-" * 50)
        
        choice: str = input("Enter your choice: ")
        
        if choice == "1":
            cgpa = engine.get_cgpa()
            print(f"CGPA : {cgpa:.2f}")
        elif choice == "2":
            year: str = input("Enter year (leave empty for overall): ")
            semester: str = input("Enter semester (leave empty for overall): ")
            
            if year and semester:
                cgpa = engine.get_cgpa(up_to_year=int(year), up_to_semester=int(semester))
                print(f"CGPA up to Year {year}, Semester {semester}: {cgpa:.2f}")
            elif year:
                cgpa = engine.get_cgpa(up_to_year=int(year))
                print(f"CGPA up to Year {year}: {cgpa:.2f}")
            elif semester:
                cgpa = engine.get_cgpa(up_to_semester=int(semester))
                print(f"CGPA up to Semester {semester}: {cgpa:.2f}")
            else:
                cgpa = engine.get_cgpa()
                print(f"Overall CGPA: {cgpa:.2f}")
        elif choice == "3":
            course_identifier: str = input("Enter course ID or name: ")
            engine.print_course_details(course_identifier)
        elif choice == "4":
            running = False
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
