import tkinter as tk

root = tk.Tk()
root.title("TechCockpit v0.1")
root.geometry("1440x900")

main_frame = tk.Frame(root, bg="gray10", padx=20, pady=20)
main_frame.pack(side="top", fill="both", expand=True)

title = tk.Label(main_frame, text="TechCockpit v0.1",
                 font=("Arial", 24, "bold"), fg="white", bg="gray10")
title.pack(pady=(0, 30))

btn1 = tk.Button(main_frame, text="🖥️ SystemInfo",
                 font=("Arial", 14), height=2, bg="darkblue", fg="white")
btn1.pack(fill="x", pady=10)

btn2 = tk.Button(main_frame, text="💻 Coding.. (in development)",
                 font=("Arial", 14), height=2, bg="darkgreen", fg="white")
btn2.pack(fill="x", pady=10)

btn3 = tk.Button(main_frame, text="Future features",
                 font=("Arial", 14), height=2, bg="purple", fg="white")
btn3.pack(fill="x", pady=10)

btn4 = tk.Button(main_frame, text="❌ Выход",
                 font=("Arial", 14), height=2, bg="darkred", fg="white",
                 command=root.quit)
btn4.pack(fill="x", pady=10)

status = tk.Label(root, text="Готов к работе", bg="gray20", fg="lime",
                  anchor="w", padx=10)
status.pack(side="bottom", fill="x")

if __name__ == '__main__':
    root.mainloop()
