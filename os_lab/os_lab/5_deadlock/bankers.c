/* -----------------------------------------------------
 * Program: Banker's Algorithm for Deadlock Avoidance
 * ----------------------------------------------------- */
#include <stdio.h>

#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int n, m; /* n = number of processes, m = number of resource types */
int allocation[MAX_PROCESSES][MAX_RESOURCES];
int max_demand[MAX_PROCESSES][MAX_RESOURCES];
int need[MAX_PROCESSES][MAX_RESOURCES];
int available[MAX_RESOURCES];

void calculateNeed() {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            need[i][j] = max_demand[i][j] - allocation[i][j];
}

/* Checks whether the system is in a safe state.
   If safe, prints the safe sequence and returns 1, else returns 0. */
int isSafeState() {
    int work[MAX_RESOURCES];
    int finish[MAX_PROCESSES] = {0};
    int safe_sequence[MAX_PROCESSES];
    int count = 0;

    for (int j = 0; j < m; j++)
        work[j] = available[j];

    while (count < n) {
        int found = 0;

        for (int i = 0; i < n; i++) {
            if (!finish[i]) {
                int can_allocate = 1;
                for (int j = 0; j < m; j++) {
                    if (need[i][j] > work[j]) {
                        can_allocate = 0;
                        break;
                    }
                }

                if (can_allocate) {
                    /* Process i can finish; release its resources back to work */
                    for (int j = 0; j < m; j++)
                        work[j] += allocation[i][j];

                    safe_sequence[count++] = i;
                    finish[i] = 1;
                    found = 1;
                }
            }
        }

        if (!found) {
            /* No process could be allocated resources; system is NOT safe */
            printf("\nSystem is in an UNSAFE state. Deadlock may occur.\n");
            return 0;
        }
    }

    printf("\nSystem is in a SAFE state.\n");
    printf("Safe Sequence: ");
    for (int i = 0; i < n; i++) {
        printf("P%d", safe_sequence[i]);
        if (i != n - 1) printf(" -> ");
    }
    printf("\n");
    return 1;
}

/* Attempts to process a resource request from process pid.
   Returns 1 if the request can be safely granted, 0 otherwise. */
int requestResources(int pid, int request[]) {
    for (int j = 0; j < m; j++) {
        if (request[j] > need[pid][j]) {
            printf("Error: Process has exceeded its maximum claim.\n");
            return 0;
        }
        if (request[j] > available[j]) {
            printf("Process must wait; resources are not available.\n");
            return 0;
        }
    }

    /* Tentatively allocate the requested resources */
    for (int j = 0; j < m; j++) {
        available[j] -= request[j];
        allocation[pid][j] += request[j];
        need[pid][j] -= request[j];
    }

    if (isSafeState()) {
        printf("Request granted immediately.\n");
        return 1;
    } else {
        /* Roll back if unsafe */
        for (int j = 0; j < m; j++) {
            available[j] += request[j];
            allocation[pid][j] -= request[j];
            need[pid][j] += request[j];
        }
        printf("Request denied; would leave system in an unsafe state.\n");
        return 0;
    }
}

int main() {
    printf("Enter number of processes: ");
    scanf("%d", &n);
    printf("Enter number of resource types: ");
    scanf("%d", &m);

    printf("\nEnter Allocation matrix (%d x %d):\n", n, m);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &allocation[i][j]);

    printf("\nEnter Maximum Demand matrix (%d x %d):\n", n, m);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &max_demand[i][j]);

    printf("\nEnter Available resources vector (%d values):\n", m);
    for (int j = 0; j < m; j++)
        scanf("%d", &available[j]);

    calculateNeed();

    printf("\nNeed Matrix:\n");
    for (int i = 0; i < n; i++) {
        printf("P%d: ", i);
        for (int j = 0; j < m; j++)
            printf("%d ", need[i][j]);
        printf("\n");
    }

    isSafeState();

    /* Optional: demonstrate a resource request */
    int choice;
    printf("\nDo you want to test a resource request? (1=Yes, 0=No): ");
    scanf("%d", &choice);

    if (choice == 1) {
        int pid, request[MAX_RESOURCES];
        printf("Enter process ID (0 to %d): ", n - 1);
        scanf("%d", &pid);
        printf("Enter request vector (%d values): ", m);
        for (int j = 0; j < m; j++)
            scanf("%d", &request[j]);

        requestResources(pid, request);
    }

    return 0;
}
