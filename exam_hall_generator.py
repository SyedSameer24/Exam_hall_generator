import tkinter as tk
from tkinter import messagebox
import random

# --- Configuration ---
DEPARTMENTS = {
    "CSE": "CS", "ISE": "IS", "ECE": "EC", "EEE": "EE",
    "MECH": "ME", "CIVIL": "CV", "IC": "IC", "AIML": "AI"
}
ROOM_CAPACITY = 60
ROOM_LIST = [floor * 100 + room for floor in range(1, 6) for room in range(1, 11)]
room_occupancy = {room: 0 for room in ROOM_LIST}
usn_room_map = {}

def generate_usn(branch_code, usn_number):
    return f"1RR24{branch_code}{usn_number:02d}"

def assign_room(usn):
    if usn in usn_room_map:
        return usn_room_map[usn]

    available_rooms = [room for room, count in room_occupancy.items() if count < ROOM_CAPACITY]
    if not available_rooms:
        return None

    selected_room = random.choice(available_rooms)
    room_occupancy[selected_room] += 1
    usn_room_map[usn] = selected_room
    return selected_room

# --- GUI Setup ---
root = tk.Tk()
root.title("Exam Room Allotment System")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#d0e6f8")

# Header
header = tk.Label(
    root,
    text="🎓 Exam Hall Allotment System",
    font=("Calibri", 22, "bold italic"),
    bg="#d0e6f8",
    fg="#283593"
)
header.place(relx=0.5, y=20, anchor="n")

# Form Frame
form_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="ridge", highlightthickness=3, highlightbackground="#3949AB")
form_frame.place(relx=0.5, y=70, anchor="n", width=400, height=140)

tk.Label(form_frame, text="Department:", font=("Verdana", 14, "bold"), bg="#ffffff", fg="#3949AB").grid(row=0, column=0, padx=10, pady=15, sticky="e")
branch_var = tk.StringVar(value=list(DEPARTMENTS.keys())[0])
branch_menu = tk.OptionMenu(form_frame, branch_var, *DEPARTMENTS.keys())
branch_menu.config(font=("Verdana", 12), fg="#1A237E", relief="raised", bd=3)
branch_menu.grid(row=0, column=1, padx=10, pady=15)

tk.Label(form_frame, text="USN Number (1-60):", font=("Verdana", 14, "bold"), bg="#ffffff", fg="#3949AB").grid(row=1, column=0, padx=10, pady=5, sticky="e")
usn_spinbox = tk.Spinbox(form_frame, from_=1, to=60, width=5, font=("Verdana", 14), relief="sunken", bd=3)
usn_spinbox.grid(row=1, column=1, padx=10, pady=5)

# Result Label
result_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"), bg="#d0e6f8", fg="#1B5E20")
result_label.place(relx=0.5, y=230, anchor="n")

# Submit Button
def on_submit():
    try:
        usn_number = int(usn_spinbox.get())
        branch = branch_var.get()

        if branch not in DEPARTMENTS:
            messagebox.showerror("Invalid", "Select a valid department.")
            return

        if not (1 <= usn_number <= 60):
            messagebox.showerror("Invalid", "Enter USN number between 1-60.")
            return

        branch_code = DEPARTMENTS[branch]
        usn = generate_usn(branch_code, usn_number)
        room = assign_room(usn)

        if room is None:
            messagebox.showerror("Full", "All rooms are full!")
            submit_btn.config(state="disabled")
            result_label.config(text="❌ All rooms are full!")
            return

        result_label.config(text=f"✅ USN: {usn}\n🏫 Room: {room}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid number.")

submit_btn = tk.Button(root, text="Generate Room", command=on_submit,
                       font=("Verdana", 14, "bold"), bg="#3949AB", fg="white", activebackground="#283593",
                       padx=20, pady=7)
submit_btn.place(relx=0.5, y=310, anchor="n")

# Footer
footer = tk.Label(root, text="Developed by ExamCell RRCE", font=("Segoe UI", 10), bg="#d0e6f8", fg="#555")
footer.place(relx=0.5, rely=1.0, anchor="s", y=-10)

root.mainloop()
