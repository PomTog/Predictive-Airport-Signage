"""
To create a table of the time of 
arrival and determine what language to 
display by pulling from the API.
"""
from itertools import count
from unicodedata import numeric
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
    origin: Optional[Dict[str, Optional[str]]]
    destination: Optional[Dict[str, Optional[str]]]
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
    origin: Optional[Dict[str, Optional[str]]]
    destination: Optional[Dict[str, Optional[str]]]
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

class Airport(BaseModel):
    """Class for airport data"""
    
    iata: str
    name: str
    city: str
    subd: str
    country: str
    elevation: float
    lat: float
    lon: float
    tz: str

class Country(BaseModel):
    """class for country data"""
    
    alpha_2: str
    alpha_3: str
    flag: str
    name: str
    numeric: str
    official_name: Optional[str]

class Language(BaseModel):
    """class for language data"""
    
    character_order: Optional[str]
    display_name: Optional[str]
    english_name: Optional[str]
    language: Optional[str]
    language_name: Optional[str]
    population_percent: Optional[float]
    official_status: Optional[str]

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
    country_destination: Country
    country_origin: Country
    languages_origin: List[Language]
    languages_destination: List[Language]
    airport_origin: Airport
    airport_destination: Airport
    
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
            
            if not scheduled_arrival_departure.destination or not scheduled_arrival_departure.origin:
                continue

            airport_destination, country_destination, languages_destination = SignageData.get_airport_country_language(
                scheduled_arrival_departure.destination.get("code_iata")
                )

            airport_origin, country_origin, languages_origin = SignageData.get_airport_country_language(
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
                languages_origin = languages_origin,
                languages_destination = languages_destination,
                airport_origin = airport_origin,
                airport_destination = airport_destination
            )
            signage_datas.append(signage_data)
        
        return signage_datas

    @staticmethod
    def get_airport_country_language(code_iata : str):
        """Gets the airport, country and lang from code"""
        
        airport_data = airports[code_iata]
        country_data = pycountry.countries.get(alpha_2 = airport_data["country"])
        languages_data = babel.languages.get_territory_language_info(country_data.alpha_2)
        
        airport = Airport(
            iata = airport_data["iata"],
            name = airport_data["name"],
            city = airport_data["city"],
            subd = airport_data["subd"],
            country = airport_data["country"],
            elevation = airport_data["elevation"],
            lat = airport_data["lat"],
            lon = airport_data["lon"],
            tz = airport_data["tz"]
        )
        
        country = Country(
            alpha_2 = country_data.alpha_2,
            alpha_3 = country_data.alpha_3,
            flag = country_data.flag,
            name = country_data.name,
            numeric = country_data.numeric,
            official_name = country_data.official_name if hasattr(country_data, "offical_name") else None
        )
    
        languages = []
        
        for language, language_data in languages_data.items():
            babel_language = None
            try:
                babel_language = babel.Locale.parse(language)
            except:
                pass

            language_object = Language(
                character_order = babel_language.character_order if babel_language else None,
                display_name = babel_language.display_name if babel_language else None,
                english_name = babel_language.english_name if babel_language else None,
                language = babel_language.language if babel_language else None,
                language_name = babel_language.language_name if babel_language else None,
                population_percent = language_data["population_percent"],
                official_status = language_data["official_status"]
            )
            languages.append(language_object)

        return airport, country, languages


class SignageDatas(BaseModel):
    """A Model to hold data for multiple signs (and make json serialization easier)"""
    
    arrivals_departures: str
    signage_datas: List[SignageData]

    def cache(self):
        """Caching the signage data"""
        client.set(
            f'signage:{self.arrivals_departures}',
            self.json()
        )
    
    @staticmethod
    def get(arrivals_departures: str):
        """get data from cache"""
        data=client.get(
            f'signage:{arrivals_departures}'
        )
        return SignageDatas(**json.loads(data))

if __name__=="__main__":

    arrivals = Arrivals.cached_get()
    departures = Departures.cached_get()
    arrivals_signage_datas = SignageDatas(
        arrivals_departures = "arrivals",
        signage_datas = SignageData.factory(arrivals)
        )
    departures_signage_datas = SignageDatas(
        arrivals_departures = "departures",
        signage_datas = SignageData.factory(departures)
        )
    arrivals_signage_datas.cache()
    departures_signage_datas.cache()
    print("Done")
