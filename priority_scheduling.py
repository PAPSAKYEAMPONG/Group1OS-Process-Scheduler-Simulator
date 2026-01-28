"""
Priority CPU Scheduling Algorithm
This program implements the Priority Scheduling algorithm in non-preemptive mode.

Key Concept:
- Priority Scheduling selects the process with the HIGHEST priority (lowest number)
- Among all ARRIVED processes, the CPU picks the one with the smallest priority value
- Once a process starts, it runs to completion (non-preemptive)
- Lower priority number = Higher priority (e.g 1 is higher priority than 2)

Example:
  Process A: Priority 2 (lower priority)
  Process B: Priority 1 (higher priority)
   Process B gets CPU first
"""


def priority_scheduling(processes):
    """
    Implements Priority Scheduling (non-preemptive mode).
    
    Args:
        processes: List of dictionaries with keys:
                   - 'pid': Process ID
                   - 'arrival_time': When the process arrives in the system
                   - 'burst_time': How long the process needs CPU
                   - 'priority': Priority level (lower number = higher priority)
    
    Returns:
        Dictionary containing:
        - 'results': List of process details with calculated times
        - 'gantt_chart': List of (pid, start_time, end_time) tuples
        - 'avg_waiting_time': Average waiting time of all processes
        - 'avg_turnaround_time': Average turnaround time of all processes
        - 'cpu_utilization': CPU utilization percentage
    """
    
    # Step 1: Validate input
    if not processes or len(processes) == 0:
        return {
            'results': [],
            'gantt_chart': [],
            'avg_waiting_time': 0,
            'avg_turnaround_time': 0,
            'cpu_utilization': 0
        }
    
    # Step 2: Create a copy so we don't modify the original list
    processes = [p.copy() for p in processes]
    
    # Step 3: Initialize tracking variables
    current_time = 0  # Current time on the CPU
    completed_processes = []  # Processes that have finished
    gantt_chart = []  # Records when each process runs
    
    # Step 4: Main scheduling loop - continue until all processes are done
    while len(completed_processes) < len(processes):
        
        # Step 5: Find all processes that have ARRIVED by current_time
        # "Arrived" means: arrival_time <= current_time
        available_processes = [
            p for p in processes 
            if p['arrival_time'] <= current_time and p not in completed_processes
        ]
        
        # Step 6: Handle CPU idle time
        # If no process has arrived yet, move time forward to the next arrival
        if len(available_processes) == 0:
            # Find the process that arrives next
            next_arrival_time = min(
                p['arrival_time'] for p in processes 
                if p not in completed_processes
            )
            current_time = next_arrival_time
            continue  # Go back to Step 5 with updated time
        
        # Step 7: SELECT THE PROCESS WITH HIGHEST PRIORITY (lowest priority number)
        # This is the key step of Priority Scheduling!
        selected_process = min(
            available_processes, 
            key=lambda p: p['priority']
        )
        
        # Step 8: Execute the selected process (non-preemptive = runs to completion)
        start_time = current_time
        burst_time = selected_process['burst_time']
        completion_time = start_time + burst_time
        
        # Step 9: Record this execution in the Gantt chart
        gantt_chart.append((selected_process['pid'], start_time, completion_time))
        
        # Step 10: Calculate metrics for this process
        arrival_time = selected_process['arrival_time']
        waiting_time = start_time - arrival_time  # Time from arrival to start
        turnaround_time = completion_time - arrival_time  # Total time from arrival to completion
        
        # Step 11: Store results for this process
        result = {
            'pid': selected_process['pid'],
            'arrival_time': arrival_time,
            'burst_time': burst_time,
            'priority': selected_process['priority'],
            'start_time': start_time,
            'completion_time': completion_time,
            'waiting_time': waiting_time,
            'turnaround_time': turnaround_time
        }
        completed_processes.append(result)
        
        # Step 12: Move time forward (CPU is now at the end of this process)
        current_time = completion_time
    
    
    # Step 13: Calculate average metrics
    total_waiting_time = sum(p['waiting_time'] for p in completed_processes)
    total_turnaround_time = sum(p['turnaround_time'] for p in completed_processes)
    
    avg_waiting_time = total_waiting_time / len(completed_processes)
    avg_turnaround_time = total_turnaround_time / len(completed_processes)
    
    # Step 14: Calculate CPU Utilization
    # CPU Utilization = (Total busy time / Total time needed) * 100
    # Total busy time = sum of all burst times
    # Total time needed = final completion time (from 0 to last process completion)
    total_busy_time = sum(p['burst_time'] for p in completed_processes)
    total_time_needed = completed_processes[-1]['completion_time']
    cpu_utilization = (total_busy_time / total_time_needed * 100) if total_time_needed > 0 else 0
    
    # Step 15: Return all results
    return {
        'results': completed_processes,
        'gantt_chart': gantt_chart,
        'avg_waiting_time': round(avg_waiting_time, 2),
        'avg_turnaround_time': round(avg_turnaround_time, 2),
        'cpu_utilization': round(cpu_utilization, 2)
    }


def print_results(scheduling_results):
    """
    Helper function to display the scheduling results in a nice format.
    This is optional - included for easy testing.
    """
    print("\n" + "="*80)
    print("PRIORITY SCHEDULING RESULTS")
    print("="*80)
    
    # Print individual process details
    print("\nProcess Details:")
    print("-" * 80)
    print(f"{'PID':<6} {'Arrival':<10} {'Burst':<8} {'Priority':<10} {'Start':<8} {'Complete':<10} {'Waiting':<10} {'Turnaround':<12}")
    print("-" * 80)
    
    for process in scheduling_results['results']:
        print(f"{process['pid']:<6} {process['arrival_time']:<10} {process['burst_time']:<8} "
              f"{process['priority']:<10} {process['start_time']:<8} {process['completion_time']:<10} "
              f"{process['waiting_time']:<10} {process['turnaround_time']:<12}")
    
    # Print Gantt chart
    print("\nGantt Chart:")
    print("-" * 80)
    for pid, start, end in scheduling_results['gantt_chart']:
        print(f"Process {pid}: [{start} -> {end}]")
    
    # Print average metrics
    print("\nSummary Metrics:")
    print("-" * 80)
    print(f"Average Waiting Time:    {scheduling_results['avg_waiting_time']} units")
    print(f"Average Turnaround Time: {scheduling_results['avg_turnaround_time']} units")
    print(f"CPU Utilization:         {scheduling_results['cpu_utilization']}%")
    print("="*80 + "\n")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

# Create a list of processes
# Format: {'pid': 'P1', 'arrival_time': 0, 'burst_time': 5, 'priority': 2}

processes = [
    {'pid': 'P1', 'arrival_time': 0, 'burst_time': 5, 'priority': 2},
    {'pid': 'P2', 'arrival_time': 1, 'burst_time': 3, 'priority': 1},
    {'pid': 'P3', 'arrival_time': 2, 'burst_time': 4, 'priority': 3},
    {'pid': 'P4', 'arrival_time': 3, 'burst_time': 2, 'priority': 2}
]

# Call the scheduling function
results = priority_scheduling(processes)

# Print the results
print_results(results)

# Access individual results programmatically:
# results['results'] - List of process details
# results['gantt_chart'] - Gantt chart data
# results['avg_waiting_time'] - Average waiting time
# results['avg_turnaround_time'] - Average turnaround time
# results['cpu_utilization'] - CPU utilization percentage
