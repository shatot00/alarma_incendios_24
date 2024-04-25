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


@app.post("/add_accelerometer")
async def add_accelerometer(accelerometer: schemas.Accelerometer, db: Session = Depends(get_db)):    
    crud.add_information_accelerometer(db, accelerometer)
    return HTTPException(status_code=200, detail="added accelerometer")


@app.post("/add_magnetometer")
async def add_magnetometer(magnetometer: schemas.Magnetometer, db: Session = Depends(get_db)):
    #print(magnetometer)
    crud.add_information_magnetometer(db, magnetometer)
    return HTTPException(status_code=200, detail="added magnetometer")


@app.post("/add_gps")
async def add_gps(gps: schemas.GPS, db: Session = Depends(get_db)):
    crud.add_information_gps(db, gps)
    return HTTPException(status_code=200, detail="added gps")


@app.post("/add_gyroscope")
async def add_gyroscope(gyroscope: schemas.Gyroscope, db: Session = Depends(get_db)):
    crud.add_information_gyroscope(db, gyroscope)
    return HTTPException(status_code=200, detail="added gyroscope")


@app.post("/add_lightSensor")
async def add_lightSensor(lightSensor: schemas.LightSensor, db: Session = Depends(get_db)):
    crud.add_information_lightSensor(db, lightSensor)
    return HTTPException(status_code=200, detail="added lightSensor")


@app.get("/accelerometer")
async def get_accelerometer(request: Request, db: Session = Depends(get_db)):

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



@app.get("/magnetometer")
async def get_magnetometer(request: Request, db: Session = Depends(get_db)):

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


@app.get("/gps")
async def get_gps(request: Request, db: Session = Depends(get_db)):
    records = crud.get_information_gps(db)
    db.close()
    places = []
    if records:
        for record in records:
            places.append({"id": record.id, "latitude": record.latitude, "longitude": record.longitude})
            latitude = record.latitude
            longitude = record.longitude

    else:
        return HTTPException(status_code=404, detail="No data found")
    
    return templates.TemplateResponse("gps.html", {"request": request, "places": places, "latitude": latitude, "longitude": longitude})


@app.get("/gyroscope")
async def get_gyroscope(request: Request, db: Session = Depends(get_db)):    
    records = crud.get_information_gyroscope(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
        x_values = [records.x for records in records]
        y_values = [records.y for records in records]
        z_values = [records.z for records in records]
    else:
        return HTTPException(status_code=404, detail="No data found")

    return templates.TemplateResponse("gyroscope.html", {"request": request, "times": time, "x_values": x_values, "y_values": y_values, "z_values": z_values})


@app.get("/lightsensor")
async def get_lightSensor(request: Request, db: Session = Depends(get_db)):
    records = crud.get_information_lightSensor(db)
    db.close()
    if records:
        times = [str(records.time) for records in records]
        illuminance_values = [records.illuminance for records in records]
    else:
        return HTTPException(status_code=404, detail="No data found")

    return templates.TemplateResponse("lightSensor.html", {"request": request, "times": times, "illuminance_values": illuminance_values})
