def check_clearance(user):
    if user == 'admin':
        return 'granted'
    else:
        return 'denied'
def check_password_strength(password):
    if len(password) < 8:
        return 'Weak: Too short (min 8 chars)'
    if not any(char.isdigit() for char in password):
        return 'Weak: Needs numbers'
    if not any(char.isupper() for char in password):
        return 'Weak: Needs uppercase letter'
    return 'Strong'

if __name__ == '__main__':
    password = input("Enter a password to check its strength: ")
    user=input("admin or user")
    print(f"Strength: {check_password_strength(password)}")
    print(f"Acess: {check_clearance(user)}")


