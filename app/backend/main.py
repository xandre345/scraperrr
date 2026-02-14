from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .services import DataService
from .models import ArticleList
import uvicorn
import os

app = FastAPI(title="AI News Dashboard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get absolute path to frontend directory
# Works in both local dev and Vercel's serverless environment
_this_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(_this_dir, '..', 'frontend')
if not os.path.isdir(frontend_path):
    # Fallback: resolve relative to the project root (Vercel layout)
    frontend_path = os.path.join(os.getcwd(), 'app', 'frontend')
frontend_path = os.path.abspath(frontend_path)

# Mount static files (css, js, assets)
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

# Initialize DataService
data_service = DataService()

@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/api/articles", response_model=ArticleList)
def get_articles():
    """Fetch all articles from all sources"""
    try:
        articles = data_service.fetch_all_articles()
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
