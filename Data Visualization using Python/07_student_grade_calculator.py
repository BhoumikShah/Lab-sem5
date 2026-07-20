# Student Grade Calculator
def calculate_grade(marks):
    if marks >= 90: return 'A'
    elif marks >= 80: return 'B'
    elif marks >= 70: return 'C'
    elif marks >= 60: return 'D'
    else: return 'F'

if __name__ == '__main__':
    try:
        marks = float(input("Enter student marks (0-100): "))
        if 0 <= marks <= 100:
            print(f"Marks: {marks}, Grade: {calculate_grade(marks)}")
        else:
            print("Marks must be between 0 and 100.")
    except ValueError:
        print("Please enter a valid number.")
