import tkinter as tk
from tkinter import messagebox

# Predefined email and password
VALID_EMAIL = "atharvaghosalkar22@.com"
VALID_PASSWORD = "Atharva123"

# Function to validate login
def validate_login():
    email = email_entry.get()
    password = password_entry.get()

    # Check if '@' is present in the email
    if "@" not in email:
        messagebox.showerror("Error", "Invalid Mail ID")
        return
    
    # Check if email matches
    if email != VALID_EMAIL:
        messagebox.showerror("Error", "Email ID is not matching")
        return
    
    # Check if password matches
    if password != VALID_PASSWORD:
        messagebox.showerror("Error", "Wrong Password")
        return

    # If all conditions pass
    messagebox.showinfo("Success", "Access Granted!")

# Create main window
root = tk.Tk()
root.title("Login System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Email Label and Entry
email_label = tk.Label(root, text="Enter Email ID:", font=("Arial", 12), bg="#f0f0f0")
email_label.pack(pady=5)
email_entry = tk.Entry(root, width=30, font=("Arial", 12))
email_entry.pack(pady=5)

# Password Label and Entry
password_label = tk.Label(root, text="Enter Password:", font=("Arial", 12), bg="#f0f0f0")
password_label.pack(pady=5)
password_entry = tk.Entry(root, width=30, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

# Login Button
login_button = tk.Button(root, text="Login", command=validate_login, font=("Arial", 12, "bold"), bg="#4caf50", fg="white")
login_button.pack(pady=20)

root.mainloop()
