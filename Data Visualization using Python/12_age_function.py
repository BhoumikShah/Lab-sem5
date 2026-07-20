import datetime

def calculate_age(birth_year):
    current_year = datetime.datetime.now().year
    return current_year - birth_year

if __name__ == '__main__':
    try:
        birth_year = int(input("Enter your birth year: "))
        print(f"Your age is approximately {calculate_age(birth_year)} years.")
    except ValueError:
        print("Please enter a valid year.")
