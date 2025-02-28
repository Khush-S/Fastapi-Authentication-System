FastAPI Authentication System
This is a simple authentication system built using FastAPI, which supports user registration, login, and logout functionalities. It interacts with a MySQL database to store user credentials, and it uses SHA-256 for password hashing (though you are encouraged to use more secure algorithms such as bcrypt for production).

Features:
User Signup: Allows users to register by providing their username, email, and password.
User Login: Authenticates users by checking the email and password.
Welcome Page: Displays a welcome page after successful login.
Logout: Clears the session and redirects to the login page.
Requirements
To run this project, you will need the following:

Python 3.7+
FastAPI
Uvicorn (for development server)
MySQL (to store user data)
Install required dependencies:
bash
Copy
pip install fastapi uvicorn mysql-connector
Database Setup
Before running the application, ensure you have a MySQL database set up with the following structure:

1. Create the Database:
sql
Copy
CREATE DATABASE user_data;
2. Create the users Table:
sql
Copy
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    pass_word VARCHAR(255) NOT NULL
);
Configuration
In the get_db_connection() function, ensure that your MySQL credentials are set correctly (e.g., host, user, password, database).

python
Copy
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",      # Database host
        user="root",           # MySQL username
        password="Jk@2343",    # MySQL password
        database="user_data"   # Database name
    )
    return connection
Running the Application
1. Run the application using uvicorn:
bash
Copy
uvicorn main:app --reload
The server will start at http://127.0.0.1:8000/.

2. Routes
GET /: Displays the login form (login.html).
GET /signup: Displays the signup form (signup.html).
POST /login: Accepts email and password as form data, authenticates the user, and redirects to the welcome page (welcome.html) if credentials are correct.
POST /signup: Accepts username, email, and password as form data, creates a new user, and redirects to the login page.
GET /welcome: Displays the welcome page after a successful login.
GET /logout: Logs the user out and redirects them to the login page.
Password Hashing
In this module, we are using SHA-256 to hash passwords, but it's important to note that SHA-256 is not a recommended algorithm for password hashing due to its vulnerability to brute force attacks. In production, it's better to use secure algorithms such as bcrypt or argon2.

Example of how to change to bcrypt (recommended for production):

Install bcrypt:

bash
Copy
pip install bcrypt
Modify the password hashing logic:

python
Copy
import bcrypt

# Hash the password during signup
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Compare the entered password with the stored hash
if bcrypt.checkpw(password.encode(), entered_password.encode()):
    # passwords match
Folder Structure
Here is the basic structure of the project:

bash
Copy
/fastapi-auth-system
│
├── main.py                  # FastAPI application (this file)
├── templates/
│   ├── login.html           # Login page template
│   ├── signup.html          # Signup page template
│   └── welcome.html         # Welcome page template
├── requirements.txt         # List of dependencies (for deployment)
└── README.md                # Project documentation
Templates
login.html: A form where users input their email and password to log in.
signup.html: A form where users input their username, email, and password to register.
welcome.html: Displays a welcome message after the user successfully logs in.
Error Handling
The application will raise HTTPException in case of invalid login credentials. If the provided email doesn't exist in the database or the passwords don't match, a 400 error with the message "Invalid credentials" will be returned.

Logout
When users log out, the session is cleared, and they are redirected to the login page. The current implementation does not handle sessions or tokens; it's simply a redirect after logout.

