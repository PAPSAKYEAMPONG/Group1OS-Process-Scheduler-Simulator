import tkinter as tk
from tkinter import ttk, messagebox
import copy

# --- Core Process Class ---
class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid              # The process name (like "P1")
        self.arrival_time = arrival # When it shows up
        self.burst_time = burst     # How long it takes
        self.priority = priority    # How important it is (smaller number = more important)
        self.start_time = 0         # When the CPU actually starts it
        self.completion_time = 0    #The time it takes to complete
        self.waiting_time = 0       # Time spent sitting in the queue
        self.turnaround_time = 0    # Total time from Arrival to CT
        self.remaining_time = burst # Used for Round Robin "slices"

class SchedulerApp:
    def __init__(self, root):
        self.root = root    # main window container provided by Tkinter
        self.root.title("Group 1: OS Process Scheduler Simulator") # My group's name at the very top of the window bar
        self.root.geometry("1000x850") # size of window to 1000 pixels wide and 850 tall
        self.processes = [] # empty list where we will store the processes we add

        # 1. Input Interface
        input_frame = tk.LabelFrame(root, text="Step 1: Enter Process Details", padx=10, pady=10) # A labeled box

        input_frame.pack(fill="x", padx=20, pady=10) # Box to sit at the top and stretch from left to right 

        fields = [("PID:", "P1"), ("Arrival:", "0"), ("Burst:", "5"), ("Priority:", "1")] # Starting hints for the user

        self.entries = {} # A dictionary to store the white typing boxes for later use

        # We loop through those 4 fields so we don't have to write the same code 4 times
        for i, (label, default) in enumerate(fields):

            tk.Label(input_frame, text=label).grid(row=0, column=i*2, padx=5) # Write the label (e.g., "PID:") on the screen

            entry = tk.Entry(input_frame, width=8) # The white box where the user types

            entry.insert(0, default) # Hint (like "P1") inside the box

            entry.grid(row=0, column=i*2+1, padx=5)

            self.entries[label] = entry # Save this box in our dictionary so our 'Add' button can find the numbers

        # Create the green "Add to List" button
        # 'command=self.add_process' tells Python: "When clicked, run that function!"
        tk.Button(input_frame, text="Add to List", command=self.add_process, bg="#4CAF50", fg="white").grid(row=0, column=8, padx=15)



        # 2. Controls
        control_frame = tk.LabelFrame(root, text="Step 2: Choose Algorithm & Run", padx=10, pady=10)
        control_frame.pack(fill="x", padx=20, pady=5)

        # The Combobox is a drop-down menu for our 4 algorithms
        self.algo_choice = ttk.Combobox(control_frame, values=["FCFS", "SJF (Non-Preemptive)", "Priority", "Round Robin"])
        self.algo_choice.set("FCFS")
        self.algo_choice.pack(side="left", padx=10)
        self.quantum_entry = tk.Entry(control_frame, width=5); self.quantum_entry.insert(0, "2"); self.quantum_entry.pack(side="left", padx=5)
        tk.Button(control_frame, text="EXECUTE", command=self.run_simulation, bg="#2196F3", fg="white", width=15).pack(side="left", padx=20)
        tk.Button(control_frame, text="CLEAR ALL", command=self.clear_data).pack(side="left")

        # 3. Output Table (Added CT column here)
        self.tree = ttk.Treeview(root, columns=("PID", "AT", "BT", "PRI", "CT", "WT", "TAT"), show="headings", height=8)
        column_map = {"PID": "PID", "AT": "Arrival", "BT": "Burst", "PRI": "Priority", "CT": "Comp Time", "WT": "Wait Time", "TAT": "Turnaround"}
        for col, heading in column_map.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=110, anchor="center")
        self.tree.pack(fill="x", padx=20, pady=5)

        # 4. Gantt Chart Canvas
        self.chart_frame = tk.LabelFrame(root, text="Step 3: Gantt Chart Visualization", padx=10, pady=10)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.canvas = tk.Canvas(self.chart_frame, bg="white", height=150)
        self.canvas.pack(fill="both", expand=True)
        
        self.summary_label = tk.Label(root, text="Results summary will appear here.", font=("Arial", 10, "bold"))
        self.summary_label.pack(pady=5)

    def add_process(self):
        # 1. THE 'TRY' BLOCK is a safety net. If someone types 'abc' instead of a number, the program won't crash; it will jump to the 'except' part.
        try:
            p = Process(self.entries["PID:"].get(), int(self.entries["Arrival:"].get()), int(self.entries["Burst:"].get()), int(self.entries["Priority:"].get()))
            self.processes.append(p)
            self.tree.insert("", "end", values=(p.pid, p.arrival_time, p.burst_time, p.priority, "-", "-", "-"))
        except: messagebox.showerror("Error", "Check your numbers!")

    def run_simulation(self):
        if not self.processes: return
        algo = self.algo_choice.get()
        data = copy.deepcopy(self.processes)
        if algo == "FCFS": res = self.logic_fcfs(data)
        elif algo == "SJF (Non-Preemptive)": res = self.logic_sjf(data)
        elif algo == "Priority": res = self.logic_priority(data)
        else: res = self.logic_rr(data, int(self.quantum_entry.get()))
        self.display_results(res)
        self.draw_gantt(res)

    # --- Logic sections now calculate CT, WT, and TAT ---
    def logic_fcfs(self, procs):
        procs.sort(key=lambda x: x.arrival_time)
        t = 0
        for p in procs:
            if t < p.arrival_time: t = p.arrival_time
            p.start_time = t
            p.completion_time = t + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            t = p.completion_time
        return procs

    def logic_sjf(self, procs):
        n, t, count, res = len(procs), 0, 0, []
        comp = [False] * n
        while count < n:
            avail = [i for i in range(n) if procs[i].arrival_time <= t and not comp[i]]
            if not avail: t += 1; continue
            idx = min(avail, key=lambda i: procs[i].burst_time)
            p = procs[idx]
            p.start_time = t
            p.completion_time = t + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            t = p.completion_time
            comp[idx] = True; count += 1; res.append(p)
        return res

    def logic_priority(self, procs):
        n, t, count, res = len(procs), 0, 0, []
        comp = [False] * n
        while count < n:
            avail = [i for i in range(n) if procs[i].arrival_time <= t and not comp[i]]
            if not avail: t += 1; continue
            idx = min(avail, key=lambda i: procs[i].priority)
            p = procs[idx]
            p.start_time = t
            p.completion_time = t + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            t = p.completion_time
            comp[idx] = True; count += 1; res.append(p)
        return res

    def logic_rr(self, procs, q):
        procs.sort(key=lambda x: x.arrival_time)
        queue, t, count, res, visited = [procs[0]], 0, 0, [], [False]*len(procs)
        visited[0] = True
        gantt_log = [] # RR needs a complex log for accurate Gantt drawing
        while count < len(procs):
            if not queue:
                t += 1
                for i, p in enumerate(procs):
                    if p.arrival_time <= t and not visited[i]: queue.append(p); visited[i] = True
                continue
            curr = queue.pop(0)
            start_this_turn = t
            run = min(curr.remaining_time, q)
            curr.remaining_time -= run; t += run
            gantt_log.append((curr.pid, start_this_turn, t))
            for i, p in enumerate(procs):
                if p.arrival_time <= t and not visited[i]: queue.append(p); visited[i] = True
            if curr.remaining_time > 0: queue.append(curr)
            else:
                curr.completion_time = t
                curr.turnaround_time = t - curr.arrival_time
                curr.waiting_time = curr.turnaround_time - curr.burst_time
                count += 1; res.append(curr)
        self.rr_gantt_data = gantt_log # Store for drawing
        return res

    def display_results(self, res):
        for i in self.tree.get_children(): self.tree.delete(i)
        tw, tt = 0, 0
        # Re-sort by PID for consistent table view
        table_view = sorted(res, key=lambda x: x.pid)
        for p in table_view:
            self.tree.insert("", "end", values=(p.pid, p.arrival_time, p.burst_time, p.priority, p.completion_time, p.waiting_time, p.turnaround_time))
            tw += p.waiting_time; tt += p.turnaround_time
        self.summary_label.config(text=f"Avg Wait: {tw/len(res):.2f}ms | Avg Turnaround: {tt/len(res):.2f}ms")

    def draw_gantt(self, res):
        self.canvas.delete("all")
        if not res: return
        colors = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF"]
        x_start, y_top, height, scale = 50, 40, 50, 25
        
        # Determine drawing data based on algo
        if self.algo_choice.get() == "Round Robin":
            draw_data = self.rr_gantt_data
        else:
            # Sort by start time for non-preemptive
            sorted_res = sorted(res, key=lambda x: x.start_time)
            draw_data = [(p.pid, p.start_time, p.completion_time) for p in sorted_res]
        
        color_map = {}
        for i, p_orig in enumerate(self.processes): color_map[p_orig.pid] = colors[i % len(colors)]

        for i, (pid, start, end) in enumerate(draw_data):
            x1 = x_start + (start * scale)
            x2 = x_start + (end * scale)
            self.canvas.create_rectangle(x1, y_top, x2, y_top + height, fill=color_map.get(pid, "gray"), outline="black")
            self.canvas.create_text((x1 + x2)/2, y_top + height/2, text=pid)
            self.canvas.create_text(x1, y_top + height + 15, text=str(start))
            if i == len(draw_data) - 1:
                self.canvas.create_text(x2, y_top + height + 15, text=str(end))

    def clear_data(self):
        self.processes = []; self.canvas.delete("all")
        for i in self.tree.get_children(): self.tree.delete(i)

if __name__ == "__main__":
    root = tk.Tk(); app = SchedulerApp(root); root.mainloop()