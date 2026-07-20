/* -----------------------------------------------------
 * Program: Orphan Process
 * An orphan process is a child process whose parent has
 * terminated before the child finishes execution.
 * The orphan is then adopted by the "init" (or subreaper)
 * process, which becomes its new parent (PPID becomes 1
 * or the id of the adopting process).
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed!\n");
        exit(1);
    } else if (pid > 0) {
        /* Parent process: exits quickly, leaving the child orphaned */
        printf("[Parent PID:%d] Parent process terminating...\n", getpid());
        exit(0);
    } else {
        /* Child process: sleeps, so the parent finishes first */
        sleep(2); /* give parent time to exit */
        printf("[Child  PID:%d] My original Parent PID: %d\n", getpid(), getppid());
        sleep(2); /* sleep again to check parent PID after adoption */
        printf("[Child  PID:%d] Now I am an ORPHAN. New Parent PID: %d\n", getpid(), getppid());
    }

    return 0;
}
