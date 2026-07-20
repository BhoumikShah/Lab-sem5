# ALERT for Negative Numbers
def check_positive(numbers):
    for n in numbers:
        if n < 0:
            print(f"ALERT: Negative number detected: {n}")
        else:
            print(f"Number {n} is positive.")

if __name__ == '__main__':
    nums = input("Enter a list of numbers separated by spaces: ")
    try:
        numbers = [float(x) for x in nums.split()]
        check_positive(numbers)
    except ValueError:
        print("Please enter valid numbers only.")
