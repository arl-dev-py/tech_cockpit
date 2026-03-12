from modules.system_info import get_cpu_info, get_gpu_info, get_top_processes, CACHE_PATHS, get_cache_size
import psutil
import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import os

class TechCockpit:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TechCockpit v0.1")
        self.root.geometry("1440x500")
        self.root.configure(bg="black")
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        main_frame.pack(side="top", fill="both", expand=True)

        self.title_font = ("Arial", 20, "bold")

        title = tk.Label(main_frame, text="TechCockpit v0.1", font=self.title_font, fg="white", bg="black")
        title.pack(pady=(0, 24))

        btn_opts = [
            ("System Info", self.show_system_window),
            ("Make Working Place", self.working_session),
            ("Cache Flush", self.show_cache_cleanup),
            ("Live Monitor", self.start_live_monitor),
            ("Exit", self.root.quit),
        ]

        for text, cmd in btn_opts:
            btn = tk.Button(main_frame, text=text, font=("Arial", 12), height=2,
                            bg="#1a1a1a", fg="#d0d0d0", activebackground="#2a2a2a", activeforeground="white",
                            width=40, command=cmd)
            btn.pack(fill="x", pady=8)

        self.status = tk.Label(self.root, text="Ready", bg="black", fg="#9acd32", anchor="w", padx=10)
        self.status.pack(side="bottom", fill="x")

    def show_system_window(self):
        self.sys_window = tk.Toplevel(self.root)
        self.sys_window.configure(bg='black')
        self.sys_window.title("SysInfo (realtime)")
        self.sys_window.geometry("1200x700")

        self.sys_container = tk.Frame(self.sys_window, bg='black')
        self.sys_container.place(relx=0.5, rely=0.5, anchor='center')

        self.update_system_display()

    def working_session(self):
        webbrowser.open('https://music.yandex.ru/')
        webbrowser.open('https://www.perplexity.ai/')

        pycharm_path = r"C:\Program Files\JetBrains\PyCharm 2025.3.2\bin\pycharm64.exe"
        if os.path.exists(pycharm_path):
            subprocess.Popen([pycharm_path])
        else:
            messagebox.showwarning("PyCharm", "Not found")

    def update_system_display(self):
        if hasattr(self, 'sys_window') and self.sys_window.winfo_exists():
            for widget in self.sys_container.winfo_children():
                widget.destroy()

            cpu_data = get_cpu_info()
            memory_data = psutil.virtual_memory()
            gpu_data = get_gpu_info()

            row = 0
            font_title = ("Consolas", 14, "bold")
            font_row = ("Consolas", 12)

            def add_row(label_text, value_text):
                nonlocal row
                tk.Label(self.sys_container, text=label_text, font=font_row,
                         fg="white", bg="black", anchor="w", width=20) \
                    .grid(row=row, column=0, sticky="w", padx=10, pady=2)
                tk.Label(self.sys_container, text=value_text, font=font_row,
                         fg="#9acd32", bg="black", anchor="e", width=25) \
                    .grid(row=row, column=1, sticky="e", padx=10, pady=2)
                row += 1

            tk.Label(self.sys_container, text="CPU INFO", font=font_title, fg="white", bg="black") \
                .grid(row=row, column=0, columnspan=2, pady=(0, 6))
            row += 1

            add_row("Cores", f"{cpu_data['cores']}")
            add_row("Load", f"{cpu_data['usage']:.1f}%")
            add_row("Temperature", cpu_data['temp'])

            row += 1
            tk.Label(self.sys_container, text="MEMORY INFO", font=font_title, fg="white", bg="black") \
                .grid(row=row, column=0, columnspan=2, pady=(12, 6))
            row += 1

            add_row("Total", f"{memory_data.total // (1024 ** 3)} GB")
            add_row("Used", f"{memory_data.percent:.1f}%")
            add_row("Available", f"{memory_data.available // (1024 ** 3)} GB")

            row += 1
            tk.Label(self.sys_container, text="GPU INFO", font=font_title, fg="white", bg="black") \
                .grid(row=row, column=0, columnspan=2, pady=(12, 6))

            if isinstance(gpu_data, list):
                for i, gpu in enumerate(gpu_data, 1):
                    row += 1
                    add_row("Load", gpu.get('load', 'N/A'))
                    add_row("Temp", gpu.get('temp', 'N/A'))
                    add_row("Memory", f"{gpu.get('mem_used', 'N/A')}/{gpu.get('mem_total', 'N/A')}")
                    row += 1

            processes = get_top_processes()

            row += 1
            tk.Label(self.sys_container, text="PROCESSES (TOP 5)", font=font_title, fg="white", bg="black") \
                .grid(row=row, column=0, columnspan=2, pady=(12, 6))
            row += 1

            for i, proc in enumerate(processes[:5], 1):
                cpu_ram = f"{proc['cpu']} / {proc['ram']}"
                add_row(proc['name'], cpu_ram[:20])

            self.sys_window.after(1000, self.update_system_display)

    def start_live_monitor(self):
        self.live_window = tk.Toplevel(self.root)
        self.live_window.configure(bg='black')
        self.live_window.title("Live Monitor (realtime)")
        self.live_window.geometry("900x600")
        self.update_live_display()

    def update_live_display(self):
        if hasattr(self, 'live_window') and self.live_window.winfo_exists():
            cpu_data = get_cpu_info()
            memory_data = psutil.virtual_memory()
            gpu_data = get_gpu_info()

            gpu_load = 0
            gpu_temp = 'N/A'
            if gpu_data and isinstance(gpu_data, list) and gpu_data:
                if gpu_data[0].get('load', 'N/A') != 'N/A':
                    gpu_load = float(gpu_data[0]['load'].rstrip('%'))
                gpu_temp = gpu_data[0].get('temp', 'N/A')

            import datetime
            info_text = f"""🔥 LIVE STATS (updated: {datetime.datetime.now().strftime('%H:%M:%S')})
💻 CPU: {cpu_data['usage']:.1f}% | {cpu_data['temp']}
🧠 MEMORY: {memory_data.percent:.1f}% ({memory_data.available // (1024 ** 3)} GB free)
🎮 GPU: {gpu_load:.1f}% | {gpu_temp}"""

            try:
                self.live_label.config(text=info_text)
            except:
                self.live_label = tk.Label(self.live_window, text=info_text, font=("Consolas", 16),
                                           fg="#9acd32", bg="black", padx=20, pady=20, justify="left")
                self.live_label.pack(expand=True, fill="both")

            self.live_window.after(1000, self.update_live_display)

    def show_cache_cleanup(self):
        self.cache_window = tk.Toplevel(self.root)
        self.cache_window.title("Cleaning Cache")
        self.cache_window.geometry("500x450")
        self.cache_window.configure(bg='black')

        main_frame = tk.Frame(self.cache_window, bg='black')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.cache_vars = {}
        self.cache_checkbuttons = {}

        for i, (category, paths) in enumerate(CACHE_PATHS.items()):
            size_str, _ = get_cache_size(paths)
            var = tk.BooleanVar(value=True)
            self.cache_vars[category] = var

            chk = tk.Checkbutton(
                main_frame,
                text=f"{category.replace('_', ' ').title()}: {size_str}",
                variable=var,
                bg='black', fg='#9acd32', selectcolor='#1a1a1a',
                font=("Consolas", 12),
                anchor='w'
            )
            chk.pack(pady=12)
            self.cache_checkbuttons[category] = chk


        btn = tk.Button(
            main_frame,
            text="Clear",
            font=("Arial", 12),
            height=2,
            bg="#1a1a1a", fg="#d0d0d0",
            activebackground="#2a2a2a", activeforeground="white",
            width=40,
            command=self.execute_cleanup
        )
        btn.pack(pady=20)

    def execute_cleanup(self):
        from modules.system_info import clear_cache_paths
        selected_paths = []
        total_size = 0

        for category, var in self.cache_vars.items():
            if var.get():
                paths = CACHE_PATHS[category]
                size_str = self.cache_checkbuttons[category].cget('text').split(': ')[1]
                total_size += float(size_str.replace(' GB', ''))
                selected_paths.extend(paths)

        if not selected_paths:
            messagebox.showwarning("Warning", "Choose at least one category!")
            return

        result = messagebox.askyesno(
            "Confirmation",
            f"Clear cache?\nWill free up: {total_size:.1f} GB"
        )

        if result:
            freed = clear_cache_paths(selected_paths)
            messagebox.showinfo("Ready!", freed)
            self.cache_window.destroy()

    def run(self):
        self.root.mainloop()


