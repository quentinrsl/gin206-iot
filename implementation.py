import time
import requests
from dotenv import load_dotenv
import os

dT = 0.5

RATE_OF_CHANGE = [
    0.609164,
    0.533102,
    0.490007,
    0.441728,
    0.422819,
    0.397558,
    0.381043,
    0.459887,
    1.095440,
    2.825424,
    3.922974,
    3.454793,
    2.309282,
    1.671112,
    1.513777,
    1.621256,
    2.043299,
    2.568422,
    2.934706,
    2.461657,
    2.166300,
    1.601714,
    1.058227,
    0.778290,
    ]

load_dotenv()

def poll_data():
    # make a api call to http://quentin.com/api/temperature
    res = requests.get(os.getenv("SENSOR_API_URL")).json()
    return res["temperature"]

def push_data(temperature):
    print(f"Pushed data: {temperature}")
    requests.post(os.getenv("API_URL"), json={"temperature": temperature})

def main():
    temperature = poll_data()
    push_data(temperature)
    while True:
        #get hour of the day
        current_hour = time.localtime().tm_hour
        #get the rate of change for the current hour
        rate_of_change = RATE_OF_CHANGE[current_hour]
        #calculate the wait before the next poll
        wait_time = 3600 * dT / rate_of_change
        #wait
        time.sleep(wait_time)
        #poll data
        new_temperature = poll_data()
        print(f"New temperature: {new_temperature}")
        #push data
        push_data(new_temperature)
    
