from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def add_information_gas(db: Session, gas: schemas.Gas):
    db_gas = models.Gas(time=datetime.now(), level=gas.level)
    db.add(db_gas)
    db.commit()
    db.refresh(db_gas)
    return db_gas

def add_information_fire(db: Session, fire: schemas.Fire):
    db_fire = models.Fire(time=datetime.now(), level=fire.level)
    db.add(db_fire)
    db.commit()
    db.refresh(db_fire)
    return db_fire

def get_information_gas(db: Session):
    return db.query(models.Gas).all()

def get_information_fire(db: Session):
    return db.query(models.Fire).all()