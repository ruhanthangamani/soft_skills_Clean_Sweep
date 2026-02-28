-- Database Schema for Clean Sweep

-- Users Table (Organizers and Volunteers)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('organizer', 'volunteer')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events Table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organizer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    date TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'Clean-up Drive',
    image_url TEXT,
    status TEXT DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

-- Signups Table (Volunteers joining events)
CREATE TABLE IF NOT EXISTS signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    volunteer_id INTEGER NOT NULL,
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, volunteer_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (volunteer_id) REFERENCES users(id)
);
