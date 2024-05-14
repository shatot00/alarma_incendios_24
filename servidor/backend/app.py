from fastapi import FastAPI, Depends, Request, HTTPException, Response, status
import os
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import requests

models.Base.metadata.create_all(bind=engine)

IP_ARDUINO_ACTUATORS = '192.168.253.69:80' # IP of the arduino that has the sensors

FIRE = False # Variable to check if there is a fire

GAS_LEVEL = 400 # Level of gas to activate the actuators
FIRE_LEVEL = 1 # Level of fire to activate the actuators

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

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def check_fire(db: Session = Depends(get_db)):
    if crud.get_information_gas_last(db).level > GAS_LEVEL or crud.get_information_fire_last(db).level == FIRE_LEVEL:
        return True
    else:
        return False

def extinguish_fire(db: Session = Depends(get_db), FIRE=FIRE):
    print(FIRE)
    print(FIRE_LEVEL)
    print(check_fire(db))

    # if len(crud.get_information_gas(db)) > 100 and len(crud.get_information_fire(db)) > 100:
    #     crud.delete_information_gas_last_10(db)
    #     crud.delete_information_fire_last_10(db)
        
    # Send signal to actuators to extinguish
    if check_fire(db) and not FIRE:
        FIRE = True
        print("AAAAAAAAAA")
        lcd_start()
        buzzer_start()
        sprinkler_start()
    elif not check_fire(db):
        FIRE = False
        lcd_stop()
        buzzer_stop()
        sprinkler_stop()


# ---------------------------- Methods GET and POST ----------------------------

# ---------------------------- Get information from sensors ----------------------------

@app.post("/db_gas", status_code=201)
async def db_gas(gas: schemas.Gas, db: Session = Depends(get_db)):
    print("GAS POST")
    print(gas)
    crud.add_information_gas(db, gas)
    extinguish_fire(db)


@app.post("/db_fire", status_code=201)
async def db_fire(fire: schemas.Fire, db: Session = Depends(get_db)):
    print("FIRE POST")
    print(fire)
    crud.add_information_fire(db, fire)
    extinguish_fire(db)

# ---------------------------- Send to actuators to start ----------------------------

@app.get("/sprinkler_start", status_code=200)
def sprinkler_start():

    url = f"http://{IP_ARDUINO_ACTUATORS}/sprinkler_on"

    resp = requests.get(url)
    print(resp)

@app.get("/lcd_start", status_code=200)
def lcd_start():
    print("Iniciar LCD")

    url = f"http://{IP_ARDUINO_ACTUATORS}/lcd_on"

    resp = requests.get(url)
    print(resp)

@app.get("/buzzer_start", status_code=200)
def buzzer_start():

    url = f"http://{IP_ARDUINO_ACTUATORS}/buzzer_on"

    resp = requests.get(url)
    print(resp)


# ---------------------------- Send to actuators to stop ----------------------------

@app.get("/sprinkler_stop", status_code=200)
def sprinkler_stop():

    url = f"http://{IP_ARDUINO_ACTUATORS}/sprinkler_off"

    resp = requests.get(url)
    print(resp)


@app.get("/lcd_stop", status_code=200)
def lcd_stop():
    print("Apagar LCD")

    url = f"http://{IP_ARDUINO_ACTUATORS}/lcd_off"

    resp = requests.get(url)
    print(resp)

@app.get("/buzzer_stop", status_code=200)
def buzzer_stop():

    url = f"http://{IP_ARDUINO_ACTUATORS}/buzzer_off"

    resp = requests.get(url)
    print(resp)


# ---------------------------- Show information from sensors ----------------------------

@app.get("/gas", status_code=200)
async def gas(request: Request, response: Response, db: Session = Depends(get_db)):

    records = crud.get_information_gas(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
        level = [str(records.level) for records in records]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="No data found")

    return templates.TemplateResponse("gas.html", {"request": request, "times": time, "levels": level})

@app.get("/fire", status_code=200)
async def fire(request: Request, response: Response, db: Session = Depends(get_db)):

    records = crud.get_information_fire(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
        level = [str(records.level) for records in records]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="No data found")
    
    return templates.TemplateResponse("fire.html", {"request": request, "times": time, "levels": level})