# gin206-iot
IOT Project for the GIN206 course of Télécom Paris

# Description
The main.py file contains the code generating the graphs seen on the document submitted for the project. The implementation.py file contains the code that sends the data to the Thingsboard server.

# How to setup the implementation
Install the requirements
```
pip install -r requirements.txt
```
Create a .env file in the root directory of the project with the following content:
```
SENSOR_API_URL= # URL of the sensor API
THINGSBOARD_URL = # URL of the Thingsboard server
```
Run the application
```
python implementation.py
```