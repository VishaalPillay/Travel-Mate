from fastapi import FastAPI

app = FastAPI(title="Travel-Mate Backend Engine")

@app.get("/")
async def root():
    return {"message": "Welcome to Travel-Mate API"}
