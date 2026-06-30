from fastapi import FastAPI

app = FastAPI(title="ELEV Finance Agent")

@app.get("/health")
def health():
    return {"status": "ok"}
