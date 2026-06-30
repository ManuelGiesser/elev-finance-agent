from fastapi import FastAPI

app = FastAPI(title="ELEV Finance Agent")

@app.get("/health")
def health():
    return {"status": "ok", "service": "elev-finance-agent"}

@app.get("/")
def root():
    return {"name": "ELEV Finance Agent", "version": "0.1.0"}
