/* -----------------------------------------------------
 * Program: Inter-Process Communication using SHARED MEMORY
 * Parent writes a message into a shared memory segment;
 * Child reads it, and writes back a reply which the
 * parent then reads.
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define SHM_SIZE 1024

int main() {
    /* Create a shared memory segment */
    int shmid = shmget(IPC_PRIVATE, SHM_SIZE, IPC_CREAT | 0666);
    if (shmid < 0) {
        fprintf(stderr, "shmget failed!\n");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed!\n");
        exit(1);
    } else if (pid == 0) {
        /* ---------------- Child process ---------------- */
        sleep(1); /* small delay to ensure parent writes first */

        char *shm = (char *) shmat(shmid, NULL, 0);
        if (shm == (char *) -1) {
            fprintf(stderr, "shmat failed in child!\n");
            exit(1);
        }

        printf("[Child] Read from shared memory: %s\n", shm);

        /* Overwrite shared memory with a reply for the parent */
        char reply[] = "Hello Parent, Child has read your message!";
        memset(shm, 0, SHM_SIZE);
        strcpy(shm, reply);

        shmdt(shm); /* detach */
        exit(0);
    } else {
        /* ---------------- Parent process ---------------- */
        char *shm = (char *) shmat(shmid, NULL, 0);
        if (shm == (char *) -1) {
            fprintf(stderr, "shmat failed in parent!\n");
            exit(1);
        }

        char message[] = "Hello Child, this is Parent writing via shared memory!";
        strcpy(shm, message);

        wait(NULL); /* wait for child to read and overwrite */

        printf("[Parent] Read from shared memory: %s\n", shm);

        shmdt(shm); /* detach */
        shmctl(shmid, IPC_RMID, NULL); /* destroy shared memory segment */
    }

    return 0;
}
