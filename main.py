
import os
from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv



import bcrypt
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



@app.get("/")
def home():
    return {"message": "Welcome to School Management API"}


class UserRegister(BaseModel):
    email: str
    password: str
    role: str  # admin, teacher, student, parent
@app.post("/register")
async def register(user: UserRegister):
    try:
        # Attempt to sign up the user
        response = supabase.auth.sign_up({"email": user.email, "password": user.password})

        # Check if the response contains an error message
        if 'error' in response:
            error_message = response['error']
            print("Error message:", error_message)
            raise HTTPException(status_code=400, detail=error_message)

        # If no error, registration is successful
        return {"message": "User registered successfully"}

    except Exception as e:
        # Log the exception and raise a 500 error for debugging
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=404, detail="Internal server error")




class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(user: UserLogin):
    try:
        # Attempt to sign in the user
        response = supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})

        # Check if there's an error in the response
        if response.user is None:  # If no user is found in the response
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        # If login is successful, return the access token
        return {"token": response.session.access_token}

    except Exception as e:
        # Log the exception and raise a 500 error for debugging
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=404, detail="Internal server error")



class Student(BaseModel):
    name: str
    email: str
    grade: str
    parent_email: str

@app.post("/students/")
async def add_student(student: Student):
    try:
        # Insert the student into the 'students' table
        response = supabase.table("students").insert(student.dict()).execute()

        # Log the response for debugging purposes
        print(f"Response occurred: {response}")

        # If there's an error in the response, raise an HTTPException
        if response.get("error"):
            raise HTTPException(status_code=400, detail="Failed to add student")

        return {"message": "Student added successfully"}
    
    except Exception as e:
        # Catch any exception and return a 500 Internal Server Error response
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=404, detail="Internal server error")



class Attendance(BaseModel):
    student_id: str
    date: str
    status: str  # present, absent, late


@app.post("/attendance/")
async def mark_attendance(attendance: Attendance):
    response = supabase.table("attendance").insert(attendance.dict()).execute()
    return {"message": "Attendance recorded"}
