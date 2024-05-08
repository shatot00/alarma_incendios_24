from fastapi import FastAPI, Depends, Request, HTTPException, Response, status
import os
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import httpx


models.Base.metadata.create_all(bind=engine)

IP_ARDUINO_SENSORS = '192.168.198.69' # IP of the arduino that has the sensors
IP_ARDUINO_ACTUATORS = '192.168.198.122:7999' # IP of the arduino that has the actuators

FIRE = False # Variable to check if there is a fire

GAS_LEVEL = 700 # Level of gas to activate the actuators
FIRE_LEVEL = 700 # Level of fire to activate the actuators

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

def check_fire(db: Session = Depends(get_db)):
    if crud.get_information_gas_last(db) > GAS_LEVEL and crud.get_information_fire_last(db) > FIRE_LEVEL:
        return True
    else:
        return False

def extinguish_fire(db: Session = Depends(get_db)):
    # Send signal to actuators to extinguish
    if check_fire(db) and not FIRE:
        FIRE = True
        send_sprinkler_start()
        send_lcd_start()
        send_buzzer_start()
    elif not check_fire(db) and FIRE:
        FIRE = False
        send_sprinkler_stop()
        send_lcd_stop()
        send_buzzer_stop()


# ---------------------------- Methods GET and POST ----------------------------
        
@app.get("/")
async def root():
    return "hola"

# ---------------------------- Get information from sensors ----------------------------

@app.post("/add_gas", status_code=201)
async def add_gas(gas: schemas.Gas, db: Session = Depends(get_db)):    
    crud.add_information_gas(db, gas)
    extinguish_fire(db)


@app.post("/add_fire", status_code=201)
async def add_fire(fire: schemas.Fire, db: Session = Depends(get_db)):
    crud.add_information_fire(db, fire)
    extinguish_fire(db)

# ---------------------------- Send to actuators to start ----------------------------

@app.get("/send_sprinkler_start", status_code=200)
async def send_sprinkler_start(sprinkler: schemas.Sprinkler, db: Session = Depends(get_db)):
    return HTTPException(status_code=200, detail="added gps")


@app.get("/send_lcd_start", status_code=200)
async def send_lcd_start():

    url = f"http://{IP_ARDUINO_ACTUATORS}/lcd_on"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response
    
    return HTTPException(status_code=200, detail="added gyroscope")


@app.get("/send_buzzer_start", status_code=200)
async def send_buzzer_start(buzzer: schemas.Buzzer, db: Session = Depends(get_db)):
    return HTTPException(status_code=200, detail="added lightSensor")


# ---------------------------- Send to actuators to stop ----------------------------

@app.get("/send_sprinkler_stop", status_code=200)
async def send_sprinkler_stop(sprinkler: schemas.Sprinkler, db: Session = Depends(get_db)):
    return HTTPException(status_code=200, detail="added gps")


@app.get("/send_lcd_stop", status_code=200)
async def send_lcd_stop():

    url = f"http://{IP_ARDUINO_ACTUATORS}/lcd_off"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(response)
        return response
    
    return HTTPException(status_code=200, detail="added gyroscope")


@app.get("/send_buzzer_stop", status_code=200)
async def send_buzzer_stop(buzzer: schemas.Buzzer, db: Session = Depends(get_db)):
    return HTTPException(status_code=200, detail="added lightSensor")


# ---------------------------- Show information from sensors ----------------------------

@app.get("/gas", status_code=200)
async def get_gas(request: Request, response: Response, db: Session = Depends(get_db)):

    records = crud.get_information_gas(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="No data found")

    return templates.TemplateResponse("gas.html", {"request": request, "times": time})

@app.get("/fire", status_code=200)
async def get_fire(request: Request, response: Response, db: Session = Depends(get_db)):

    records = crud.get_information_fire(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="No data found")
    
    return templates.TemplateResponse("fire.html", {"request": request, "times": time})