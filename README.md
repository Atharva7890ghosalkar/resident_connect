# resident_connect



## Overview
This Python-based Apartment Management System provides a complete solution for apartment administration and resident services. It includes complaint management, event registration, and admin-resident interactions with a Tkinter GUI and MongoDB for persistent storage.

## Features
### Resident Panel
- **Submit Complaint:** Residents can submit complaints with details.
- **Event Registration:** View and register for community events.

### Admin Panel
- **Login Authentication:** Secure admin login to access the system.
- **View Complaints:** See all submitted complaints, update their status (Pending, Processing, Resolved), and send email notifications to residents.
- **Manage Events:** Add, edit, and delete community events, track resident registrations.

### Technical Features
- **GUI:** Tkinter-based desktop interface.
- **Database:** MongoDB for storing complaints, residents, and events.
- **Email Notifications:** Automated emails sent to residents when complaint statuses are updated.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Atharva7890ghosalkar/resident_connect.git

Install required Python packages:
bash
Copy code
pip install pymongo tk smtplib email-validator
Set up MongoDB and update the connection string in the code.

Usage:
Run the main application file:
bash
Copy code
python Complaint_Management.py
Use the Resident panel to submit complaints or register for events.

Admins can log in to manage complaints and events.

Future Enhancements:
Mobile app integration.
Chatbot for quick resident queries.
Advanced analytics for admin insights