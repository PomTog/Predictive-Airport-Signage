"""
To create a table of the time of 
arrival and determine what language to 
display by pulling from the API.
"""
from pydantic import BaseModel, validate_arguments
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
import requests
import redis
import json
import airportsdata
import pycountry
import collections
import babel
import babel.languages

client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


id="LHR"
airports = airportsdata.load('IATA')

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
    def get():
        """pull request from api for arrivals"""
        response = requests.get(
            f"https://aeroapi.flightaware.com/aeroapi/airports/{id}/flights/scheduled_arrivals",
            headers={
                "x-apikey":"hAUtREfKvazvRdYJu7NwAEpCklCkUvxt",
            }
        )
        return Arrivals(**response.json())

    @staticmethod
    def cached_get():
        """cached request"""
        data = client.get('processor:api:arrivals')
        if data: 
            return Arrivals(**json.loads(data))
        
        arrivals = Arrivals.get()
        client.set(
            'processor:api:arrivals',
            arrivals.json()
        )
        return arrivals

class Departures(BaseModel):
    """Its a model to represent departures data from the FlightAware API"""
    
    scheduled_departures: List[Departure]
    links: Dict[str, str]
    num_pages: int

    @staticmethod
    def get():
        """pull request from api for departures"""
        response = requests.get(
            f"https://aeroapi.flightaware.com/aeroapi/airports/{id}/flights/scheduled_departures",
            headers={
                "x-apikey":"hAUtREfKvazvRdYJu7NwAEpCklCkUvxt",
            }
        )
        return Departures(**response.json())
    
    @staticmethod
    def cached_get():
        """cached request"""
        data = client.get('processor:api:departures')
        if data: 
            return Departures(**json.loads(data))
        
        departures = Departures.get()
        client.set(
            'processor:api:departures',
            departures.json()
        )
        return departures

class SignageData(BaseModel):
    """This is the signage data"""
    gate_destination: Optional[str]
    terminal_destination: Optional[str]
    gate_origin: Optional[str]
    status: str
    estimated_in: Optional[datetime]
    estimated_out: Optional[datetime]
    destination_code_iata: Optional[str]
    origin_code_iata: Optional[str]
    country_destination: Any
    country_origin: Any
    language_origin: Any
    language_destination: Any
    airport_origin: collections.OrderedDict
    airport_destination: collections.OrderedDict
    
    @staticmethod
    def factory(arrivals_departures: Union[Arrivals, Departures]):
        """to generate signage data object from arrivals/departures"""

        signage_datas=[]
        scheduled_arrivals_departures=[]

        if isinstance(arrivals_departures, Arrivals):
            scheduled_arrivals_departures = arrivals_departures.scheduled_arrivals
        elif isinstance(arrivals_departures, Departures):
            scheduled_arrivals_departures = arrivals_departures.scheduled_departures
        
        for scheduled_arrival_departure in scheduled_arrivals_departures:

            airport_destination, country_destination, language_destination = SignageData.get_airport_country_language(
                scheduled_arrival_departure.destination.get("code_iata")
                )

            airport_origin, country_origin, language_origin = SignageData.get_airport_country_language(
                scheduled_arrival_departure.origin.get("code_iata")
                )

            signage_data = SignageData(
                gate_destination = scheduled_arrival_departure.gate_destination,
                terminal_destination = scheduled_arrival_departure.terminal_destination,
                gate_origin = scheduled_arrival_departure.gate_origin,
                status = scheduled_arrival_departure.status,
                estimated_in = scheduled_arrival_departure.estimated_in,
                estimated_out = scheduled_arrival_departure.estimated_out,
                destination_code_iata = scheduled_arrival_departure.destination.get("code_iata"),
                origin_code_iata = scheduled_arrival_departure.origin.get("code_iata"),
                country_destination = country_destination,
                country_origin = country_origin,
                language_origin = language_origin,
                language_destination = language_destination,
                airport_origin = airport_origin,
                airport_destination = airport_destination
            )
            signage_datas.append(signage_data)
        
        return signage_datas

    @staticmethod
    def get_airport_country_language(code_iata : str):
        """Gets the airport, country and lang from code"""
        airport = airports[code_iata]
        country = pycountry.countries.get(alpha_2 = airport["country"])
        languages = babel.languages.get_territory_language_info(country.alpha_2)
        language = babel.Locale.parse(list(languages)[0])
        return airport, country.__dict__, language.__dict__

    @staticmethod
    def cache_signage_datas(signage_datas:list, arrivals_departures: str):
        """Caching the signage data"""
        client.set(
            f'signage:{arrivals_departures}',
            json.dumps([json.loads(signage_data.json()) for signage_data in signage_datas])
        )
        return departures


if __name__=="__main__":

    arrivals = Arrivals.cached_get()
    departures = Departures.cached_get()
    arrivals_signage_datas = SignageData.factory(arrivals)
    departures_signage_datas = SignageData.factory(departures)
    SignageData.cache_signage_datas(arrivals_signage_datas, "arrivals")
    SignageData.cache_signage_datas(departures_signage_datas, "departures")
    print("Done")
    breakpoint()


