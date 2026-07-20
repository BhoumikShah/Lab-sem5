# File Read
def read_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print("\n--- File content ---")
            print(content)
    except FileNotFoundError:
        print("File not found.")

if __name__ == '__main__':
    filename = input("Enter filename to read (e.g. sample.txt): ")
    # Create a dummy file if user types sample.txt and it doesn't exist just for demo
    try:
        with open(filename, 'x') as f: f.write("Dummy content for " + filename)
    except FileExistsError:
        pass
    read_file(filename)
