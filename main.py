from fastapi import FastAPI
from database import get_db
from load_databases import load_databases
from routers.api import router
app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    db = get_db()
    load_databases(db)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
