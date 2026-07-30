
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed!\n");
        exit(1);
    } else if (pid > 0) {
        printf("[Parent PID:%d] Parent process terminating...\n", getpid());
        exit(0);
    } else {
        sleep(2); 
        printf("[Child  PID:%d] My original Parent PID: %d\n", getpid(), getppid());
        sleep(2); 
        printf("[Child  PID:%d] Now I am an ORPHAN. New Parent PID: %d\n", getpid(), getppid());
    }

    return 0;
}
