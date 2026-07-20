/* -----------------------------------------------------
 * Program: Readers-Writers Problem (using Semaphores & Threads)
 * Readers-preference solution:
 *   - Multiple readers can read simultaneously.
 *   - Writers require exclusive access.
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

sem_t mutex;    /* protects access to read_count */
sem_t wrt;      /* ensures exclusive access for writers */
int read_count = 0;
int shared_data = 0;

void *reader(void *arg) {
    int id = *(int *) arg;

    sem_wait(&mutex);
    read_count++;
    if (read_count == 1)
        sem_wait(&wrt); /* first reader locks out writers */
    sem_post(&mutex);

    /* ---- Critical section: reading ---- */
    printf("[Reader %d] Reading shared_data = %d\n", id, shared_data);
    sleep(1);
    /* ------------------------------------ */

    sem_wait(&mutex);
    read_count--;
    if (read_count == 0)
        sem_post(&wrt); /* last reader unlocks writers */
    sem_post(&mutex);

    free(arg);
    return NULL;
}

void *writer(void *arg) {
    int id = *(int *) arg;

    sem_wait(&wrt); /* exclusive access */

    /* ---- Critical section: writing ---- */
    shared_data += 10;
    printf("[Writer %d] Writing shared_data = %d\n", id, shared_data);
    sleep(1);
    /* ------------------------------------ */

    sem_post(&wrt);

    free(arg);
    return NULL;
}

int main() {
    int num_readers, num_writers;
    printf("Enter number of readers: ");
    scanf("%d", &num_readers);
    printf("Enter number of writers: ");
    scanf("%d", &num_writers);

    sem_init(&mutex, 0, 1);
    sem_init(&wrt, 0, 1);

    pthread_t readers[num_readers], writers[num_writers];

    /* Create readers and writers, interleaved */
    for (int i = 0; i < num_readers || i < num_writers; i++) {
        if (i < num_readers) {
            int *id = malloc(sizeof(int));
            *id = i + 1;
            pthread_create(&readers[i], NULL, reader, id);
        }
        if (i < num_writers) {
            int *id = malloc(sizeof(int));
            *id = i + 1;
            pthread_create(&writers[i], NULL, writer, id);
        }
    }

    for (int i = 0; i < num_readers; i++)
        pthread_join(readers[i], NULL);
    for (int i = 0; i < num_writers; i++)
        pthread_join(writers[i], NULL);

    sem_destroy(&mutex);
    sem_destroy(&wrt);

    printf("\nFinal value of shared_data = %d\n", shared_data);

    return 0;
}
