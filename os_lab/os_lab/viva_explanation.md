# OS Lab Viva Preparation Guide (Labs 1, 2 & 3)

This document contains quick summaries, line-by-line code explanations, and common viva questions for Labs 1, 2, and 3.

---

## 📁 Lab 1: Shell Scripting

### 📄 File: [arithmetic.sh](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/1_shell/arithmetic.sh)

#### 💡 Quick Summary
This script is a command-line menu-driven program written in Bash. It takes two integers as input from the user and performs arithmetic operations (Addition, Subtraction, Multiplication, Division, Modulus, or all at once) based on a menu choice using a `case` statement. It also includes error handling for division/modulus by zero.

#### 🔍 Line-by-Line Explanation
* **Line 1 (`#!/bin/bash`):** The **Shebang** line. Tells the OS to interpret/run this script using the Bash shell located at `/bin/bash`.
* **Line 6-9 (`echo "Enter first number:" ... read num1 ...`):** Prompts the user and reads input variables `num1` and `num2` from standard input.
* **Line 11-21 (`echo ... read choice`):** Displays a menu of available arithmetic operations (1 to 6) and reads the user's selection into the `choice` variable.
* **Line 23 (`case $choice in`):** Begins a `case` block (similar to a `switch` statement in C) matching the `choice` variable.
* **Line 24-27 (`1) result=$((num1 + num2)) ... ;;`):** If the choice is `1`, performs addition using `$(( ... ))` (arithmetic expansion) and prints the result. `;;` acts as a case break.
* **Line 28-35 (`2)` and `3)`):** Subtraction and multiplication options using `$((num1 - num2))` and `$((num1 * num2))`.
* **Line 36-43 (`4) if [ $num2 -eq 0 ]; ... else ... fi ;;`):** Checks if the second number is equal (`-eq`) to `0` to prevent division-by-zero runtime errors. Performs division if safe.
* **Line 44-51 (`5) if [ $num2 -eq 0 ]; ... else ... fi ;;`):** Similar check for Modulus (`%`) by zero safety.
* **Line 52-62 (`6) ...`):** Choice to perform all operations at once. Checks divisor safety before printing division and modulo.
* **Line 63-65 (`*) ...`):** Wildcard matching. Prints an invalid choice error if the input is outside 1-6.
* **Line 66 (`esac`):** Ends the `case` block.

#### 🗣️ Core Viva Questions
1. **What is the Shebang line?**
   * *Answer:* It specifies the interpreter (e.g. `/bin/bash`) to parse and run the script.
2. **What does `$(( ... ))` do?**
   * *Answer:* It performs integer arithmetic expansion in Bash.
3. **What does `-eq` stand for?**
   * *Answer:* It stands for "equal to", used for numerical comparisons in Bash.

---

## 📁 Lab 2: Process Control

### 📄 File 1: [fork_sort.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/2_process_control/fork_sort.c)

#### 💡 Quick Summary
Demonstrates process creation. The program duplicates an integer array and invokes `fork()`. The child process sorts its copy in descending order, while the parent waits for it and then sorts its copy in ascending order.

#### 🔍 Line-by-Line Explanation
* **Line 2-5:** Header inclusions: standard input/output (`stdio.h`), helper utilities (`stdlib.h`), POSIX API headers (`unistd.h`), and process wait control (`sys/wait.h`).
* **Line 7-15 (`bubbleSortAscending`):** Function to sort an array in ascending order using standard Bubble Sort.
* **Line 17-25 (`bubbleSortDescending`):** Function to sort an array in descending order.
* **Line 27-31 (`printArray`):** Prints array elements sequentially.
* **Line 33-44:** Reads number of elements `n` and array values. `fflush(stdout)` clears standard output buffers to prevent duplicate outputs across the fork boundary.
* **Line 47-51:** Allocates and populates two identical arrays `arr_parent` and `arr_child` so that the processes work independently.
* **Line 53 (`pid_t pid = fork();`):** Spawns a child process. `fork()` returns `0` in the child process, the child's PID in the parent process, and a negative number if it fails.
* **Line 55-57:** Checks if `fork()` failed and exits if it did.
* **Line 58-63:** **Child Process block** (triggered when `pid == 0`). Sorts `arr_child` in descending order, prints it with its PID (`getpid()`), and terminates via `exit(0)`.
* **Line 64-70:** **Parent Process block** (triggered when `pid > 0`). Calls `wait(NULL)` to pause execution until the child terminates. Then sorts `arr_parent` in ascending order and prints it.

---

### 📄 File 2: [orphan.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/2_process_control/orphan.c)

#### 💡 Quick Summary
Demonstrates an orphan process. The parent process exits immediately, leaving the child running. The child is subsequently adopted by the init process (`init` or `systemd`).

