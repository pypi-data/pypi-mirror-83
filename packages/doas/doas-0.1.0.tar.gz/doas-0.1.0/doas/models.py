from sqlalchemy import Column, Date, DateTime, Float, String
from sqlalchemy.ext.automap import automap_base

from .settings import STATION_NAME

Base = automap_base()


class SimpleSO2Flux(Base):
    """
    Simple models to store DOAS SO2 flux data. It stores only date and flux
    values, with one value per date.
    """
    __tablename__ = f'{STATION_NAME}_simple_so2_flux'

    date = Column('date', Date, primary_key=True, index=True)
    flux = Column('flux', Float, index=True, nullable=True)


class SO2Flux(Base):
    """
    Models to store necessary DOAS SO2 flux data including starttime, endtime,
    angle, and flux.
    """
    __tablename__ = f'{STATION_NAME}_so2_flux'

    starttime = Column('starttime', DateTime, primary_key=True, index=True)
    endtime = Column('endtime', DateTime, index=True, nullable=True)
    angle = Column('angle', Float, index=True, nullable=True)
    flux = Column('flux', Float, index=True, nullable=True)


class FullSO2Flux(Base):
    """
    Models to store full DOAS SO2 flux data including scan index, filepath,
    starttime, endtime, angle and flux.
    """
    __tablename__ = f'{STATION_NAME}_full_so2_flux'

    starttime = Column('starttime', DateTime, primary_key=True, index=True)
    endtime = Column('endtime', DateTime, index=True, nullable=True)
    angle = Column('angle', Float, index=True, nullable=True)
    flux = Column('flux', Float, index=True, nullable=True)
    scanindex = Column('scanindex', String(255), index=True, nullable=True)
    filepath = Column('filepath', String(255), index=True, nullable=True)


class ModelTypes:
    SO2_FLUX = 'so2_flux'
    SIMPLE_SO2_FLUX = 'simple_so2_flux'
    FULL_SO2_FLUX = 'full_so2_flux'

    LIST = (
        SO2_FLUX,
        SIMPLE_SO2_FLUX,
        FULL_SO2_FLUX,
    )


MODELS = {
    ModelTypes.SIMPLE_SO2_FLUX: SimpleSO2Flux,
    ModelTypes.SO2_FLUX: SO2Flux,
    ModelTypes.FULL_SO2_FLUX: FullSO2Flux,
}
