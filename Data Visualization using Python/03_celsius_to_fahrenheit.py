def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

if __name__ == '__main__':
    try:
        c = float(input("Enter temperature in Celsius: "))
        print(f"{c}C is {celsius_to_fahrenheit(c)}F")
    except ValueError:
        print("Please enter a valid number.")
