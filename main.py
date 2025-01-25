from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from db.database import init_db, get_user_by_username, create_user, save_query
from vectorstore.vectorstore import query_documents
from utils.auth import hash_password, verify_password
import logging

# Initialize the FastAPI app
app = FastAPI()

# Initialize Database and Pinecone on Startup
#@app.on_event("startup")
#async def startup():
#    init_db()
#    upload_documents_to_pinecone("data/")  # Process and upload PDFs to Pinecone

# Models for API requests
class UserRequest(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    query: str

# Routes for Signup, Login, and Chat
@app.post("/signup")
async def signup(user_request: UserRequest):
    if get_user_by_username(user_request.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user_request.password)
    create_user(user_request.username, hashed_password)
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user_request: UserRequest):
    user = get_user_by_username(user_request.username)
    if not user or not verify_password(user_request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.post("/chat")
async def chat(query_request: QueryRequest):
    try:
        # Get a response based on research papers
        response = query_documents(query_request.query)
        return {"response": response}
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Serve Frontend Pages
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_signup():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/login", response_class=HTMLResponse)
async def serve_login():
    with open("templates/login.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/chat-ui", response_class=HTMLResponse)
async def serve_chat():
    with open("templates/chat.html") as f:
        return HTMLResponse(content=f.read())
