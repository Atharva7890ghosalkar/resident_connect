import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Apartment"]
complaint_collection = db["complaints"]

# Admin Credentials
ADMIN_USERNAME = "Atharva"
ADMIN_PASSWORD = "Atharva123"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "atharvaghosalkar22@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "wwdkliamzlgjfyby"  # Replace with your email app password

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending email:", e)

def update_complaint_status(complaint_id, new_status, app):
    complaint = complaint_collection.find_one({"_id": ObjectId(complaint_id)})
    if complaint:
        complaint_collection.update_one({"_id": ObjectId(complaint_id)}, {"$set": {"status": new_status}})
        messagebox.showinfo("Success", "Complaint status updated successfully!")
        
        # Send email notification
        resident_email = complaint.get("contact_info")
        subject = "Complaint Status Updated"
        body = (f"Dear {complaint['resident_name']},\n\n"
                f"Your complaint submitted on {complaint['timestamp']} has been updated.\n"
                f"Complaint: {complaint['complaint_text']}\n"
                f"Current Status: {new_status}\n\n"
                f"Thank you for your patience.\n\n"
                f"Regards,\n"
                f"Apartment Management Team")
        send_email(resident_email, subject, body)
        
        app.view_complaints()

def view_complaints(app):
    for widget in app.admin_tab.winfo_children():
        widget.destroy()
    
    app.text_area = scrolledtext.ScrolledText(app.admin_tab, wrap=tk.WORD, width=70, height=20, font=("Arial", 11), bg="#e8f5e9")
    app.text_area.pack(pady=10)
    
    complaints = list(complaint_collection.find())
    
    if not complaints:
        app.text_area.insert(tk.END, "😞 No complaints found!")
        return

    for complaint in complaints:
        complaint_details = (
            f"🏢 Resident Name: {complaint['resident_name']}\n"
            f"🏠 Room Number: {complaint['room_number']}\n"
            f"📧 Contact: {complaint['contact_info']}\n"
            f"📝 Complaint: {complaint['complaint_text']}\n"
            f"📅 Submitted On: {complaint['timestamp']}\n"
            f"🔄 Status: {complaint['status']}\n"
            f"{'-' * 50}\n"
        )
        app.text_area.insert(tk.END, complaint_details)
        
        frame = tk.Frame(app.admin_tab)
        frame.pack(pady=2)
        
        status_var = tk.StringVar(value=complaint['status'])
        status_dropdown = ttk.Combobox(frame, textvariable=status_var, values=["Pending", "Processing", "Resolved"], state="readonly")
        status_dropdown.pack(side=tk.LEFT)
        
        update_button = tk.Button(
            frame, text="Update Status", command=lambda c_id=complaint['_id'], s=status_var: update_complaint_status(str(c_id), s.get(), app)
        )
        update_button.pack(side=tk.LEFT, padx=5)

    refresh_button = tk.Button(
        app.admin_tab,
        text="🔄 Refresh Complaints",
        command=lambda: view_complaints(app),
        bg="#2196F3",
        fg="white",
        font=("Arial", 12, "bold"),
    )
    refresh_button.pack(pady=5)

def admin_login(app):
    login_window = tk.Toplevel()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def check_login():
        if username_entry.get() == ADMIN_USERNAME and password_entry.get() == ADMIN_PASSWORD:
            messagebox.showinfo("Login Successful", "Welcome, Admin! 🎉")
            login_window.destroy()
            app.create_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password!")

    login_button = tk.Button(login_window, text="Login", command=check_login)
    login_button.pack(pady=10)

class ComplaintManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Apartment Complaint Management System")
        self.root.geometry("750x500")
        self.root.configure(bg="#f0f0f0")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.create_login_tab()

    def create_login_tab(self):
        self.login_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.login_tab, text="🔑 Admin Login")

        login_button = tk.Button(
            self.login_tab,
            text="Login as Admin",
            command=lambda: admin_login(self),
            bg="#2196F3",
            fg="white",
            font=("Arial", 14, "bold"),
        )
        login_button.pack(pady=50)

    def create_admin_panel(self):
        self.admin_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.admin_tab, text="📄 View Complaints")
        view_complaints(self)

if __name__ == "__main__":
    root = tk.Tk()
    app = ComplaintManagementApp(root)
    root.mainloop()