/* -----------------------------------------------------
 * Program: Fork - Parent sorts ascending, Child sorts descending
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

void bubbleSortAscending(int arr[], int n) {
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
}

void bubbleSortDescending(int arr[], int n) {
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] < arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int n;
    printf("Enter number of elements: ");
    fflush(stdout);
    scanf("%d", &n);

    int arr[n];
    printf("Enter %d elements: ", n);
    fflush(stdout);
    for (int i = 0; i < n; i++)
        scanf("%d", &arr[i]);
    fflush(stdout); /* ensure buffer is clear before fork so it isn't duplicated */

    /* Make separate copies so parent and child work independently */
    int arr_parent[n], arr_child[n];
    for (int i = 0; i < n; i++) {
        arr_parent[i] = arr[i];
        arr_child[i] = arr[i];
    }

    pid_t pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed!\n");
        exit(1);
    } else if (pid == 0) {
        /* Child process: sort descending */
        bubbleSortDescending(arr_child, n);
        printf("[Child  PID:%d] Descending order: ", getpid());
        printArray(arr_child, n);
        exit(0);
    } else {
        /* Parent process: sort ascending */
        wait(NULL); /* wait for child to finish so output is not interleaved */
        bubbleSortAscending(arr_parent, n);
        printf("[Parent PID:%d] Ascending order:  ", getpid());
        printArray(arr_parent, n);
    }

    return 0;
}
