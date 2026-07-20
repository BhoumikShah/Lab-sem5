# Day Number to Day Name
def day_name(num):
    days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    return days.get(num, 'Invalid day number')

if __name__ == '__main__':
    try:
        num = int(input("Enter day number (1-7): "))
        print(f"Day {num} is {day_name(num)}")
    except ValueError:
        print("Please enter a valid integer.")
