# Operating Systems Lab Programs

All programs have been written, compiled, and tested on Ubuntu (gcc 13.3.0).

## Folder Structure

```
os_lab/
├── 1_shell/
│   └── arithmetic.sh              # Shell scripting - arithmetic operations
├── 2_process_control/
│   ├── fork_sort.c                # fork(): parent sorts ascending, child sorts descending
│   ├── orphan.c                   # Orphan process demonstration
│   └── zombie.c                   # Zombie process demonstration
├── 3_scheduling/
│   ├── fcfs.c                     # FCFS (Non-preemptive) CPU scheduling
│   └── srtf.c                     # SRTF (Preemptive) CPU scheduling
├── 4_ipc/
│   ├── pipe_ipc.c                 # IPC using pipes
│   └── shared_memory.c            # IPC using shared memory (System V shm)
├── 5_deadlock/
│   └── bankers.c                  # Banker's Algorithm for deadlock avoidance
├── 6_semaphore/
│   ├── readers_writers.c          # Readers-Writers problem (pthreads + semaphores)
│   └── producer_consumer.c        # Producer-Consumer problem (bounded buffer)
└── 7_paging/
    └── page_replacement.c         # FIFO and LRU page replacement algorithms
```

## How to Compile and Run

### 1. Shell Script
```bash
chmod +x arithmetic.sh
./arithmetic.sh
```

### 2. Process Control
```bash
gcc -o fork_sort fork_sort.c && ./fork_sort
gcc -o orphan orphan.c && ./orphan
gcc -o zombie zombie.c && ./zombie
# While zombie is running (within its 10-second sleep window), open another
# terminal and run `ps -el` or `ps aux` — you will see the child in 'Z' state.
```

### 3. CPU Scheduling
```bash
gcc -o fcfs fcfs.c && ./fcfs
gcc -o srtf srtf.c && ./srtf
```
Sample input for both (4 processes, arrival & burst time pairs):
```
4
0 5
1 3
2 8
3 6
```

### 4. IPC
```bash
gcc -o pipe_ipc pipe_ipc.c && ./pipe_ipc
gcc -o shared_memory shared_memory.c && ./shared_memory
```

### 5. Banker's Algorithm
```bash
gcc -o bankers bankers.c && ./bankers
```
Classic textbook test input (5 processes, 3 resource types):
```
5
3
0 1 0
2 0 0
3 0 2
2 1 1
0 0 2
7 5 3
3 2 2
9 0 2
2 2 2
4 3 3
3 3 2
```
Expected safe sequence: P1 -> P3 -> P4 -> P0 -> P2

### 6. Semaphores (requires pthread library)
```bash
gcc -o readers_writers readers_writers.c -lpthread && ./readers_writers
gcc -o producer_consumer producer_consumer.c -lpthread && ./producer_consumer
```

### 7. Page Replacement
```bash
gcc -o page_replacement page_replacement.c && ./page_replacement
```
Classic test input (reference string, 3 frames):
```
20
7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
3
```
Expected: FIFO = 15 faults, LRU = 12 faults

## Notes
- All C programs were compiled with `gcc` and tested for correct output.
- `readers_writers.c` and `producer_consumer.c` use POSIX threads and semaphores;
  compile with `-lpthread`.
- `shared_memory.c` uses System V shared memory APIs (`shmget`, `shmat`, `shmdt`, `shmctl`).
  You can inspect active segments with `ipcs -m` while the program is paused,
  or if it's interrupted before cleanup, remove a segment manually with
  `ipcrm -m <shmid>`.