#### 🔍 Line-by-Line Explanation
* **Line 7:** Calls `fork()` to create a child process.
* **Line 9-11:** Errors out if `fork()` fails.
* **Line 12-14:** **Parent Process block** (`pid > 0`). Prints its PID and exits immediately using `exit(0)`.
* **Line 15-20:** **Child Process block** (`pid == 0`). Sleeps for 2 seconds (`sleep(2)`) to give the parent time to exit. Once it wakes up, it queries its parent's PID using `getppid()`. Since the original parent has died, it prints the PID of the adoption process (usually `1` or a user-session manager).

---

### 📄 File 3: [zombie.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/2_process_control/zombie.c)

#### 💡 Quick Summary
Demonstrates a zombie (defunct) process. The child exits immediately, but the parent sleeps for 10 seconds without calling `wait()`, keeping the terminated child in the system's process table.

#### 🔍 Line-by-Line Explanation
* **Line 7:** Spawns a child process.
* **Line 12-15:** **Child Process block** (`pid == 0`). Prints a termination message and exits immediately using `exit(0)`.
* **Line 16-25:** **Parent Process block** (`pid > 0`). Prints instructions to check `ps -el` or `ps aux` to view the child in a zombie status (`Z`). It sleeps for 10 seconds (`sleep(10)`), during which the child remains a zombie. Afterward, it calls `wait(NULL)`, which reaps the child process and removes it from the process table.

#### 🗣️ Core Viva Questions
1. **What is a Zombie Process?**
   * *Answer:* A process that has finished execution but still has an entry in the process table because its parent hasn't reaped it via `wait()`.
2. **What is an Orphan Process?**
   * *Answer:* A process whose parent has terminated, causing it to be adopted by PID 1 (`init`) or another system process.
3. **What is the purpose of `wait(NULL)`?**
   * *Answer:* It blocks the parent process until one of its child processes exits, retrieving its exit status and reclaiming system resources.

---

## 📁 Lab 3: CPU Scheduling

### 📄 File 1: [fcfs.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/3_scheduling/fcfs.c)

#### 💡 Quick Summary
Implements the First-Come, First-Served (FCFS) non-preemptive CPU scheduling algorithm. Processes are sorted by arrival time and executed in that sequence.

#### 🔍 Line-by-Line Explanation
* **Line 4-11 (`struct Process`):** Defines process properties: PID, arrival time, burst time, completion time, turnaround time, and waiting time.
* **Line 20-24:** Collects arrival and burst times for `n` processes.
* **Line 26-32:** Sorts the process array in ascending order of arrival time using a simple Bubble Sort.
* **Line 34:** Sets `current_time` to 0.
* **Line 37-48:** Loops through the sorted processes:
  * **Line 38-39:** If the CPU is idle (i.e. `current_time < arrival_time`), fast-forwards the clock to the process's arrival time.
  * **Line 41-44:** Adds burst time to `current_time` to set Completion Time (`completion_time`). Computes Turnaround Time ($TAT = CT - AT$) and Waiting Time ($WT = TAT - BT$).
  * **Line 46-47:** Sums up waiting and turnaround times for average calculation.
* **Line 50-58:** Prints metrics table and calculates averages.

---

### 📄 File 2: [srtf.c](file:///c:/Users/Asus/Documents/GitHub/Lab/os_lab/os_lab/3_scheduling/srtf.c)

#### 💡 Quick Summary
Implements the preemptive Shortest Remaining Time First (SRTF) algorithm. At every time unit, the scheduler picks the process with the shortest remaining execution time.

#### 🔍 Line-by-Line Explanation
* **Line 5-14 (`struct Process`):** Includes `remaining_time` and `is_completed` tracking.
* **Line 27-28:** Initializes `remaining_time` to the full `burst_time` and `is_completed` flag to `0`.
* **Line 36 (`while (completed < n)`):** Loops unit-by-unit until all `n` processes are complete.
* **Line 37-46:** Scans all arrived processes to find the one with the smallest remaining burst time.
* **Line 48-52:** If no process has arrived, increments `current_time` (CPU idle time).
* **Line 54-57:** Prints execution step, decrements the active process's `remaining_time` by `1`, and increments `current_time` by `1`.
* **Line 59-68:** When `remaining_time == 0`, marks it complete, sets Completion Time ($CT = current\_time$), and computes Turnaround Time ($TAT = CT - AT$) and Waiting Time ($WT = TAT - BT$).
* **Line 71-79:** Prints final stats and averages.

#### 🗣️ Core Viva Questions
1. **State the formulas for Turnaround Time and Waiting Time.**
   * *Answer:* $TAT = Completion\ Time - Arrival\ Time$; $Waiting\ Time = Turnaround\ Time - Burst\ Time$.
2. **Why is SRTF called preemptive?**
   * *Answer:* If a new process arrives with a shorter remaining burst time than the currently running process, the current process is suspended (preempted) and the new one starts running.
3. **What is the Convoy Effect?**
   * *Answer:* A phenomenon in FCFS where short processes wait a long time behind a large process that arrived first, reducing CPU efficiency.
