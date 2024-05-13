from fastapi import FastAPI, Depends, Request, HTTPException, Response, status
import os
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import httpx

models.Base.metadata.create_all(bind=engine)

IP_ARDUINO_ACTUATORS = '192.168.198.69:80' # IP of the arduino that has the sensors

FIRE = False # Variable to check if there is a fire

GAS_LEVEL = 700 # Level of gas to activate the actuators
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
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def check_fire(db: Session = Depends(get_db)):
    if crud.get_information_gas_last(db).level > GAS_LEVEL and crud.get_information_fire_last(db).level > FIRE_LEVEL:
        return True
    else:
        return False

def extinguish_fire(db: Session = Depends(get_db), FIRE=FIRE):
    # Send signal to actuators to extinguish
    if check_fire(db) and not FIRE:
        FIRE = True
        sprinkler_start()
        lcd_start()
        buzzer_start()
    elif not check_fire(db) and FIRE:
        FIRE = False
        sprinkler_stop()
        lcd_stop()
        buzzer_stop()


# ---------------------------- Methods GET and POST ----------------------------

# ---------------------------- Get information from sensors ----------------------------

@app.post("/db_gas", status_code=201)
def db_gas(gas: schemas.Gas, db: Session = Depends(get_db)):
    print("Metodo POST")
    print(gas)
    crud.add_information_gas(db, gas)
    extinguish_fire(db)


@app.post("/db_fire", status_code=201)
def db_fire(fire: schemas.Fire, db: Session = Depends(get_db)):
    crud.add_information_fire(db, fire)
    extinguish_fire(db)

# ---------------------------- Send to actuators to start ----------------------------

@app.get("/sprinkler_start", status_code=200)
def sprinkler_start(response: Response):

    url = f"http://{IP_ARDUINO_ACTUATORS}/sprinkler_on"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            print(response)
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(status_code=404, detail="IP not found")


@app.get("/lcd_start", status_code=200)
def lcd_start(response: Response):

    url = f"http://{IP_ARDUINO_ACTUATORS}/lcd_on"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            print(response)
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(status_code=404, detail="IP not found")

@app.get("/buzzer_start", status_code=200)
def buzzer_start(response: Response):

    url = f"http://{IP_ARDUINO_ACTUATORS}/buzzer_on"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            print(response)
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(status_code=404, detail="IP not found")


# ---------------------------- Send to actuators to stop ----------------------------

@app.get("/sprinkler_stop", status_code=200)
def sprinkler_stop(response: Response):

    url = f"http://{IP_ARDUINO_ACTUATORS}/sprinkler_off"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            print(response)
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(status_code=404, detail="IP not found")


@app.get("/lcd_stop", status_code=200)
def lcd_stop(response: Response):

    url = f"http://{IP_ARDUINO_ACTUATORS}/lcd_off"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            print(response)
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(status_code=404, detail="IP not found")

@app.get("/buzzer_stop", status_code=200)
def buzzer_stop(response: Response):

    url = f"http://{IP_ARDUINO_ACTUATORS}/buzzer_off"

    with httpx.Client() as client:
        try:
            response = client.get(url)
            print(response)
        except:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(status_code=404, detail="IP not found")


# ---------------------------- Show information from sensors ----------------------------

@app.get("/gas", status_code=200)
def gas(request: Request, response: Response, db: Session = Depends(get_db)):

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
def fire(request: Request, response: Response, db: Session = Depends(get_db)):

    records = crud.get_information_fire(db)
    db.close()
    if records:
        time = [str(records.time) for records in records]
        level = [str(records.level) for records in records]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="No data found")
    
    return templates.TemplateResponse("fire.html", {"request": request, "times": time, "levels": level})