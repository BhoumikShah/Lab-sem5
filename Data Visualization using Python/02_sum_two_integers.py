def sum_two(a, b):
    return a + b

if __name__ == '__main__':
    try:
        a = int(input("Enter first integer: "))
        b = int(input("Enter second integer: "))
        print(f"Sum of {a} and {b} is {sum_two(a, b)}")
    except ValueError:
        print("Please enter valid integers.")
