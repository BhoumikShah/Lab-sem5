import math

def triangle_area(a, b, c):
    s = (a + b + c) / 2
    if s <= a or s <= b or s <= c:
        return "Invalid triangle sides"
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

if __name__ == '__main__':
    try:
        a = float(input("Enter side a: "))
        b = float(input("Enter side b: "))
        c = float(input("Enter side c: "))
        print(f"Area of triangle is: {triangle_area(a, b, c)}")
    except ValueError:
        print("Please enter valid numbers.")
