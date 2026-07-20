# Income Tax Calculator
def calculate_tax(income):
    if income <= 250000:
        return 0
    elif income <= 500000:
        return (income - 250000) * 0.05
    else:
        return (250000 * 0.05) + ((income - 500000) * 0.1)

if __name__ == '__main__':
    try:
        income = float(input("Enter annual income: "))
        print(f"Tax for income {income} is {calculate_tax(income)}")
    except ValueError:
        print("Please enter a valid number.")
