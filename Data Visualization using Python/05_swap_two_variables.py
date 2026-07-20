def swap(a, b):
    print(f"Before swap: a={a}, b={b}")
    a, b = b, a
    print(f"After swap: a={a}, b={b}")
    return a, b

if __name__ == '__main__':
    a = input("Enter first variable (a): ")
    b = input("Enter second variable (b): ")
    swap(a, b)
