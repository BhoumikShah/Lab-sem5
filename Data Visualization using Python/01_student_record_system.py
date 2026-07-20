# Student Record System (Lists & Dictionaries)
students = []

def add_student(roll_no, name, marks):
    student = {'roll_no': roll_no, 'name': name, 'marks': marks}
    students.append(student)
    print(f"Student {name} added.")

def display_students():
    print("\n--- Student Records ---")
    for s in students:
        print(s)

if __name__ == '__main__':
    while True:
        try:
            roll_no = int(input("Enter Roll No (or 0 to stop): "))
            if roll_no == 0: break
            name = input("Enter Name: ")
            marks = float(input("Enter Marks: "))
            add_student(roll_no, name, marks)
        except ValueError:
            print("Invalid input, please enter valid numbers.")
    display_students()
