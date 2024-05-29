from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from os import getenv
from auth import get_current_user
from routers import todo, user

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router, prefix="/todos", tags=["todos"])
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the TODO app"}

if __name__ == "__main__":
    import uvicorn
    port=int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port,reload=True)