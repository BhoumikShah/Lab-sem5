/* -----------------------------------------------------
 * Program: SRTF (Shortest Remaining Time First) - Preemptive
 * CPU Scheduling Algorithm
 * ----------------------------------------------------- */
#include <stdio.h>
#include <limits.h>

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int remaining_time;
    int completion_time;
    int turnaround_time;
    int waiting_time;
    int is_completed;
};

int main() {
    int n;
    printf("Enter number of processes: ");
    scanf("%d", &n);

    struct Process p[n];

    for (int i = 0; i < n; i++) {
        p[i].pid = i + 1;
        printf("Enter arrival time and burst time for Process %d: ", p[i].pid);
        scanf("%d %d", &p[i].arrival_time, &p[i].burst_time);
        p[i].remaining_time = p[i].burst_time;
        p[i].is_completed = 0;
    }

    int current_time = 0, completed = 0;
    float total_waiting_time = 0, total_turnaround_time = 0;

    printf("\nGantt Chart (process executed each time unit):\n");

    while (completed < n) {
        int shortest = -1;
        int min_remaining = INT_MAX;

        /* Find the process with the shortest remaining time among arrived processes */
        for (int i = 0; i < n; i++) {
            if (p[i].arrival_time <= current_time && !p[i].is_completed &&
                p[i].remaining_time < min_remaining) {
                min_remaining = p[i].remaining_time;
                shortest = i;
            }
        }

        if (shortest == -1) {
            /* No process has arrived yet, CPU is idle */
            printf("Time %d: [IDLE]\n", current_time);
            current_time++;
            continue;
        }

        printf("Time %d: P%d (remaining=%d)\n", current_time, p[shortest].pid, p[shortest].remaining_time);

        p[shortest].remaining_time--;
        current_time++;

        if (p[shortest].remaining_time == 0) {
            p[shortest].is_completed = 1;
            completed++;
            p[shortest].completion_time = current_time;
            p[shortest].turnaround_time = p[shortest].completion_time - p[shortest].arrival_time;
            p[shortest].waiting_time = p[shortest].turnaround_time - p[shortest].burst_time;

            total_waiting_time += p[shortest].waiting_time;
            total_turnaround_time += p[shortest].turnaround_time;
        }
    }

    printf("\nProcess\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n");
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t\t%d\t\t%d\n",
               p[i].pid, p[i].arrival_time, p[i].burst_time,
               p[i].completion_time, p[i].turnaround_time, p[i].waiting_time);
    }

    printf("\nAverage Waiting Time    = %.2f\n", total_waiting_time / n);
    printf("Average Turnaround Time = %.2f\n", total_turnaround_time / n);

    return 0;
}
