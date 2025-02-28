from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import base64
from io import BytesIO
import os
from sqlalchemy.orm import Session
from models import SessionLocal, WifiSettings

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 절대 경로로 templates와 static 폴더 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Default credentials - in production, use a secure database
WIFI_CREDENTIALS = {
    "ssid": "DefaultSSID",
    "password": "DefaultPassword"
}

ADMIN_PASSWORD = "password"  # Change this to a secure password

def generate_wifi_qr(ssid: str, password: str) -> str:
    wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(wifi_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    settings = db.query(WifiSettings).first()
    qr_code = generate_wifi_qr(settings.ssid, settings.password)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "ssid": settings.ssid,
        "password": settings.password,
        "qr_code": qr_code
    })

@app.get("/edit", response_class=HTMLResponse)
async def edit_page(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})

@app.post("/update")
async def update_credentials(
    admin_password: str = Form(...),
    ssid: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Invalid admin password")
    
    settings = db.query(WifiSettings).first()
    settings.ssid = ssid
    settings.password = password
    db.commit()
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    print(f"Templates directory: {os.path.join(BASE_DIR, 'templates')}")
    uvicorn.run(app, host="127.0.0.1", port=8001)
