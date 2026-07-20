/* -----------------------------------------------------
 * Program: Page Replacement Algorithms - FIFO and LRU
 * ----------------------------------------------------- */
#include <stdio.h>

#define MAX_FRAMES 10
#define MAX_PAGES 50

int isPresent(int frames[], int frame_count, int page) {
    for (int i = 0; i < frame_count; i++)
        if (frames[i] == page)
            return 1;
    return 0;
}

/* ---------------- FIFO Page Replacement ---------------- */
void fifo(int pages[], int n, int capacity) {
    int frames[MAX_FRAMES];
    int frame_count = 0;
    int front = 0; /* points to oldest frame (for replacement) */
    int page_faults = 0;

    printf("\n--- FIFO Page Replacement ---\n");

    for (int i = 0; i < n; i++) {
        int page = pages[i];

        if (!isPresent(frames, frame_count, page)) {
            page_faults++;
            if (frame_count < capacity) {
                frames[frame_count++] = page;
            } else {
                frames[front] = page;
                front = (front + 1) % capacity;
            }
            printf("Page %d -> FAULT   | Frames: ", page);
        } else {
            printf("Page %d -> HIT     | Frames: ", page);
        }

        for (int j = 0; j < frame_count; j++)
            printf("%d ", frames[j]);
        printf("\n");
    }

    printf("Total Page Faults (FIFO) = %d\n", page_faults);
}

/* ---------------- LRU Page Replacement ---------------- */
void lru(int pages[], int n, int capacity) {
    int frames[MAX_FRAMES];
    int last_used[MAX_FRAMES]; /* tracks the last-used "time" for each frame */
    int frame_count = 0;
    int page_faults = 0;

    printf("\n--- LRU Page Replacement ---\n");

    for (int i = 0; i < n; i++) {
        int page = pages[i];
        int found = -1;

        for (int j = 0; j < frame_count; j++)
            if (frames[j] == page) {
                found = j;
                break;
            }

        if (found == -1) {
            /* Page fault */
            page_faults++;
            if (frame_count < capacity) {
                frames[frame_count] = page;
                last_used[frame_count] = i;
                frame_count++;
            } else {
                /* Find the least recently used frame */
                int lru_index = 0;
                for (int j = 1; j < capacity; j++)
                    if (last_used[j] < last_used[lru_index])
                        lru_index = j;

                frames[lru_index] = page;
                last_used[lru_index] = i;
            }
            printf("Page %d -> FAULT   | Frames: ", page);
        } else {
            /* Page hit: update its last-used time */
            last_used[found] = i;
            printf("Page %d -> HIT     | Frames: ", page);
        }

        for (int j = 0; j < frame_count; j++)
            printf("%d ", frames[j]);
        printf("\n");
    }

    printf("Total Page Faults (LRU) = %d\n", page_faults);
}

int main() {
    int n, capacity;
    int pages[MAX_PAGES];

    printf("Enter number of pages in the reference string: ");
    scanf("%d", &n);

    printf("Enter the page reference string: ");
    for (int i = 0; i < n; i++)
        scanf("%d", &pages[i]);

    printf("Enter number of frames: ");
    scanf("%d", &capacity);

    fifo(pages, n, capacity);
    lru(pages, n, capacity);

    return 0;
}
