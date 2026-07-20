# File Write
def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Successfully wrote to {filename}")

if __name__ == '__main__':
    filename = input("Enter filename to write to (e.g. output.txt): ")
    content = input("Enter text to write: ")
    write_file(filename, content)
