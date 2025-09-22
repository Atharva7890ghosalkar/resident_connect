import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pymongo import MongoClient
from datetime import datetime
from tkcalendar import DateEntry
import bcrypt
from bson import ObjectId

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["CommunityEventSystem"]
event_collection = db["events"]
registration_collection = db["registrations"]
admin_collection = db["admins"]

# Initialize sample data if collections are empty
if admin_collection.count_documents({}) == 0:
    hashed_pw = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
    admin_collection.insert_one({
        "username": "admin",
        "password": hashed_pw,
        "created_at": datetime.now()
    })

if event_collection.count_documents({}) == 0:
    event_collection.insert_many([
        {
            "title": "Community BBQ",
            "description": "Annual neighborhood barbecue with food and games",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": "18:00",
            "venue": "Community Park",
            "max_participants": 50,
            "created_at": datetime.now()
        },
        {
            "title": "Yoga Morning",
            "description": "Beginner-friendly yoga session",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": "08:00",
            "venue": "Community Center",
            "max_participants": 20,
            "created_at": datetime.now()
        }
    ])

class EventSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🏘️ Community Event System")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure colors
        self.bg_color = "#f0f8ff"
        self.button_color = "#4a7a8c"
        self.text_color = "#2d3e4f"
        
        self.root.configure(bg=self.bg_color)
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = ttk.Label(self.root, 
                         text="COMMUNITY EVENT SYSTEM", 
                         font=("Arial", 18, "bold"),
                         background=self.bg_color,
                         foreground=self.text_color)
        title.pack(pady=30)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, 
                  text="🔑 Admin Login", 
                  command=self.admin_login,
                  style="Accent.TButton").pack(pady=10, ipadx=20, ipady=10)
        
        ttk.Button(button_frame, 
                  text="👤 Resident Portal", 
                  command=self.resident_portal,
                  style="Accent.TButton").pack(pady=10, ipadx=20, ipady=10)
        
        self.style.configure("Accent.TButton", 
                           background=self.button_color, 
                           foreground="white",
                           font=("Arial", 12, "bold"))
    
    def admin_login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Admin Login")
        login_window.geometry("400x300")
        login_window.resizable(False, False)
        
        ttk.Label(login_window, text="Username:").pack(pady=10)
        self.admin_user = ttk.Entry(login_window)
        self.admin_user.pack(pady=5)
        
        ttk.Label(login_window, text="Password:").pack(pady=10)
        self.admin_pass = ttk.Entry(login_window, show="*")
        self.admin_pass.pack(pady=5)
        
        ttk.Button(login_window, 
                  text="Login", 
                  command=lambda: self.verify_admin(login_window),
                  style="Accent.TButton").pack(pady=20)
    
    def verify_admin(self, window):
        admin = admin_collection.find_one({"username": self.admin_user.get()})
        if admin and bcrypt.checkpw(self.admin_pass.get().encode('utf-8'), admin["password"]):
            window.destroy()
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def admin_panel(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Admin Panel Header
        header = ttk.Frame(self.root)
        header.pack(fill="x", pady=10)
        
        ttk.Label(header, 
                 text="ADMIN PANEL", 
                 font=("Arial", 16, "bold"),
                 background=self.bg_color,
                 foreground=self.text_color).pack(side="left", padx=20)
        
        ttk.Button(header, 
                  text="Logout", 
                  command=self.create_main_menu,
                  style="Accent.TButton").pack(side="right", padx=20)
        
        # Admin Functions
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=30)
        
        buttons = [
            ("➕ Create Event", self.create_event),
            ("📅 View Events", self.view_events_admin),
            ("👥 View Registrations", self.view_registrations),
            ("📊 Event Statistics", self.event_stats)
        ]
        
        for text, command in buttons:
            ttk.Button(button_frame, 
                      text=text, 
                      command=command,
                      style="Accent.TButton").pack(pady=10, fill="x")
    
    def create_event(self):
        event_window = tk.Toplevel(self.root)
        event_window.title("Create New Event")
        event_window.geometry("500x600")
        
        fields = [
            ("Event Title:", ttk.Entry(event_window, width=40)),
            ("Description:", scrolledtext.ScrolledText(event_window, width=40, height=5)),
            ("Date:", DateEntry(event_window, width=37, date_pattern="yyyy-mm-dd")),
            ("Time:", ttk.Entry(event_window, width=40)),
            ("Venue:", ttk.Entry(event_window, width=40)),
            ("Max Participants:", ttk.Entry(event_window, width=40))
        ]
        
        for i, (label, widget) in enumerate(fields):
            ttk.Label(event_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            widget.grid(row=i, column=1, padx=10, pady=5)
        
        def save_event():
            try:
                event_data = {
                    "title": fields[0][1].get(),
                    "description": fields[1][1].get("1.0", tk.END).strip(),
                    "date": fields[2][1].get_date().strftime("%Y-%m-%d"),
                    "time": fields[3][1].get(),
                    "venue": fields[4][1].get(),
                    "max_participants": int(fields[5][1].get()),
                    "created_at": datetime.now()
                }
                
                event_collection.insert_one(event_data)
                messagebox.showinfo("Success", "Event created successfully!")
                event_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values!")
        
        ttk.Button(event_window, 
                  text="Save Event", 
                  command=save_event,
                  style="Accent.TButton").grid(row=6, column=1, pady=10)
    
    def view_events_admin(self):
        events_window = tk.Toplevel(self.root)
        events_window.title("All Events")
        events_window.geometry("800x600")
        
        # Treeview for events
        tree = ttk.Treeview(events_window, columns=("ID", "Title", "Date", "Time", "Venue", "Participants"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Venue", text="Venue")
        tree.heading("Participants", text="Participants")
        
        tree.column("ID", width=50)
        tree.column("Title", width=150)
        tree.column("Date", width=100)
        tree.column("Time", width=80)
        tree.column("Venue", width=150)
        tree.column("Participants", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(events_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate with events
        for event in event_collection.find():
            reg_count = registration_collection.count_documents({"event_id": str(event["_id"])})
            tree.insert("", "end", values=(
                str(event["_id"]),
                event["title"],
                event["date"],
                event["time"],
                event["venue"],
                f"{reg_count}/{event['max_participants']}"
            ))
    
    def view_registrations(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Event Registrations")
        reg_window.geometry("800x600")
        
        # Get events for dropdown
        events = list(event_collection.find())
        event_options = [f"{event['title']} ({event['date']})" for event in events]
        
        ttk.Label(reg_window, text="Select Event:").pack(pady=10)
        event_var = tk.StringVar()
        event_dropdown = ttk.Combobox(reg_window, textvariable=event_var, values=event_options, state="readonly")
        event_dropdown.pack(pady=5)
        
        # Treeview for registrations
        tree = ttk.Treeview(reg_window, columns=("Name", "Email", "Event"), show="headings")
        tree.heading("Name", text="Resident Name")
        tree.heading("Email", text="Email")
        tree.heading("Event", text="Event")
        
        tree.column("Name", width=150)
        tree.column("Email", width=200)
        tree.column("Event", width=250)
        
        scrollbar = ttk.Scrollbar(reg_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def load_registrations():
            tree.delete(*tree.get_children())
            selected = event_var.get()
            if not selected:
                return
            
            # Find the selected event
            event_title = selected.split(" (")[0]
            event = event_collection.find_one({"title": event_title})
            
            if event:
                registrations = registration_collection.find({"event_id": str(event["_id"])})
                for reg in registrations:
                    tree.insert("", "end", values=(
                        reg["resident_name"],
                        reg["email"],
                        f"{event['title']} ({event['date']})"
                    ))
        
        ttk.Button(reg_window, 
                  text="Load Registrations", 
                  command=load_registrations,
                  style="Accent.TButton").pack(pady=10)
    
    def event_stats(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Event Statistics")
        stats_window.geometry("600x400")
        
        text = scrolledtext.ScrolledText(stats_window, width=70, height=20)
        text.pack(pady=10)
        
        text.insert(tk.END, "📊 EVENT STATISTICS\n\n")
        
        # Total events
        total_events = event_collection.count_documents({})
        text.insert(tk.END, f"Total Events: {total_events}\n\n")
        
        # Events with most registrations
        text.insert(tk.END, "Most Popular Events:\n")
        pipeline = [
            {"$group": {"_id": "$event_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        top_events = list(registration_collection.aggregate(pipeline))
        
        for i, event in enumerate(top_events, 1):
            e = event_collection.find_one({"_id": ObjectId(event["_id"])})
            if e:
                text.insert(tk.END, f"{i}. {e['title']} - {event['count']} registrations\n")
        
        text.config(state=tk.DISABLED)
    
    def resident_portal(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Resident Portal Header
        header = ttk.Frame(self.root)
        header.pack(fill="x", pady=10)
        
        ttk.Label(header, 
                 text="RESIDENT PORTAL", 
                 font=("Arial", 16, "bold"),
                 background=self.bg_color,
                 foreground=self.text_color).pack(side="left", padx=20)
        
        ttk.Button(header, 
                  text="Back", 
                  command=self.create_main_menu,
                  style="Accent.TButton").pack(side="right", padx=20)
        
        # Available Events
        ttk.Label(self.root, 
                 text="Available Events:", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Treeview for events
        tree = ttk.Treeview(self.root, columns=("Title", "Date", "Time", "Venue", "Spaces"), show="headings")
        tree.heading("Title", text="Title")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Venue", text="Venue")
        tree.heading("Spaces", text="Available Spaces")
        
        tree.column("Title", width=200)
        tree.column("Date", width=100)
        tree.column("Time", width=80)
        tree.column("Venue", width=150)
        tree.column("Spaces", width=100)
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate with events
        for event in event_collection.find():
            reg_count = registration_collection.count_documents({"event_id": str(event["_id"])})
            spaces = event["max_participants"] - reg_count
            tree.insert("", "end", values=(
                event["title"],
                event["date"],
                event["time"],
                event["venue"],
                f"{spaces}/{event['max_participants']}"
            ))
        
        # Registration Frame
        reg_frame = ttk.Frame(self.root)
        reg_frame.pack(fill="x", pady=20)
        
        ttk.Button(reg_frame, 
                  text="Register for Selected Event", 
                  command=lambda: self.register_for_event(tree),
                  style="Accent.TButton").pack(pady=10)
    
    def register_for_event(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event first!")
            return
        
        event_data = tree.item(selected)["values"]
        event_title = event_data[0]
        
        # Check if there are spaces available
        spaces = event_data[4].split("/")
        if int(spaces[0]) <= 0:
            messagebox.showerror("Error", "This event is already full!")
            return
        
        # Registration form
        reg_window = tk.Toplevel(self.root)
        reg_window.title(f"Register for {event_title}")
        reg_window.geometry("400x300")
        
        ttk.Label(reg_window, text="Your Name:").pack(pady=5)
        name_entry = ttk.Entry(reg_window)
        name_entry.pack(pady=5)
        
        ttk.Label(reg_window, text="Your Email:").pack(pady=5)
        email_entry = ttk.Entry(reg_window)
        email_entry.pack(pady=5)
        
        def submit_registration():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            
            if not name or not email:
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            # Find the event
            event = event_collection.find_one({"title": event_title})
            
            # Check if already registered
            existing = registration_collection.find_one({
                "email": email,
                "event_id": str(event["_id"])
            })
            
            if existing:
                messagebox.showwarning("Warning", "You're already registered for this event!")
                return
            
            # Save registration
            registration_collection.insert_one({
                "resident_name": name,
                "email": email,
                "event_id": str(event["_id"]),
                "registered_at": datetime.now()
            })
            
            messagebox.showinfo("Success", "Registration successful!")
            reg_window.destroy()
            self.resident_portal()  # Refresh the view
        
        ttk.Button(reg_window, 
                  text="Submit Registration", 
                  command=submit_registration,
                  style="Accent.TButton").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = EventSystem(root)
    root.mainloop()