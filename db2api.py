from fastapi import FastAPI
from sqlalchemy import create_engine, text
import yaml
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("The DATABASE_URL environment variable MUST be set!")
if not DATABASE_URL.startswith("postgresql"):
   DATABASE_URL = f"postgresql://{DATABASE_URL}"

app = FastAPI()
eng = create_engine(DATABASE_URL)

def create_simple_endpoint(endpoint, query):
   """Function to manufacture simple endpoints for those without much
   Python experience.
   """
   @app.get(endpoint)
   def auto_simple_endpoint():
      f"""Automatic endpoint function for {endpoint}"""
      with eng.connect() as con:
         res = con.execute(query)
         return [r._asdict() for r in res]
            
with open("endpoints.yaml") as f:
   endpoints = yaml.safe_load(f)
   for endpoint, query in endpoints.items():
      create_simple_endpoint(endpoint, query)





#------------------------------------------------
# Custom Endpoints
#------------------------------------------------

@app.get("/weather/{page}")
def weather_by_page(page):
     with eng.connect() as con:
        query = """
                SELECT *
                FROM clean_weather
                LIMIT 50
                OFFSET :off
                """
        res = con.execute(text(query), {'off': 50*int(page)})
        return [r._asdict() for r in res]

@app.get("/systems/{page}")
def systems_by_page(page):
     with eng.connect() as con:
        query = """
                SELECT *
                FROM systems
                LIMIT 50
                OFFSET :off
                """
        res = con.execute(text(query), {'off': 50*int(page)})
        return [r._asdict() for r in res]

@app.get("/weather_report/{page}")
def weather_report_by_page(page):
     with eng.connect() as con:
        query = """
                SELECT *
                FROM weather_report
                LIMIT 50
                OFFSET :off
                """
        res = con.execute(text(query), {'off': 50*int(page)})
        return [r._asdict() for r in res]

