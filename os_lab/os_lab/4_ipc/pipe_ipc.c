/* -----------------------------------------------------
 * Program: Inter-Process Communication using PIPE
 * Parent sends a message to Child through an unnamed pipe;
 * Child sends a reply back through a second pipe.
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define MSG_SIZE 100

int main() {
    int parent_to_child[2]; /* pipe: parent -> child */
    int child_to_parent[2]; /* pipe: child -> parent */
    char write_msg[MSG_SIZE], read_msg[MSG_SIZE];

    if (pipe(parent_to_child) == -1 || pipe(child_to_parent) == -1) {
        fprintf(stderr, "Pipe creation failed!\n");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed!\n");
        exit(1);
    } else if (pid == 0) {
        /* ---------------- Child process ---------------- */
        close(parent_to_child[1]); /* close unused write end */
        close(child_to_parent[0]); /* close unused read end */

        read(parent_to_child[0], read_msg, MSG_SIZE);
        printf("[Child] Received from Parent: %s\n", read_msg);

        strcpy(write_msg, "Hello Parent, message received!");
        write(child_to_parent[1], write_msg, strlen(write_msg) + 1);

        close(parent_to_child[0]);
        close(child_to_parent[1]);
        exit(0);
    } else {
        /* ---------------- Parent process ---------------- */
        close(parent_to_child[0]); /* close unused read end */
        close(child_to_parent[1]); /* close unused write end */

        strcpy(write_msg, "Hello Child, this is Parent!");
        write(parent_to_child[1], write_msg, strlen(write_msg) + 1);

        wait(NULL); /* wait for child to respond */

        read(child_to_parent[0], read_msg, MSG_SIZE);
        printf("[Parent] Received from Child: %s\n", read_msg);

        close(parent_to_child[1]);
        close(child_to_parent[0]);
    }

    return 0;
}
