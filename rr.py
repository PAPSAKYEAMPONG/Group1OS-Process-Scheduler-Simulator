from collections import deque

# =====================================================
# ROUND ROBIN CPU SCHEDULING
# =====================================================
# Round Robin is a CPU scheduling algorithm where each
# process gets a small amount of CPU time (time quantum).
# If a process needs more time, it goes to the back of
# the queue. This ensures all processes get fair CPU time.
# =====================================================

def round_robin(processes, time_quantum):
    """
    Implement Round Robin CPU scheduling algorithm.
    
    Args:
        processes: List of process objects with attributes:
                   - pid: Process ID
                   - arrival: Time when process arrives
                   - burst: Total CPU time needed
                   - remaining: CPU time still needed
        time_quantum: Maximum CPU time slice each process gets
    
    Returns:
        gantt: List of tuples (process_id, start_time, end_time)
               showing when each process executed
    """
    # Current time in the simulation
    time = 0
    # Gantt chart: records when each process runs
    gantt = []
    # Queue to hold processes waiting for CPU
    queue = deque()
    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival)
    # Total number of processes
    n = len(processes)
    # Count of completed processes
    completed = 0

    # Track which processes have arrived (to avoid adding them twice)
    arrived = [False] * n

    # Keep scheduling until all processes are completed
    while completed < n:
        # Check if any new processes have arrived at the current time
        for i, p in enumerate(processes):
            if p.arrival <= time and not arrived[i]:
                queue.append(p)  # Add arrived process to the queue
                arrived[i] = True  # Mark as arrived

        # If no processes are ready, skip to next time unit
        if not queue:
            time += 1
            continue

        # Get the first process from the queue
        current = queue.popleft()

        # Record when this process starts execution
        start = time
        # Execute for time_quantum or until process is done (whichever is less)
        execute_time = min(current.remaining, time_quantum)
        time += execute_time
        # Reduce remaining time for this process
        current.remaining -= execute_time
        # Record when this execution ends
        end = time

        # Add to gantt chart: which process ran and when
        gantt.append((current.pid, start, end))

        # Check if any more processes arrived while current was executing
        for i, p in enumerate(processes):
            if p.arrival > start and p.arrival <= time and not arrived[i]:
                queue.append(p)  # Add to queue
                arrived[i] = True

        # If process still needs more CPU time, put it back in the queue
        if current.remaining > 0:
            queue.append(current)
        else:
            # Process is done! Calculate its metrics
            current.completion = time  # When it finished
            current.turnaround = current.completion - current.arrival  # Total time in system
            current.waiting = current.turnaround - current.burst  # Time spent waiting
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
        self.completion = 0      # Time when process finishes (set later)
        self.turnaround = 0      # Total time in system (set later)
        self.waiting = 0         # Time spent waiting (set later)

# Create some sample processes
processes = [
    Process(1, 0, 8),    # P1: arrives at 0, needs 8 units of CPU time
    Process(2, 1, 4),    # P2: arrives at 1, needs 4 units of CPU time
    Process(3, 2, 2),    # P3: arrives at 2, needs 2 units of CPU time
]

# Time quantum: each process gets 3 units of CPU time per turn
time_quantum = 3

# Run the algorithm
gantt_chart = round_robin(processes, time_quantum)

# Print results
print("\n" + "="*70)
print("ROUND ROBIN CPU SCHEDULING - RESULTS")
print("="*70)

print("\nGantt Chart (Process execution order on CPU):")
print("-" * 70)
for process_id, start, end in gantt_chart:
    print(f"  P{process_id}: {start} - {end}")

print("\nProcess Details:")
print("-" * 70)
print(f"{'PID':<5} {'Arrival':<10} {'Burst':<8} {'Completion':<12} {'Turnaround':<12} {'Waiting':<10}")
print("-" * 70)
for p in processes:
    print(f"P{p.pid:<4} {p.arrival:<10} {p.burst:<8} {p.completion:<12} {p.turnaround:<12} {p.waiting:<10}")

print("="*70 + "\n")
