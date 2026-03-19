from grade_engine import GradeEngine

def main() -> None:
    # alpha: float = float(input("Enter the alpha factor: "))
    alpha: float = 0.7

    engine = GradeEngine(alpha)
    engine.print_cgpa()

if __name__ == "__main__":
    main()
