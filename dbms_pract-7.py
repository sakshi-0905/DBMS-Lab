import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
# ---------------- Database Connection ----------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="Sakshi@2005",       
        database="student_db" 
    )
# ---------------- CRUD Operations ----------------
def add_record():
    if name_entry.get() == "" or age_entry.get() == "" or course_entry.get() == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    con = connect_db()
    cur = con.cursor()
    cur.execute("INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
                (name_entry.get(), age_entry.get(), course_entry.get()))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Record added successfully!")
    clear_fields()
    show_records()

def show_records():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    con.close()
    # Clear old records
    for i in table.get_children():
        table.delete(i)
    # Insert new records
    for row in rows:
        table.insert("", "end", values=row)

def delete_record():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a record to delete")
        return
    data = table.item(selected, "values")
    con = connect_db()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (data[0],))
    con.commit()
    con.close()
    messagebox.showinfo("Deleted", "Record deleted successfully!")
    show_records()

def edit_record():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a record to edit")
        return
    data = table.item(selected, "values")
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    course_entry.delete(0, END)
    name_entry.insert(0, data[1])
    age_entry.insert(0, data[2])
    course_entry.insert(0, data[3])
    update_btn.config(state=NORMAL)
    add_btn.config(state=DISABLED)
    delete_btn.config(state=DISABLED)
    table.config(selectmode="none")
    global edit_id
    edit_id = data[0]

def update_record():
    con = connect_db()
    cur = con.cursor()
    cur.execute("UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
                (name_entry.get(), age_entry.get(), course_entry.get(), edit_id))
    con.commit()
    con.close()
    messagebox.showinfo("Updated", "Record updated successfully!")
    clear_fields()
    update_btn.config(state=DISABLED)
    add_btn.config(state=NORMAL)
    delete_btn.config(state=NORMAL)
    table.config(selectmode="browse")
    show_records()

def clear_fields():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    course_entry.delete(0, END)

# ---------------- GUI ----------------
root = Tk()
root.title("Student Database Management System")
root.geometry("650x500")
# Beautiful background color
root.config(bg="#2c3e50")  # Dark bluish background
title = Label(root, text="Student Database Management System", font=("Arial", 18, "bold"),
              bg="#2c3e50", fg="#ecf0f1")  # Light text on dark background
title.pack(pady=10)
# Input Frame
frame = Frame(root, bg="#34495e")  # Slightly lighter dark blue
frame.pack(pady=10)
Label(frame, text="Name:", bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(frame, width=25)
name_entry.grid(row=0, column=1, padx=10, pady=5)
Label(frame, text="Age:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, padx=10, pady=5)
age_entry = Entry(frame, width=25)
age_entry.grid(row=1, column=1, padx=10, pady=5)
Label(frame, text="Course:", bg="#34495e", fg="#ecf0f1").grid(row=2, column=0, padx=10, pady=5)
course_entry = Entry(frame, width=25)
course_entry.grid(row=2, column=1, padx=10, pady=5)
# Button Frame
btn_frame = Frame(root, bg="#2c3e50")
btn_frame.pack(pady=10)
add_btn = Button(btn_frame, text="Add", width=10, command=add_record, bg="#1abc9c", fg="white")
add_btn.grid(row=0, column=0, padx=10)
show_btn = Button(btn_frame, text="Show", width=10, command=show_records, bg="#3498db", fg="white")
show_btn.grid(row=0, column=1, padx=10)
edit_btn = Button(btn_frame, text="Edit", width=10, command=edit_record, bg="#9b59b6", fg="white")
edit_btn.grid(row=0, column=2, padx=10)
update_btn = Button(btn_frame, text="Update", width=10, command=update_record, bg="#f1c40f", fg="black", state=DISABLED)
update_btn.grid(row=0, column=3, padx=10)
delete_btn = Button(btn_frame, text="Delete", width=10, command=delete_record, bg="#e74c3c", fg="white")
delete_btn.grid(row=0, column=4, padx=10)
# Table Frame
table_frame = Frame(root, bg="#2c3e50")
table_frame.pack(pady=10)
columns = ("ID", "Name", "Age", "Course")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
# Define headings
table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("Age", text="Age")
table.heading("Course", text="Course")
# Define column widths
table.column("ID", width=50, anchor=CENTER)
table.column("Name", width=150, anchor=CENTER)
table.column("Age", width=100, anchor=CENTER)
table.column("Course", width=150, anchor=CENTER)
# Add scrollbar
scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
table.pack(fill=BOTH)

root.mainloop()
