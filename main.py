from grade_engine import GradeEngine

def main() -> None:
    # alpha: float = float(input("Enter the alpha factor: "))
    alpha: float = 0.7

    engine = GradeEngine(alpha)
    cgpa = engine.get_cgpa()
    print(f"CGPA : {cgpa:.2f}")
    engine.print_course_details("CS1106")  # Testing on Data Structures

if __name__ == "__main__":
    main()
