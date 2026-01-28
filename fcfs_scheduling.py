"""
First-Come-First-Serve (FCFS) CPU Scheduling Algorithm
This program implements a simple FCFS scheduler for an Operating Systems project.
FCFS means: the process that arrives first gets scheduled first on the CPU.
"""

def fcfs_scheduling(processes):
    """
    Implements the FCFS (First-Come-First-Serve) CPU scheduling algorithm.
    
    Parameters:
    -----------
    processes : list of dictionaries
        Each dictionary represents a process with:
        - 'pid': Process ID (e.g., 'P1', 'P2')
        - 'arrival_time': When the process arrives in the CPU queue
        - 'burst_time': How long the process needs to run on the CPU
        
    Returns:
    --------
    A dictionary containing:
    - 'processes': List of processes with calculated scheduling metrics
    - 'gantt_chart': List of tuples (PID, start_time, end_time)
    - 'avg_waiting_time': Average waiting time across all processes
    - 'avg_turnaround_time': Average turnaround time across all processes
    - 'cpu_utilization': Percentage of time CPU was busy
    """
    
    # Step 1: Sort processes by arrival time (FCFS rule - first to arrive goes first)
    sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])
    
    # Step 2: Initialize variables to store scheduling information
    current_time = 0  # This tracks the current CPU time
    gantt_chart = []  # Will store (PID, start_time, end_time) for visualization
    
    # Step 3: Process each process in arrival order
    for process in sorted_processes:
        pid = process['pid']
        arrival_time = process['arrival_time']
        burst_time = process['burst_time']
        
        # Step 4: Handle CPU idle time
        # If current_time < arrival_time, the CPU is idle (no process ready)
        # In FCFS, we wait for the next process to arrive
        if current_time < arrival_time:
            current_time = arrival_time
        
        # Step 5: Calculate scheduling metrics for this process
        start_time = current_time
        completion_time = current_time + burst_time
        waiting_time = start_time - arrival_time
        turnaround_time = completion_time - arrival_time
        
        # Step 6: Store the results in the process dictionary
        process['start_time'] = start_time
        process['completion_time'] = completion_time
        process['waiting_time'] = waiting_time
        process['turnaround_time'] = turnaround_time
        
        # Step 7: Add this process to the Gantt chart
        gantt_chart.append((pid, start_time, completion_time))
        
        # Step 8: Update current_time for the next process
        current_time = completion_time
    
    # Step 9: Calculate average metrics
    total_waiting_time = sum(p['waiting_time'] for p in sorted_processes)
    total_turnaround_time = sum(p['turnaround_time'] for p in sorted_processes)
    num_processes = len(sorted_processes)
    
    avg_waiting_time = total_waiting_time / num_processes if num_processes > 0 else 0
    avg_turnaround_time = total_turnaround_time / num_processes if num_processes > 0 else 0
    
    # Step 10: Calculate CPU Utilization
    # CPU Utilization = (Total Burst Time) / (Total Time from first arrival to last completion)
    total_burst_time = sum(p['burst_time'] for p in sorted_processes)
    total_time = current_time - sorted_processes[0]['arrival_time'] if sorted_processes else 0
    
    if total_time > 0:
        cpu_utilization = (total_burst_time / total_time) * 100
    else:
        cpu_utilization = 0
    
    # Step 11: Prepare and return the results
    results = {
        'processes': sorted_processes,
        'gantt_chart': gantt_chart,
        'avg_waiting_time': avg_waiting_time,
        'avg_turnaround_time': avg_turnaround_time,
        'cpu_utilization': cpu_utilization
    }
    
    return results


def print_results(results):
    """
    Helper function to print the scheduling results in a readable format.
    This makes it easy to see the output without writing print statements separately.
    
    Parameters:
    -----------
    results : dictionary
        The results returned from fcfs_scheduling() function
    """
    
    print("\n" + "="*70)
    print("FCFS CPU SCHEDULING - DETAILED RESULTS")
    print("="*70)
    
    # Print process details in a table format
    print("\nProcess Details:")
    print("-" * 70)
    print(f"{'PID':<5} {'Arrival':<10} {'Burst':<8} {'Start':<8} {'Completion':<12} {'Waiting':<10} {'Turnaround':<12}")
    print("-" * 70)
    
    for process in results['processes']:
        print(f"{process['pid']:<5} {process['arrival_time']:<10} {process['burst_time']:<8} "
              f"{process['start_time']:<8} {process['completion_time']:<12} "
              f"{process['waiting_time']:<10} {process['turnaround_time']:<12}")
    
    # Print Gantt Chart
    print("\nGantt Chart (Process execution order on CPU):")
    print("-" * 70)
    gantt_visual = " | ".join([f"{pid}({start}-{end})" 
                                for pid, start, end in results['gantt_chart']])
    print(gantt_visual)
    
    # Print timing data
    print(f"\nGantt Chart Data (for visualization):")
    print("-" * 70)
    for pid, start, end in results['gantt_chart']:
        print(f"  Process {pid}: starts at {start}, ends at {end}")
    
    # Print average metrics
    print("\nPerformance Metrics:")
    print("-" * 70)
    print(f"Average Waiting Time:      {results['avg_waiting_time']:.2f} time units")
    print(f"Average Turnaround Time:   {results['avg_turnaround_time']:.2f} time units")
    print(f"CPU Utilization:           {results['cpu_utilization']:.2f}%")
    print("="*70 + "\n")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

# Example: Basic example with 3 processes
print("\nExample 1: Basic FCFS Scheduling")
processes_example1 = [
    {'pid': 'P1', 'arrival_time': 0, 'burst_time': 8},
    {'pid': 'P2', 'arrival_time': 1, 'burst_time': 4},
    {'pid': 'P3', 'arrival_time': 2, 'burst_time': 2},
]

results1 = fcfs_scheduling(processes_example1)
print_results(results1)
