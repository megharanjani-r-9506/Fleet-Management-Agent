from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Fleet Maintenance System Running"}