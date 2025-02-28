from fastapi import FastAPI, Form, HTTPException, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
import hashlib

# Initialize FastAPI application and Jinja2 templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Function to establish a connection to the MySQL database
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",      # Database host
        user="root",           # MySQL username
        password="enter_your_database _password",    # MySQL password
        database="user_data"   # Database name
    )
    return connection

# Route to display the login form
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Route to display the signup form
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Route to display the welcome page after a successful login
@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

# Route to handle login logic
@app.post("/login")
async def handle_login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Establish a connection to the database and query for the user
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # If the user is not found, return an error
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Retrieve the stored password and hash the entered password for comparison
    entered_password = str(user.get("pass_word", ""))  # Safely get the password field
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the entered password

    # If passwords match, redirect to the welcome page; otherwise, return an error
    if entered_password == hashed_password:
        return templates.TemplateResponse("welcome.html", {"request": request})
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

# Route to handle user signup (register a new user)
@app.post("/signup")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Establish a connection to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Hash the password before storing it in the database
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert the new user data into the database
    cursor.execute("INSERT INTO users (username, email, pass_word) VALUES (%s, %s, %s)", (username, email, hashed_password))
    connection.commit()

    cursor.close()
    connection.close()

    # Redirect the user to the login page after signup
    return RedirectResponse(url="/", status_code=303)

# Route to handle user logout and clear session data
@app.get("/logout")
async def logout(response: Response):
    return RedirectResponse(url="/", status_code=303)
