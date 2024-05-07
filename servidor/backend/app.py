from fastapi import FastAPI, Depends, Request, HTTPException
import os
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


dir = os.path.dirname(__file__)
#
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="../frontend/templates") # Path to the template folder

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# async def root(request: Request, db: Session = Depends(get_db)):
#     return templates.TemplateResponse("index.html", {"request": request})


@app.get("/")
async def root():
    return "hola"


@app.post("/add_gas")
async def add_gas(accelerometer: schemas.Accelerometer, db: Session = Depends(get_db)):    
    crud.add_information_accelerometer(db, accelerometer)
    return HTTPException(status_code=200, detail="added accelerometer")


@app.post("/add_fire")
async def add_fire(magnetometer: schemas.Magnetometer, db: Session = Depends(get_db)):
    #print(magnetometer)
    crud.add_information_magnetometer(db, magnetometer)
    return HTTPException(status_code=200, detail="added magnetometer")

# ----------------------------

@app.get("/send_sprinkler")
async def send_sprinkler(gps: schemas.GPS, db: Session = Depends(get_db)):
    crud.add_information_gps(db, gps)
    return HTTPException(status_code=200, detail="added gps")


@app.get("/send_lcd")
async def send_lcd(gyroscope: schemas.Gyroscope, db: Session = Depends(get_db)):
    crud.add_information_gyroscope(db, gyroscope)
    return HTTPException(status_code=200, detail="added gyroscope")


@app.get("/send_buzzer")
async def send_buzzer(lightSensor: schemas.LightSensor, db: Session = Depends(get_db)):
    crud.add_information_lightSensor(db, lightSensor)
    return HTTPException(status_code=200, detail="added lightSensor")


@app.get("/gas")
async def get_gas(request: Request, db: Session = Depends(get_db)):

    records = crud.get_information_accelerometer(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
        x_values = [records.x for records in records]
        y_values = [records.y for records in records]
        z_values = [records.z for records in records]
    else:
        return HTTPException(status_code=404, detail="No data found")

    return templates.TemplateResponse("accelerometer.html", {"request": request, "times": time, "x_values": x_values, "y_values": y_values, "z_values": z_values})

@app.get("/fire")
async def get_fire(request: Request, db: Session = Depends(get_db)):

    records = crud.get_information_magnetometer(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
        x_values = [records.x for records in records]
        y_values = [records.y for records in records]
        z_values = [records.z for records in records]
    
    else:
        return HTTPException(status_code=404, detail="No data found")
    
    return templates.TemplateResponse("magnetometer.html", {"request": request, "times": time, "x_values": x_values, "y_values": y_values, "z_values": z_values})