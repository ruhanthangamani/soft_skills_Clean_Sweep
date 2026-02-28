# Clean Sweep 🧹

A civic-tech platform that connects organizers (panchayats, NGOs, colleges) with citizens to manage and participate in clean-up drives.

## 🚀 Features

- **Organizers**: Create and manage clean-up events, track volunteers.
- **Volunteers**: Browse events, sign up for drives, track participation history.
- **Civic Focus**: Designed for real-world impact with a professional, clean UI.

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3 (Custom Design System), Vanilla JavaScript (Modular).
- **Backend**: Python (Flask).
- **Database**: SQLite.
- **Design**: Modern, responsive, mobile-first. Fonts: Proxima Nova (fallback Montserrat), Open Sans.

## 📂 Project Structure

```
clean-sweep/
│
├── frontend/           # Static assets and UI
│   ├── index.html      # Landing Page
│   ├── browse.html     # Find Drives
│   ├── css/            # Custom Styles
│   ├── js/             # Application Logic
│   └── assets/         # Images & Icons
│
├── backend/            # API Server
│   ├── app.py          # Entry point
│   ├── routes/         # API Endpoints
│   ├── models/         # Database Helpers
│   └── config/         # Configuration
│
└── database/           # Data Storage
    └── schema.sql      # Database Schema
```

## ⚡ How to Run

1. **Prerequisites**: Python 3.x installed.
2. **Setup**:
   ```bash
   cd clean-sweep/backend
   pip install flask
   ```
3. **Run Server**:
   ```bash
   python app.py
   ```
4. **Access App**:
   Open browser at `http://localhost:5000`

## 🔑 Demo Credentials

You can register a new account on the homepage:
- **Organizer**: Select "Organize Events" during signup.
- **Volunteer**: Select "Volunteer" during signup.

---
Built with ❤️ for a cleaner future.
