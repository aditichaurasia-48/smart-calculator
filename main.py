import tkinter as tk
from tkinter import messagebox
import os
import sys

# ==================================================
# SAFE HISTORY PATH (NO PERMISSION ERROR)
# ==================================================
def get_history_path():
    data_dir = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        "SmartCalculator"
    )
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "history.txt")

HISTORY_FILE = get_history_path()

# ==================================================
# CENTER WINDOW
# ==================================================
def center_window(win, w=800, h=550):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ==================================================
# MAIN WINDOW
# ==================================================
root = tk.Tk()
root.title("Smart Calculator")
center_window(root, 800, 550)
root.resizable(False, False)
root.configure(bg="#1e1e1e")
root.tk.call("tk", "scaling", 1.25)

# ICON (safe)
try:
    root.iconbitmap("calculator.ico")
except:
    pass

# ==================================================
# FONTS
# ==================================================
FONT_DISPLAY = ("Segoe UI", 26, "bold")
FONT_BUTTON  = ("Segoe UI", 14, "bold")
FONT_HISTORY = ("Consolas", 12)

# ==================================================
# VARIABLES
# ==================================================
expression = ""
memory = 0

# ==================================================
# DISPLAY
# ==================================================
display_var = tk.StringVar()
display = tk.Entry(
    root,
    textvariable=display_var,
    font=FONT_DISPLAY,
    bg="#111111",
    fg="white",
    bd=10,
    relief="flat",
    justify="right"
)
display.place(x=20, y=20, width=360, height=65)

# ==================================================
# HISTORY
# ==================================================
tk.Label(
    root,
    text="History",
    font=("Segoe UI", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
).place(x=420, y=30)

history_box = tk.Text(
    root,
    font=FONT_HISTORY,
    bg="#111111",
    fg="white",
    bd=0
)
history_box.place(x=420, y=70, width=350, height=380)

def load_history():
    history_box.delete(1.0, tk.END)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_box.insert(tk.END, f.read())

def save_history(text):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def clear_history():
    open(HISTORY_FILE, "w").close()
    load_history()

# ==================================================
# FUNCTIONS
# ==================================================
def press(value):
    global expression
    expression += str(value)
    display_var.set(expression)

def clear():
    global expression
    expression = ""
    display_var.set("")

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def calculate():
    global expression
    try:
        result = str(eval(expression))
        save_history(f"{expression} = {result}")
        expression = result
        display_var.set(result)
        load_history()
    except:
        display_var.set("Error")
        expression = ""

        def on_key(event):
            key = event.char

            if key.isdigit() or key in "+-*/.":
                press(key)
            elif event.keysym == "Return":
                calculate()
            elif event.keysym == "BackSpace":
                backspace()
            elif event.keysym == "Escape":
                clear()
def percent():
    global expression
    try:
        value = float(expression)
        expression = str(value / 100)
        display_var.set(expression)
    except:
        display_var.set("Error")
        expression = ""

import math  # top me import

def sqrt_value():
    global expression
    try:
        value = float(expression)
        expression = str(math.sqrt(value))
        display_var.set(expression)
    except:
        display_var.set("Error")
        expression = ""
def square():
    global expression
    try:
        value = float(expression)
        expression = str(value ** 2)
        display_var.set(expression)
    except:
        display_var.set("Error")
        expression = ""

        display_var.set("Error")
        root.after(1200, clear)


# ---------------- MEMORY ----------------
def memory_add():
    global memory
    try:
        memory += float(display_var.get())
    except:
        pass

def memory_sub():
    global memory
    try:
        memory -= float(display_var.get())
    except:
        pass

def memory_recall():
    display_var.set(str(memory))

def memory_clear():
    global memory
    memory = 0

# ==================================================
# BUTTONS
# ==================================================
buttons = [
    ("7", 20, 110), ("8", 110, 110), ("9", 200, 110), ("/", 290, 110),
    ("4", 20, 170), ("5", 110, 170), ("6", 200, 170), ("*", 290, 170),
    ("1", 20, 230), ("2", 110, 230), ("3", 200, 230), ("-", 290, 230),
    ("0", 20, 290), (".", 110, 290), ("+", 200, 290)
]

for (text, x, y) in buttons:
    tk.Button(
        root,
        text=text,
        font=FONT_BUTTON,
        bg="#2b2b2b",
        fg="white",
        activebackground="#444444",
        command=lambda t=text: press(t)
    ).place(x=x, y=y, width=80, height=55)

tk.Button(
    root, text="=", font=FONT_BUTTON,
    bg="#ff9500", fg="black",
    command=calculate
).place(x=20, y=350, width=350, height=60)

tk.Button(root, text="⌫", font=FONT_BUTTON, command=backspace)\
    .place(x=20, y=425, width=80, height=45)

tk.Button(root, text="C", font=FONT_BUTTON, command=clear)\
    .place(x=110, y=425, width=80, height=45)

tk.Button(root, text="M+", font=FONT_BUTTON, command=memory_add)\
    .place(x=20, y=480, width=80, height=40)

tk.Button(root, text="M-", font=FONT_BUTTON, command=memory_sub)\
    .place(x=110, y=480, width=80, height=40)

tk.Button(root, text="MR", font=FONT_BUTTON, command=memory_recall)\
    .place(x=200, y=480, width=80, height=40)

tk.Button(root, text="MC", font=FONT_BUTTON, command=memory_clear)\
    .place(x=290, y=480, width=80, height=40)

tk.Button(
    root, text="Clear History",
    font=FONT_BUTTON,
    command=clear_history
).place(x=430, y=470, width=300, height=45)
tk.Button(
    root, text="%", font=FONT_BUTTON,
    command=percent
).place(x=290, y=290, width=80, height=55)

tk.Button(
    root, text="√", font=FONT_BUTTON,
    command=sqrt_value
).place(x=290, y=170, width=80, height=55)

tk.Button(
    root, text="x²", font=FONT_BUTTON,
    command=square
).place(x=290, y=230, width=80, height=55)


# ==================================================
# START
# ==================================================
load_history()
root.bind("<Key>", 'on_key')
backspace= "delete"
esc= clear
root.mainloop()
