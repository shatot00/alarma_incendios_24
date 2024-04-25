from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def add_information_accelerometer(db: Session, accelerometer: schemas.Accelerometer):
    db_accelerometer = models.Accelerometer(time=datetime.now(), x=accelerometer.x, y=accelerometer.y, z=accelerometer.z)
    db.add(db_accelerometer)
    db.commit()
    db.refresh(db_accelerometer)
    return db_accelerometer

def add_information_magnetometer(db: Session, magnetometer: schemas.Magnetometer):
    db_magnetometer = models.Magnetometer(time=datetime.now(), x=magnetometer.x, y=magnetometer.y, z=magnetometer.z)
    db.add(db_magnetometer)
    db.commit()
    db.refresh(db_magnetometer)
    return db_magnetometer

def add_information_gps(db: Session, gps: schemas.GPS):
    db_gps = models.GPS(latitude=gps.latitude, longitude=gps.longitude)
    db.add(db_gps)
    db.commit()
    db.refresh(db_gps)
    return db_gps

def add_information_gyroscope(db: Session, gyroscope: schemas.Gyroscope):
    db_gyroscope = models.Gyroscope(time=datetime.now(), x=gyroscope.x, y=gyroscope.y, z=gyroscope.z)
    db.add(db_gyroscope)
    db.commit()
    db.refresh(db_gyroscope)
    return db_gyroscope

def add_information_lightSensor(db: Session, lightSensor: schemas.LightSensor):
    db_lightSensor = models.LightSensor(time=datetime.now(), illuminance=lightSensor.illuminance)
    db.add(db_lightSensor)
    db.commit()
    db.refresh(db_lightSensor)
    return db_lightSensor


def get_information_accelerometer(db: Session):
    return db.query(models.Accelerometer).all()

def get_information_magnetometer(db: Session):
    return db.query(models.Magnetometer).all()

def get_information_gps(db: Session):
    return db.query(models.GPS).all()

def get_information_gyroscope(db: Session):
    return db.query(models.Gyroscope).all()

def get_information_lightSensor(db: Session):
    return db.query(models.LightSensor).all()