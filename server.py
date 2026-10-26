from fastapi import FastAPI
import uvicorn
from endpoints import router


app = FastAPI(
    title="Tasks Server",
    description="Здесь собранны ваши задачи",
    version="0.01"
)

app.include_router(router)

if __name__=="__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)