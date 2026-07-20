# SORT Function
def custom_sort(arr):
    # Bubble sort implementation
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

if __name__ == '__main__':
    nums = input("Enter numbers to sort, separated by spaces: ")
    try:
        arr = [float(x) for x in nums.split()]
        print(f"Original array: {arr}")
        print(f"Sorted array: {custom_sort(arr)}")
    except ValueError:
        print("Please enter valid numbers only.")
