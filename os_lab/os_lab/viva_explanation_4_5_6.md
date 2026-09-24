# OS Lab Viva Preparation Guide (Labs 4, 5 & 6)

This document contains detailed summaries, line-by-line code explanations, and comprehensive viva questions for **Lab 4 (IPC)**, **Lab 5 (Deadlock Avoidance / Banker's Algorithm)**, and **Lab 6 (Process Synchronization & Semaphores)**.

---

## 📁 Lab 4: Inter-Process Communication (IPC)

---

### 📄 File 1: [pipe_ipc.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/4_ipc/pipe_ipc.c)

#### 💡 Quick Summary
Demonstrates **bidirectional (full-duplex) communication** between a Parent and Child process using **two unidirectional anonymous pipes**:
1. `parent_to_child`: Parent writes a message, Child reads it.
2. `child_to_parent`: Child writes a reply, Parent reads it.

#### 🔍 Line-by-Line Explanation
* **Line 6–10:** Inclusions of required headers:
  - `<stdio.h>`, `<stdlib.h>`, `<string.h>`: Basic I/O and string functions.
  - `<unistd.h>`: Declares `pipe()`, `fork()`, `read()`, `write()`, and `close()`.
  - `<sys/wait.h>`: Declares `wait()`.
* **Line 12 (`#define MSG_SIZE 100`):** Defines max buffer size for messages.
* **Line 15–16:** Declares two integer arrays `parent_to_child[2]` and `child_to_parent[2]`. For any pipe `fd[2]`, `fd[0]` is read-end and `fd[1]` is write-end.
* **Line 19–22 (`pipe(...)`):** Calls `pipe()` on both arrays to create two kernel FIFO buffers. If either call returns `-1`, exits with error.
* **Line 24 (`pid_t pid = fork();`):** Duplicates the current process. Both parent and child inherit copies of the file descriptors.
* **Line 26–28:** Error check if `fork()` returns `< 0`.
* **Line 29–43: Child Process (`pid == 0`):**
  - **Line 31–32:** `close(parent_to_child[1]); close(child_to_parent[0]);` — Crucial step: closes unused write-end of input pipe and unused read-end of output pipe.
  - **Line 34–35:** `read(parent_to_child[0], read_msg, MSG_SIZE);` — Reads parent's message from pipe and prints it.
  - **Line 37–38:** `write(child_to_parent[1], write_msg, strlen(write_msg) + 1);` — Writes response into child-to-parent pipe.
  - **Line 40–42:** Closes remaining active descriptors and exits cleanly with `exit(0)`.
* **Line 44–58: Parent Process (`pid > 0`):**
  - **Line 45–46:** `close(parent_to_child[0]); close(child_to_parent[1]);` — Closes unused read-end of input pipe and write-end of reply pipe.
  - **Line 48–49:** `write(parent_to_child[1], write_msg, strlen(write_msg) + 1);` — Writes parent message into pipe.
  - **Line 51 (`wait(NULL);`):** Pauses parent until the child process finishes execution.
  - **Line 53–54:** `read(child_to_parent[0], read_msg, MSG_SIZE);` — Reads the reply sent by the child.
  - **Line 56–57:** Closes remaining open ends.

#### 🗣️ Core Viva Questions & Answers
1. **Why do we need two pipes instead of one for two-way communication?**
   - *Answer:* Standard anonymous pipes in UNIX are strictly **unidirectional (half-duplex)**. If a single pipe is used for both reading and writing, the parent might read its own message before the child gets a chance to read it.
2. **What does `pipe(int fd[2])` return, and which index is for what?**
   - *Answer:* Returns `0` on success and `-1` on failure. `fd[0]` is the **Read end**, and `fd[1]` is the **Write end**.
3. **What happens if a process calls `read()` on an empty pipe?**
   - *Answer:* If at least one write descriptor for that pipe remains open, `read()` **blocks** until data is available. If all write ends are closed, `read()` returns `0` (EOF).
4. **Why is it essential to close unused pipe descriptors?**
   - *Answer:* It prevents resource/file descriptor leaks and ensures that reader processes can detect End-Of-File (EOF) when writer processes finish.

---

### 📄 File 2: [shared_memory.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/4_ipc/shared_memory.c)

#### 💡 Quick Summary
Demonstrates **System V Shared Memory IPC**. A shared memory segment is created using `shmget()`. The parent writes a message into the segment, the child attaches to it via `shmat()`, reads the message, writes back a reply, and the parent reads the reply and deletes the segment with `shmctl()`.

#### 🔍 Line-by-Line Explanation
* **Line 7–13:** Includes IPC headers: `<sys/ipc.h>` and `<sys/shm.h>` for System V shared memory APIs.
* **Line 15 (`#define SHM_SIZE 1024`):** Sets segment size to 1 KB.
* **Line 19 (`shmget(...)`):**
  - `IPC_PRIVATE`: Guarantees creation of a new, private shared memory segment accessible to parent and children.
  - `SHM_SIZE`: Size in bytes.
  - `IPC_CREAT | 0666`: Creates segment if it doesn't exist with octal read/write permissions (`0666`) for user, group, and others.
* **Line 25 (`fork()`):** Creates child process.
* **Line 31–49: Child Process:**
  - **Line 32 (`sleep(1);`):** Brief pause to ensure the parent writes its message first.
  - **Line 34 (`shmat(shmid, NULL, 0)`):** **Attaches** shared memory segment to child's address space. Returns a `char *` pointer to the allocated memory.
  - **Line 40:** Reads and prints data at `shm` pointer.
  - **Line 44–45:** Overwrites the shared memory segment with child's reply.
  - **Line 47 (`shmdt(shm);`):** **Detaches** the shared memory segment from the child process.
* **Line 50–66: Parent Process:**
  - **Line 51 (`shmat(...)`):** Attaches segment to parent's address space.
  - **Line 58 (`strcpy(shm, message);`):** Writes initial message directly to shared RAM.
  - **Line 60 (`wait(NULL);`):** Waits for child to finish reading and overwriting.
  - **Line 62:** Reads child's reply from `shm`.
  - **Line 64 (`shmdt(shm);`):** Detaches segment from parent.
  - **Line 65 (`shmctl(shmid, IPC_RMID, NULL);`):** Deallocates and destroys the shared memory segment (`IPC_RMID`) from system RAM.

#### 🗣️ Core Viva Questions & Answers
1. **Why is Shared Memory the fastest IPC mechanism?**
   - *Answer:* Unlike pipes or message queues, data does not pass through the kernel buffer. Once mapped, processes read and write directly to physical RAM without context switching or system call overhead on each read/write.
2. **What is the difference between `shmdt()` and `shmctl(..., IPC_RMID, ...)`?**
   - *Answer:* `shmdt()` simply **detaches** the segment from the calling process's address space (segment still exists). `shmctl(..., IPC_RMID)` **permanently destroys and deallocates** the memory segment from the operating system.
3. **What is the main challenge with Shared Memory?**
   - *Answer:* Synchronization. Since multiple processes can write simultaneously, race conditions can occur unless synchronized using locks/semaphores.

---

## 📁 Lab 5: Deadlock Avoidance (Banker's Algorithm)

---

### 📄 File: [bankers.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/5_deadlock/bankers.c)

#### 💡 Quick Summary
Implements **Dijkstra's Banker's Algorithm** for Deadlock Avoidance. It calculates the **Need Matrix**, verifies if the system is currently in a **Safe State** (by discovering a valid Safe Sequence), and tests dynamic **Resource Requests** using tentative allocation and rollback mechanisms.

#### 🔍 Line-by-Line Explanation
* **Line 6–13:** Defines limits and data structures:
  - `allocation[n][m]`: Resources currently held by processes.
  - `max_demand[n][m]`: Maximum resource demand declared by each process.
  - `need[n][m]`: Remaining resources needed ($Need = Max - Allocation$).
  - `available[m]`: Number of free instances of each resource.
* **Line 15–19 (`calculateNeed()`):** Computes $Need[i][j] = max\_demand[i][j] - allocation[i][j]$ for all processes $i$ and resources $j$.
* **Line 23–72 (`isSafeState()`):**
  - **Line 24–30:** Initializes `work` vector to `available` and `finish[i] = 0` (all incomplete).
  - **Line 32 (`while (count < n)`):** Loops until all processes complete or no further process can be satisfied.
  - **Line 35–43:** Searches for an uncompleted process $i$ (`!finish[i]`) where $Need[i][j] \le Work[j]$ for all $j$.
  - **Line 45–53:** If found, simulates process completion: adds $Allocation[i][j]$ to $Work[j]$, adds $i$ to `safe_sequence`, marks `finish[i] = 1`, and increments `count`.
  - **Line 57–61:** If no process could be satisfied in a full iteration (`!found`), system is in an **UNSAFE state** (returns `0`).
  - **Line 64–71:** If all processes finish (`count == n`), prints the **Safe Sequence** and returns `1`.
* **Line 76–108 (`requestResources(pid, request[])`):**
  - **Line 77–86:** Safety checks:
    1. If $Request[j] > Need[pid][j] \implies$ Error: Process exceeded maximum claim.
    2. If $Request[j] > Available[j] \implies$ Process must wait (insufficient resources).
  - **Line 89–93:** **Tentative Allocation**:
    - $Available[j] -= Request[j]$
    - $Allocation[pid][j] += Request[j]$
    - $Need[pid][j] -= Request[j]$
  - **Line 95–98:** Calls `isSafeState()`. If safe, request is granted immediately.
  - **Line 99–106:** If unsafe, **rolls back** (reverts) the allocation changes and denies the request.
* **Line 110–159 (`main()`):** Takes user inputs for matrices, runs safety check, and optionally simulates a resource request.

#### 🗣️ Core Viva Questions & Answers
1. **What are the 4 Coffman conditions required for a Deadlock to occur?**
   - *Answer:*
     1. **Mutual Exclusion**: At least one resource must be held in a non-shareable mode.
     2. **Hold and Wait**: A process holds resources while waiting for additional ones.
     3. **No Preemption**: Resources cannot be forcibly taken from a process.
     4. **Circular Wait**: A closed chain of processes exists where each waits for a resource held by the next.
2. **What is the difference between Deadlock Prevention and Deadlock Avoidance?**
   - *Answer:*
     - **Prevention:** Imposes static constraints so that at least one of the 4 Coffman conditions can mathematically never occur.
     - **Avoidance:** Allows all conditions dynamically, but evaluates every resource request on-the-fly (e.g., Banker's algorithm) to guarantee the system stays in a Safe State.
3. **Is an Unsafe State always a Deadlocked State?**
   - *Answer:* No! An unsafe state is not necessarily deadlocked. It simply means the OS cannot guarantee avoiding a deadlock if all processes simultaneously demand their maximum resource claims.
4. **Why is the algorithm called "Banker's" Algorithm?**
   - *Answer:* Because it is modeled after a bank that never allocates cash in a way that it cannot satisfy the maximum cash requirements of all customers eventually.

---

## 📁 Lab 6: Process Synchronization & Semaphores

---

### 📄 File 1: [producer_consumer.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/6_semaphore/producer_consumer.c)

#### 💡 Quick Summary
Solves the classic **Bounded Buffer (Producer-Consumer) Problem** using POSIX threads (`pthread`) and POSIX semaphores (`semaphore.h`). Prevents buffer overflow, buffer underflow, and race conditions on the circular buffer index.

#### 🔍 Line-by-Line Explanation
* **Line 8–9:** Inclusions: `<pthread.h>` (threads) and `<semaphore.h>` (semaphores).
* **Line 11 (`#define BUFFER_SIZE 5`):** Fixed circular buffer capacity.
* **Line 13–14:** `int buffer[5]; int in = 0, out = 0;` — Shared storage and circular indices.
* **Line 16–18: Semaphores:**
  - `sem_t empty`: Counting semaphore tracking available empty slots.
  - `sem_t full`: Counting semaphore tracking filled slots with items.
  - `sem_t mutex`: Binary semaphore (value 1) providing mutual exclusion when accessing `buffer`.
* **Line 22–39: Producer Thread (`producer`):**
  - **Line 26 (`sem_wait(&empty);`):** Decrements `empty`. Blocks if buffer is full (`empty == 0`).
  - **Line 27 (`sem_wait(&mutex);`):** Acquires lock for critical section.
  - **Line 29–31:** Inserts item at `buffer[in]` and advances `in = (in + 1) % BUFFER_SIZE`.
  - **Line 33 (`sem_post(&mutex);`):** Releases critical section lock.
  - **Line 34 (`sem_post(&full);`):** Increments `full` (signals waiting consumer).
* **Line 41–56: Consumer Thread (`consumer`):**
  - **Line 43 (`sem_wait(&full);`):** Decrements `full`. Blocks if buffer is empty (`full == 0`).
  - **Line 44 (`sem_wait(&mutex);`):** Acquires lock for critical section.
  - **Line 46–48:** Retrieves item from `buffer[out]` and advances `out = (out + 1) % BUFFER_SIZE`.
  - **Line 50 (`sem_post(&mutex);`):** Releases lock.
  - **Line 51 (`sem_post(&empty);`):** Increments `empty` (signals waiting producer).
* **Line 58–81: Main Function:**
  - **Line 62–64 (`sem_init`):**
    - `sem_init(&empty, 0, BUFFER_SIZE)`: Initializes `empty = 5`.
    - `sem_init(&full, 0, 0)`: Initializes `full = 0`.
    - `sem_init(&mutex, 0, 1)`: Initializes `mutex = 1`.
  - **Line 68–69:** `pthread_create(...)` spawns producer and consumer threads.
  - **Line 71–72:** `pthread_join(...)` waits for both threads to finish.
  - **Line 74–76:** `sem_destroy(...)` frees semaphore resources.

#### 🗣️ Core Viva Questions & Answers
1. **What happens if you swap the order of `sem_wait(&empty)` and `sem_wait(&mutex)` in Producer?**
   - *Answer:* It causes a **DEADLOCK**. If the buffer is full and producer locks `mutex` first, it will block on `sem_wait(&empty)` while holding `mutex`. The consumer will then block on `sem_wait(&mutex)` and can never consume items to free space.
2. **What does the second argument `0` in `sem_init(&sem, 0, value)` mean?**
   - *Answer:* It indicates that the semaphore is shared between **threads of the same process**. If non-zero, it would be shared between different processes.
3. **What is the mathematical meaning of `(in + 1) % BUFFER_SIZE`?**
   - *Answer:* It creates a **circular array/queue**, wrapping the index back to `0` when it reaches `BUFFER_SIZE`.

---

### 📄 File 2: [readers_writers.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/6_semaphore/readers_writers.c)

#### 💡 Quick Summary
Implements the **First Readers-Writers Problem (Readers Preference)** using threads and semaphores:
- Any number of readers can read the shared variable concurrently.
- Writers require strict exclusive access (no other reader or writer allowed).

#### 🔍 Line-by-Line Explanation
* **Line 13–16: Synchronization variables:**
  - `sem_t mutex`: Protects access to the integer counter `read_count` (initialized to 1).
  - `sem_t wrt`: Protects the shared critical section variable `shared_data` for writers (initialized to 1).
  - `int read_count = 0`: Number of readers currently reading.
  - `int shared_data = 0`: Shared resource being read/written.
* **Line 18–40: Reader Thread (`reader`):**
  - **Line 21–25 (Entry Section):**
    - `sem_wait(&mutex);`
    - `read_count++;`
    - `if (read_count == 1) sem_wait(&wrt);` $\rightarrow$ The **very first reader** locks `wrt`, preventing any writer from writing.
    - `sem_post(&mutex);`
  - **Line 28–30 (Critical Section):** Reads `shared_data`. (Multiple readers execute this concurrently).
  - **Line 32–36 (Exit Section):**
    - `sem_wait(&mutex);`
    - `read_count--;`
    - `if (read_count == 0) sem_post(&wrt);` $\rightarrow$ The **last reader** releases `wrt`, allowing waiting writers to proceed.
    - `sem_post(&mutex);`
* **Line 42–57: Writer Thread (`writer`):**
  - **Line 45 (`sem_wait(&wrt);`):** Requests exclusive lock. Blocks if any reader is reading or another writer is writing.
  - **Line 48–50:** Modifies `shared_data += 10`.
  - **Line 53 (`sem_post(&wrt);`):** Releases exclusive lock.
* **Line 59–96: Main Function:**
  - Initializes `mutex` and `wrt` to 1.
  - Creates reader and writer threads dynamically based on user input.
  - Joins all threads, destroys semaphores, and prints the final `shared_data`.

#### 🗣️ Core Viva Questions & Answers
1. **Why is this implementation called "Readers-Preference"?**
   - *Answer:* Because as long as at least one reader is active (`read_count > 0`), subsequent readers are immediately admitted to read without waiting, while writers are forced to wait.
2. **What problem does Readers-Preference cause?**
   - *Answer:* **Writer Starvation**. If a steady stream of readers arrives continuously, `read_count` never drops to 0, and writers may wait indefinitely.
3. **Why do we need `sem_wait(&mutex)` inside the reader function?**
   - *Answer:* To prevent race conditions on the shared variable `read_count` when multiple reader threads increment or decrement it concurrently.
4. **Why is the `-pthread` compiler flag necessary?**
   - *Answer:* `gcc program.c -pthread -o program` is necessary because POSIX Threads (`pthread`) and POSIX Semaphores are provided by an external system library (`libpthread`) that must be linked by the compiler.
