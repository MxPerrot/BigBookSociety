from fastapi import FastAPI

app = FastAPI()

#https://fastapi.tiangolo.com/tutorial/first-steps/

@app.get("/")
async def root():
    return {"message": "Hello World"}