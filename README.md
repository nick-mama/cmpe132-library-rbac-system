# CMPE 132 Library RBAC System

This project is a web-based access control system for a fictional library (SJSU_Library), built for CMPE 132 Information Security. The system demonstrates user provisioning, authentication, and authorization using a Role-Based Access Control (RBAC) model.

---

## Features

- User registration (provisioning)
- Login authentication
- Role-based access control (RBAC)
- Permission checking
- User deletion (de-provisioning)
- Password hashing using bcrypt

---

## Roles and Permissions

### Admin

- add_user
- delete_user
- view_books

### Librarian

- view_books
- manage_books

### Student

- view_books

---

## Technologies Used

- Backend: Python (Flask)
- Frontend: HTML + React (via CDN)
- Security: bcrypt for password hashing
- Storage: JSON file (`users.json`)

---

``md

## Backend Setup

1. Navigate to the backend folder:

```
cd backend
```

2. (Optional) Activate virtual environment (windows):

```
.\venv\Scripts\activate
```

3. Install dependencies:

```
pip install flask flask-cors bcrypt
```

4. Run the server:

```
python app.py
```

The Flask server runs at http://127.0.0.1:5000

---

``md

## Frontend

Open the frontend by launching:

```
index.html
```

```

You can:
- Open it directly in a browser
- Use VS Code Live Server

---

## API Endpoints

- POST `/register` → Create a new user
- POST `/login` → Authenticate user
- POST `/check-permission` → Check permissions
- POST `/delete-user` → Delete a user

---

``md
## Data Storage

User data is stored in:
```

backend/users.json

```

```

Each user record includes:

- username
- hashed password
- role

---

## Password Security

Passwords are hashed using **bcrypt** before storage.

bcrypt includes salting, which ensures:

- identical passwords produce different hashes
- improved protection against attacks

---

## Use of AI Tools

Claude.ai was used to assist in generating the frontend user interface, including layout and form structure.  
All backend logic, authentication, RBAC implementation, and security features were implemented independently.

---

## Notes

- This project is for educational purposes.
- The system is simplified for demonstration of access control concepts.
