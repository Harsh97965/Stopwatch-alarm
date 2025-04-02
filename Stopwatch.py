import tkinter as tk
import time
import datetime

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch & Alarm")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e1e1e")
        
        # Heading Label
        self.heading_label = tk.Label(root, text="⏱ Stopwatch & Alarm ⏰", font=("Courier", 22, "bold"), fg="#ffcc00", bg="#1e1e1e", pady=10)
        self.heading_label.pack()
        
        self.start_time = 0
        self.running = False
        self.timer_set = None
        self.blinking = False
        self.alarm_time = None
        
        self.clock_label = tk.Label(root, text="", font=("Courier", 26, "bold"), fg="#00ffff", bg="#1e1e1e")
        self.clock_label.pack(pady=10)
        
        self.label = tk.Label(root, text="00:00:00.000", font=("Courier", 44, "bold"), fg="#00ff00", bg="#333333", relief="ridge", bd=5, padx=20, pady=10)
        self.label.pack(pady=20)
        
        entry_frame = tk.Frame(root, bg="#1e1e1e")
        entry_frame.pack(pady=10)
        
        self.time_entry = tk.Entry(entry_frame, font=("Arial", 16), width=10, justify='center', bg="#222", fg="#ffffff", relief="solid", bd=3)
        self.time_entry.insert(0, "00:00:10")  # Default 10 seconds timer
        self.time_entry.grid(row=0, column=0, padx=5)
        
        set_timer_button = tk.Button(entry_frame, text="⏳ Set Timer", command=self.set_timer, font=("Arial", 12, "bold"), bg="#ff8800", fg="white", padx=10, pady=5, relief="raised")
        set_timer_button.grid(row=0, column=1, padx=5)
        
        self.alarm_entry = tk.Entry(entry_frame, font=("Arial", 16), width=10, justify='center', bg="#222", fg="#ffffff", relief="solid", bd=3)
        self.alarm_entry.insert(0, "12:00:00")  # Default alarm time
        self.alarm_entry.grid(row=1, column=0, padx=5, pady=5)
        
        set_alarm_button = tk.Button(entry_frame, text="⏰ Set Alarm", command=self.set_alarm, font=("Arial", 12, "bold"), bg="#ff0000", fg="white", padx=10, pady=5, relief="raised")
        set_alarm_button.grid(row=1, column=1, padx=5, pady=5)
        
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="▶ Start", command=self.start, font=("Arial", 14, "bold"), bg="#00aa00", fg="white", padx=15, pady=8, relief="raised")
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = tk.Button(button_frame, text="⏸ Stop", command=self.stop, font=("Arial", 14, "bold"), bg="#aa0000", fg="white", padx=15, pady=8, relief="raised")
        self.stop_button.grid(row=0, column=1, padx=10)
        
        self.reset_button = tk.Button(button_frame, text="🔄 Reset", command=self.reset, font=("Arial", 14, "bold"), bg="#5555ff", fg="white", padx=15, pady=8, relief="raised")
        self.reset_button.grid(row=0, column=2, padx=10)
        
        self.update_display()
        self.update_clock()
    
    def update_display(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            mins, secs = divmod(int(elapsed_time), 60)
            hours, mins = divmod(mins, 60)
            milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
            self.label.config(text=f"{hours:02}:{mins:02}:{secs:02}.{milliseconds:03}")
            
            if self.timer_set and elapsed_time >= self.timer_set:
                self.running = False
                self.start_alarm()
        
        self.root.after(10, self.update_display)  # Update every 10 ms for better precision
    
    def update_clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        
        if self.alarm_time and current_time == self.alarm_time:
            self.start_alarm()
        
        self.root.after(1000, self.update_clock)  # Update every second
    
    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time()  # Resume from last time
            self.running = True
    
    def stop(self):
        self.running = False
    
    def reset(self):
        self.running = False
        self.blinking = False
        self.start_time = time.time()
        self.label.config(text="00:00:00.000", fg="#00ff00", bg="#333333")
    
    def elapsed_time(self):
        if self.running:
            return time.time() - self.start_time
        return 0
    
    def set_timer(self):
        time_str = self.time_entry.get()
        try:
            h, m, s = map(int, time_str.split(":"))
            self.timer_set = h * 3600 + m * 60 + s
        except ValueError:
            self.timer_set = None
    
    def set_alarm(self):
        self.alarm_time = self.alarm_entry.get()
    
    def start_alarm(self):
        self.blinking = True
        self.blink_full_screen()
    
    def blink_full_screen(self):
        if self.blinking:
            current_color = self.root.cget("bg")
            new_color = "#ff0000" if current_color == "#1e1e1e" else "#1e1e1e"
            self.root.configure(bg=new_color)
            self.label.config(bg=new_color)
            self.clock_label.config(bg=new_color)
            self.root.after(500, self.blink_full_screen)  # Blink every 500ms 

if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()
