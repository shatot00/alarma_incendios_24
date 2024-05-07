from fastapi import FastAPI, Depends, Request, HTTPException, Response, status
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

def check_fire(db: Session = Depends(get_db)):
    if crud.get_information_gas_last(db) > 1000 and crud.get_information_fire_last(db) > 1000:
        return True
    else:
        return False

def extinguish_fire(db: Session = Depends(get_db)):
    # Send signal to actuators to extinguish
    if check_fire(db):
        send_sprinkler()
        send_lcd()
        send_buzzer()


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

# ---------------------------- Send to actuators ----------------------------

@app.get("/send_sprinkler", status_code=200)
async def send_sprinkler(sprinkler: schemas.Sprinkler, db: Session = Depends(get_db)):
    return HTTPException(status_code=200, detail="added gps")


@app.get("/send_lcd", status_code=200)
async def send_lcd(lcd: schemas.Lcd, db: Session = Depends(get_db)):
    return HTTPException(status_code=200, detail="added gyroscope")


@app.get("/send_buzzer", status_code=200)
async def send_buzzer(buzzer: schemas.Buzzer, db: Session = Depends(get_db)):
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