# =====================================================
# SHORTEST JOB FIRST (SJF) CPU SCHEDULING
# =====================================================
# SJF (Shortest Job First) is a scheduling algorithm where
# the process with the shortest burst time (CPU time needed)
# gets scheduled first.
#
# Two types:
# 1. NON-PREEMPTIVE: Once a process starts, it runs to
#    completion. Then the next shortest job starts.
# 2. PREEMPTIVE: If a shorter job arrives while a process
#    is running, it switches to that shorter job
#    (also called Shortest Remaining Time First - SRTF).
# =====================================================

def sjf_non_preemptive(processes):
    """
    Implement Non-Preemptive SJF CPU scheduling algorithm.
    
    In non-preemptive SJF, once a process starts executing,
    it runs to completion before the next process can start.
    The process with the shortest burst time is selected first.
    
    Args:
        processes: List of process objects with attributes:
                   - pid: Process ID
                   - arrival: Time when process arrives
                   - burst: Total CPU time needed
                   - completion: When process finishes (set to None initially)
    
    Returns:
        gantt: List of tuples (process_id, start_time, end_time)
               showing when each process executed
    """
    # Current time in the simulation
    time = 0
    # Count of processes that have completed
    completed = 0
    # Total number of processes
    n = len(processes)
    # Gantt chart: records when each process runs
    gantt = []

    # Keep scheduling until all processes are completed
    while completed < n:
        # Form ready queue: processes that have arrived and not completed
        ready_queue = [p for p in processes if p.arrival <= time and p.completion is None]

        # If no processes are ready, CPU is idle - skip to next time
        if not ready_queue:
            time += 1
            continue

        # Select the process with the shortest burst time
        current = min(ready_queue, key=lambda p: p.burst)

        # Record execution details
        start = time
        time += current.burst  # Add burst time to current time
        end = time

        # Calculate metrics for this completed process
        current.completion = end  # When it finished
        current.turnaround = current.completion - current.arrival  # Total time in system
        current.waiting = current.turnaround - current.burst  # Time spent waiting

        # Add to gantt chart
        gantt.append((current.pid, start, end))
        completed += 1

    return gantt


def sjf_preemptive(processes):
    """
    Implement Preemptive SJF CPU scheduling algorithm.
    Also known as Shortest Remaining Time First (SRTF).
    
    In preemptive SJF, if a process with shorter remaining
    time arrives, it can interrupt the currently running process.
    The process with the shortest remaining time is always selected.
    
    Args:
        processes: List of process objects with attributes:
                   - pid: Process ID
                   - arrival: Time when process arrives
                   - burst: Total CPU time needed
                   - remaining: CPU time still needed
                   - completion: When process finishes (set to None initially)
    
    Returns:
        gantt: List of tuples (process_id, start_time) showing
               when each process starts execution (for preemptive tracking)
    """
    # Current time in the simulation
    time = 0
    # Count of processes that have completed
    completed = 0
    # Total number of processes
    n = len(processes)
    # Gantt chart: records when each process runs
    gantt = []
    # Track which process is currently running
    current_process = None

    # Keep scheduling until all processes are completed
    while completed < n:
        # Form ready queue: processes that have arrived and still have work to do
        ready_queue = [p for p in processes if p.arrival <= time and p.remaining > 0]

        # If no processes are ready, CPU is idle - skip to next time
        if not ready_queue:
            time += 1
            continue

        # Select the process with the shortest remaining time
        shortest = min(ready_queue, key=lambda p: p.remaining)

        # If switching to a different process, record the context switch
        if current_process != shortest:
            gantt.append((shortest.pid, time))
            current_process = shortest

        # Execute for 1 time unit
        shortest.remaining -= 1
        time += 1

        # If process is done, calculate its metrics
        if shortest.remaining == 0:
            shortest.completion = time  # When it finished
            shortest.turnaround = shortest.completion - shortest.arrival  # Total time in system
            shortest.waiting = shortest.turnaround - shortest.burst  # Time spent waiting
            completed += 1

    return gantt


# =====================================================
# EXAMPLE USAGE
# =====================================================

class Process:
    """Simple process class with basic attributes."""
    def __init__(self, pid, arrival, burst):
        self.pid = pid           # Process ID
        self.arrival = arrival   # Time when process arrives
        self.burst = burst       # Total CPU time needed
        self.remaining = burst   # CPU time still needed (starts same as burst)
        self.completion = None   # Time when process finishes (set later)
        self.turnaround = 0      # Total time in system (set later)
        self.waiting = 0         # Time spent waiting (set later)

# Create some sample processes
processes_data = [
    Process(1, 0, 8),    # P1: arrives at 0, needs 8 units of CPU time
    Process(2, 1, 4),    # P2: arrives at 1, needs 4 units of CPU time
    Process(3, 2, 2),    # P3: arrives at 2, needs 2 units of CPU time
]

# Make copies for each algorithm (so we can test both)
import copy
processes_non_preempt = copy.deepcopy(processes_data)
processes_preempt = copy.deepcopy(processes_data)

print("\n" + "="*70)
print("SJF NON-PREEMPTIVE SCHEDULING")
print("="*70)
gantt_non_preempt = sjf_non_preemptive(processes_non_preempt)
print("\nGantt Chart (Process execution order):")
for pid, start, end in gantt_non_preempt:
    print(f"  P{pid}: {start} - {end}")

print("\nProcess Details:")
print(f"{'PID':<5} {'Arrival':<10} {'Burst':<8} {'Completion':<12} {'Turnaround':<12} {'Waiting':<10}")
for p in processes_non_preempt:
    print(f"P{p.pid:<4} {p.arrival:<10} {p.burst:<8} {p.completion:<12} {p.turnaround:<12} {p.waiting:<10}")

print("\n" + "="*70)
print("SJF PREEMPTIVE (SHORTEST REMAINING TIME FIRST)")
print("="*70)
gantt_preempt = sjf_preemptive(processes_preempt)
print("\nGantt Chart (Process context switches):")
for i, (pid, time) in enumerate(gantt_preempt):
    print(f"  Step {i+1}: P{pid} starts at time {time}")

print("\nProcess Details:")
print(f"{'PID':<5} {'Arrival':<10} {'Burst':<8} {'Completion':<12} {'Turnaround':<12} {'Waiting':<10}")
for p in processes_preempt:
    print(f"P{p.pid:<4} {p.arrival:<10} {p.burst:<8} {p.completion:<12} {p.turnaround:<12} {p.waiting:<10}")
print("="*70 + "\n")
