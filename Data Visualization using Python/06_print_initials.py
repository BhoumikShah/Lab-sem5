def print_initials(name):
    initials = ''.join([part[0].upper() for part in name.split()])
    print(f"Initials for '{name}': {initials}")

if __name__ == '__main__':
    name = input("Enter full name: ")
    if name.strip():
        print_initials(name)
    else:
        print("Name cannot be empty.")
