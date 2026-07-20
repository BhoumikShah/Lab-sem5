/* -----------------------------------------------------
 * Program: Zombie Process
 * A zombie process is a child process that has completed
 * execution but still has an entry in the process table
 * because its parent has not yet read its exit status
 * (has not called wait()/waitpid()).
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed!\n");
        exit(1);
    } else if (pid == 0) {
        /* Child process: exits immediately */
        printf("[Child  PID:%d] Child process exiting now.\n", getpid());
        exit(0);
    } else {
        /* Parent process: deliberately delays calling wait(),
           so the child becomes a zombie in the meantime */
        printf("[Parent PID:%d] Child PID:%d has exited but parent has not called wait() yet.\n", getpid(), pid);
        printf("[Parent PID:%d] Check 'ps -el' or 'ps aux' now - Child should show state 'Z' (zombie).\n", getpid());

        sleep(10); /* window during which the child remains a zombie */

        printf("[Parent PID:%d] Now calling wait() to clean up the zombie...\n", getpid());
        wait(NULL);
        printf("[Parent PID:%d] Zombie process reaped successfully.\n", getpid());
    }

    return 0;
}
