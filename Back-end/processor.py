"""
To create a table of the time of 
arrival and determine what language to 
display by pulling from the API.
"""
import enum
from functools import cache
from webbrowser import get
from wsgiref import headers
from pydantic import BaseModel, validate_arguments
from typing import List, Dict, Optional
from datetime import datetime
import requests
from redis import StrictRedis
from redis_cache import RedisCache

client = StrictRedis(host = "localhost", decode_responses=True)
cache = RedisCache(redis_client=client)

id="LHR"

class Arrival(BaseModel):
    """Its a model to represent arrival data from the FlightAware API"""
    ident: str
    ident_icao: Optional[str]
    ident_iata: Optional[str]
    fa_flight_id: str
    operator: Optional[str]
    operator_icao: Optional[str]
    operator_iata: Optional[str]
    flight_number: Optional[str]
    registration: Optional[str]
    atc_ident: Optional[str]
    inbound_fa_flight_id: Optional[str]
    codeshares: List[str]
    codeshares_iata: List[str]
    blocked: bool
    diverted: bool
    cancelled: bool
    position_only: bool
    origin: Dict[str, Optional[str]]
    destination: Dict[str, Optional[str]]
    departure_delay: Optional[int]
    arrival_delay: Optional[int]
    filed_ete: Optional[int]
    scheduled_out: Optional[datetime]
    estimated_out: Optional[datetime]
    actual_out: Optional[datetime]
    scheduled_off: Optional[datetime]
    estimated_off: Optional[datetime]
    actual_off: Optional[datetime]
    scheduled_on: Optional[datetime]
    estimated_o: Optional[datetime]
    actual_on: Optional[datetime]
    scheduled_in: Optional[datetime]
    estimated_in: Optional[datetime]
    actual_in: Optional[datetime]
    progress_percent: Optional[int]
    status: str
    aircraft_type: Optional[str]
    route_distance: Optional[int]
    filed_airspeed: Optional[int]
    filed_altitude: Optional[int]
    route: Optional[str]
    baggage_claim: Optional[str]
    seats_cabin_business: Optional[int]
    seats_cabin_coach: Optional[int]
    seats_cabin_first: Optional[int]
    gate_origin: Optional[str]
    gate_destination: Optional[str]
    terminal_origin: Optional[str]
    terminal_destination: Optional[str]
    type: str

class Departure(BaseModel):
    """Its a model to represent departure data from the FlightAware API"""
    ident: str
    ident_icao: Optional[str]
    ident_iata: Optional[str]
    fa_flight_id: str
    operator: Optional[str]
    operator_icao: Optional[str]
    operator_iata: Optional[str]
    flight_number: Optional[str]
    registration: Optional[str]
    atc_ident: Optional[str]
    inbound_fa_flight_id: Optional[str]
    codeshares: List[str]
    codeshares_iata: List[str]
    blocked: bool
    diverted: bool
    cancelled: bool 
    position_only: bool
    origin: Dict[str, Optional[str]]
    destination: Dict[str, Optional[str]]
    departure_delay: Optional[int]
    arrival_delay:Optional[int]
    filed_ete: Optional[int]
    scheduled_out: Optional[datetime]
    estimated_out: Optional[datetime]
    actual_out: Optional[datetime]
    scheduled_off: Optional[datetime]
    estimated_off: Optional[datetime]
    actual_off: Optional[datetime]
    scheduled_on: Optional[datetime]
    estimated_on: Optional[datetime]
    actual_on: Optional[datetime]
    scheduled_in: Optional[datetime]
    estimated_in: Optional[datetime]
    actual_in: Optional[datetime]
    progress_percent: Optional[int]
    status: str
    aircraft_type: Optional[str]
    route_distance: Optional[int]
    filed_airspeed: Optional[int]
    filed_altitude: Optional[int]
    route: Optional[str]
    baggage_claim: Optional[str]
    seats_cabin_business: Optional[int]
    seats_cabin_coach: Optional[int]
    seats_cabin_first: Optional[int]
    gate_origin: Optional[str]
    gate_destination: Optional[str]
    terminal_origin: Optional[str]
    terminal_destination: Optional[str]
    type: str 

class Arrivals(BaseModel):
    """Its a model to represent arrivals data from the FlightAware API"""
    
    scheduled_arrivals: List[Arrival]
    links: Dict[str, str]
    num_pages: int

    @staticmethod
    @cache.cache()
    def get():
        """pull request from api for arrivals"""
        response = requests.get(
            f"https://aeroapi.flightaware.com/aeroapi/airports/{id}/flights/scheduled_arrivals",
            headers={
                "x-apikey":"hAUtREfKvazvRdYJu7NwAEpCklCkUvxt",
            }
        )
        return Arrivals(**response.json()).dict()

class Departures(BaseModel):
    """Its a model to represent departures data from the FlightAware API"""
    
    scheduled_departures: List[Departure]
    links: Dict[str, str]
    num_pages: int

    @staticmethod
    @cache.cache()
    def get():
        """pull request from api for departures"""
        response = requests.get(
            f"https://aeroapi.flightaware.com/aeroapi/airports/{id}/flights/scheduled_departures",
            headers={
                "x-apikey":"hAUtREfKvazvRdYJu7NwAEpCklCkUvxt",
            }
        )
        return Departures(**response.json()).dict()


if __name__=="__main__":

    scheduled_arrivals = Arrivals.get()
    scheduled_departures = Departures.get()
    print("Done")
    breakpoint()
    
