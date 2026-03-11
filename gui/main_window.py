from modules.system_info import get_cpu_info, get_gpu_info
import psutil, tkinter as tk

class TechCockpit:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TechCockpit v0.1")
        self.root.geometry("1440x900")
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
            ("Live Monitor", self.start_live_monitor),
            ("Выход", self.root.quit),
        ]

        for text, cmd in btn_opts:
            btn = tk.Button(main_frame, text=text, font=("Arial", 12), height=2,
                            bg="#1a1a1a", fg="#d0d0d0", activebackground="#2a2a2a", activeforeground="white",
                            width=40, command=cmd)
            btn.pack(fill="x", pady=8)

        self.status = tk.Label(self.root, text="Готов к работе", bg="black", fg="#9acd32", anchor="w", padx=10)
        self.status.pack(side="bottom", fill="x")

    def show_system_window(self):
        font_title = ("Consolas", 14, "bold")
        font_row = ("Consolas", 12)

        window = tk.Toplevel(self.root)
        window.configure(bg='black')
        window.title("Системная информация")
        window.geometry("1000x600")

        cpu_data = get_cpu_info()
        memory_data = psutil.virtual_memory()
        gpu_data = get_gpu_info()

        container = tk.Frame(window, bg='black')
        container.place(relx=0.5, rely=0.5, anchor='center')

        header = tk.Label(container, text="CPU INFO", font=font_title, fg="white", bg="black")
        header.grid(row=0, column=0, columnspan=2, pady=(0, 6))

        row = 1

        def add_row(label_text, value_text):
            nonlocal row
            tk.Label(container, text=label_text, font=font_row, fg="white", bg="black", anchor="w", width=20) \
                .grid(row=row, column=0, sticky="w", padx=10, pady=2)
            tk.Label(container, text=value_text, font=font_row, fg="#9acd32", bg="black", anchor="e", width=25) \
                .grid(row=row, column=1, sticky="e", padx=10, pady=2)
            row += 1

        add_row("Cores", f"{cpu_data['physical_cores']} / {cpu_data['cores']}")
        add_row("Load", f"{cpu_data['usage']:.1f}%")
        add_row("Temperature", cpu_data['temp'])  # 52.3°C (max 95°)

        row += 1
        header_ram = tk.Label(container, text="RAM INFO", font=font_title, fg="white", bg="black")
        header_ram.grid(row=row, column=0, columnspan=2, pady=(12, 6))

        row += 1
        add_row("Total RAM", f"{memory_data.total // (1024 ** 3)} GB")
        add_row("Used RAM", f"{memory_data.percent:.1f}%")
        add_row("Available RAM", f"{memory_data.available // (1024 ** 3)} GB")

        # GPU секция — Load/Temp/Memory БЕЗ Name
        row += 1
        header_gpu = tk.Label(container, text="GPU INFO", font=font_title, fg="white", bg="black")
        header_gpu.grid(row=row, column=0, columnspan=2, pady=(12, 6))

        if isinstance(gpu_data, list):
            for i, gpu in enumerate(gpu_data, 1):
                row += 1
                add_row(f"GPU {i} Load", gpu.get('load', 'N/A'))  # 45%
                add_row(f"GPU {i} Temp", gpu.get('temp', 'N/A'))  # 67°C (max 83°)
                add_row(f"GPU {i} Memory", f"{gpu.get('mem_used', 'N/A')}/{gpu.get('mem_total', 'N/A')}")
                row += 1  # Разделитель между GPU

    def start_live_monitor(self):
        self.live_window = tk.Toplevel(self.root)
        self.live_window.configure(bg='black')
        self.live_window.title("Live Monitor")
        self.live_window.geometry("800x500")
        self.update_live_display()

    def update_live_display(self):
        if hasattr(self, 'live_window') and self.live_window.winfo_exists():
            cpu_data = get_cpu_info()
            memory_data = psutil.virtual_memory()
            import datetime
            info_text = f"""🔥 LIVE STATS (обновлено: {datetime.datetime.now().strftime('%H:%M:%S')})
CPU: {cpu_data['usage']:.1f}% | Temp: {cpu_data['temp']}
RAM: {memory_data.percent:.1f}% ({memory_data.available // (1024 ** 3)} GB free)"""

            try:
                self.live_label.config(text=info_text)
            except:
                self.live_label = tk.Label(self.live_window, text=info_text, font=("Consolas", 14),
                                           fg="#9acd32", bg="black", padx=20, pady=20)
                self.live_label.pack(expand=True, fill="both")

            self.live_window.after(1000, self.update_live_display)

    def run(self):
        self.root.mainloop()
