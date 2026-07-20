# File Operations (Read/Write/Append together)
def all_operations(filename, initial_text, append_text):
    # Write
    print("\nWriting...")
    with open(filename, 'w') as f:
        f.write(initial_text + "\n")
    
    # Append
    print("Appending...")
    with open(filename, 'a') as f:
        f.write(append_text + "\n")
        
    # Read
    print("Reading file back...")
    with open(filename, 'r') as f:
        print(f.read())

if __name__ == '__main__':
    filename = input("Enter filename (e.g. full_ops.txt): ")
    initial = input("Enter initial text to write: ")
    append = input("Enter text to append: ")
    all_operations(filename, initial, append)
