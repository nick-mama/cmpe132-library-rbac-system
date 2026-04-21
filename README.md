# CMPE 132 Library RBAC System

This project is a web-based library access control system built for CMPE 132 Information Security.

## Features

- User registration
- Login authentication
- Role-based access control (RBAC)
- Permission checking
- User deletion
- Password hashing with bcrypt

## Roles

- Admin
- Librarian
- Student

## Backend Setup

1. Open a terminal in the `backend` folder
2. Activate the virtual environment
3. Run:
   python app.py

The Flask server runs at:
http://127.0.0.1:5000

## Frontend

Open `index.html` in the browser using Live Server or a local web server.

## Storage

User data is stored in `backend/users.json`.

## Hashing

Passwords are hashed using bcrypt before storage.
