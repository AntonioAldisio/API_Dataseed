from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from model.models import User

app = FastAPI()

@app.get("/")
def hello(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)