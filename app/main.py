from fastapi import FastAPI
from app.routers import post, user, vote, auth

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message":"Hello, world!"}