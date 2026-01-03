from fastapi import FastAPI
# OLD LINE: from api.v1.endpoints import routes 
# NEW LINE (Absolute Import):
from app.api.v1.endpoints import routes 

app = FastAPI(title="TravelMate Government API")

app.include_router(routes.router, prefix="/api/v1", tags=["Routes"])

@app.get("/")
def read_root():
    return {"message": "J&K Travel Safety System Active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)