import tkinter as tk
from modules.system_info import get_cpu_info


class TechCockpit:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TechCockpit v0.1")
        self.root.geometry("1440x900")
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="gray10", padx=20, pady=20)
        main_frame.pack(side="top", fill="both", expand=True)

        title = tk.Label(main_frame, text="TechCockpit v0.1", font=("Arial", 24, "bold"), fg="white", bg="gray10")
        title.pack(pady=(0, 30))

        btn1 = tk.Button(main_frame, text="🖥️ SystemInfo", font=("Arial", 14), height=2, bg="darkblue", fg="white",
                         command=self.show_system_window)
        btn1.pack(fill="x", pady=10)

        btn2 = tk.Button(main_frame, text="💻 Coding.. (in development)", font=("Arial", 14), height=2, bg="darkgreen",
                         fg="white")
        btn2.pack(fill="x", pady=10)

        btn3 = tk.Button(main_frame, text="Future features", font=("Arial", 14), height=2, bg="purple", fg="white")
        btn3.pack(fill="x", pady=10)

        btn4 = tk.Button(main_frame, text="❌ Выход", font=("Arial", 14), height=2, bg="darkred", fg="white",
                         command=self.root.quit)
        btn4.pack(fill="x", pady=10)

        status = tk.Label(self.root, text="Готов к работе", bg="gray20", fg="lime", anchor="w", padx=10)
        status.pack(side="bottom", fill="x")

    def show_system_window(self):
        window = tk.Toplevel(self.root)
        window.configure(bg='black')
        window.title("Системная информация")
        window.geometry("1000x600")

        cpu_data = get_cpu_info()

        info_text = f"""CPU:
    Cores: {cpu_data['cores']}
    Load: {cpu_data['usage']:.1f}%
    Temperature: {cpu_data['temp']}
    Max temp: {cpu_data['max_temp']}
    Per core: {cpu_data['per_core']}"""

        tk.Label(window, text="CPU Information", font=("Arial", 16, "bold"), fg="white", bg="gray20").pack(pady=10)
        tk.Label(window, text=info_text, font=("Consolas", 12), fg="lime", bg="black", padx=20, pady=20,
                 justify="left").pack(expand=True, fill="both")

    def run(self):
        self.root.mainloop()

