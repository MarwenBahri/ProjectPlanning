from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, column, project, team, ticket, user

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(column.router)
app.include_router(project.router)
app.include_router(team.router)
app.include_router(ticket.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message":  "welcome"}



