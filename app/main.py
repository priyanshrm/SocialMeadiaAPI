from fastapi import FastAPI
from app.routers import post, user, vote, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]  # wildcard "every single domain or website"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message":"Hello, world!"}