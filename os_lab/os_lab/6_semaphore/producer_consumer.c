/* -----------------------------------------------------
 * Program: Producer-Consumer Problem (Bounded Buffer)
 * using Semaphores & Threads
 * ----------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define BUFFER_SIZE 5

int buffer[BUFFER_SIZE];
int in = 0, out = 0;

sem_t empty; /* counts empty slots */
sem_t full;  /* counts full slots */
sem_t mutex; /* mutual exclusion for buffer access */

int items_to_produce;

void *producer(void *arg) {
    for (int i = 1; i <= items_to_produce; i++) {
        int item = i * 10; /* produced item */

        sem_wait(&empty);   /* wait for an empty slot */
        sem_wait(&mutex);   /* enter critical section */

        buffer[in] = item;
        printf("[Producer] Produced item %d at slot %d\n", item, in);
        in = (in + 1) % BUFFER_SIZE;

        sem_post(&mutex);   /* leave critical section */
        sem_post(&full);    /* signal a new full slot */

        usleep(300000); /* simulate production time */
    }
    return NULL;
}

void *consumer(void *arg) {
    for (int i = 1; i <= items_to_produce; i++) {
        sem_wait(&full);    /* wait for a full slot */
        sem_wait(&mutex);   /* enter critical section */

        int item = buffer[out];
        printf("[Consumer] Consumed item %d from slot %d\n", item, out);
        out = (out + 1) % BUFFER_SIZE;

        sem_post(&mutex);   /* leave critical section */
        sem_post(&empty);   /* signal a new empty slot */

        usleep(500000); /* simulate consumption time */
    }
    return NULL;
}

int main() {
    printf("Enter number of items to produce/consume: ");
    scanf("%d", &items_to_produce);

    sem_init(&empty, 0, BUFFER_SIZE); /* initially all slots are empty */
    sem_init(&full, 0, 0);            /* initially no slots are full */
    sem_init(&mutex, 0, 1);

    pthread_t prod_thread, cons_thread;

    pthread_create(&prod_thread, NULL, producer, NULL);
    pthread_create(&cons_thread, NULL, consumer, NULL);

    pthread_join(prod_thread, NULL);
    pthread_join(cons_thread, NULL);

    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&mutex);

    printf("\nAll items produced and consumed successfully.\n");

    return 0;
}
