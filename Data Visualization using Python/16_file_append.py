# File Append
def append_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + "\n")
    print(f"Successfully appended to {filename}")

if __name__ == '__main__':
    filename = input("Enter filename to append to (e.g. output.txt): ")
    content = input("Enter text to append: ")
    append_file(filename, content)
