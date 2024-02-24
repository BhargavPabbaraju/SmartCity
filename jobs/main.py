import os
import uuid
from datetime import datetime,timedelta
from confluent_kafka import SerializingProducer
import random
import simplejson as json

LONDON_COORDINATES = {"latitude": 51.5074, "longitude": -0.1278}
BIRMINGHAM_COORDINATES = {"latitude": 52.4862, "longitude": -1.8904}

# Calculate the movement increments
LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude']) / 100

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

random.seed(42)
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()

def get_next_time():
    global start_time

    start_time += timedelta(seconds=random.randint(30,60)) #update frequency

    return start_time

def simulate_vehicle_movement():
    global start_location

    #Move towards birmingham
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    #Add some randomness to simulate actual road travel
    start_location['latitude'] += random.uniform(-0.0005,0.0005)
    start_location['longitude'] += random.uniform(-0.0005,0.0005)

    return start_location






def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'],location['longitude']),
        'speed': random.uniform(10,40),
        'direction': 'North-East',
        'make': 'BMW',
        'model': 'CS500',
        'year': 2024,
        'fuelType': 'Hybrid'

    }


def generate_gps_data(device_id, timestamp,vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0,40),# km/hr
        'direction': 'North-East',
        'vehicleType': vehicle_type

    }

def generate_traffic_camera_data(device_id,timestamp,camera_id,location):
    return{
        'id':uuid.uuid4,
        'deviceId':device_id,
        'cameraId':camera_id,
        'timestamp': timestamp,
        'snapshot': 'Base64EncodedString',
        'location': location,

    }


def generate_weather_data(device_id, timestamp, location):
    return {
        'id':uuid.uuid4(),
        'deviceId':device_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(-5,26),
        'weatherCondition': random.choice(['Sunny','Cloudy','Rainy','Snowy']),
        'precipitation': random.uniform(0,25),
        'windSpeed': random.uniform(0,100),
        'humidity': random.randint(0,100),
        'airQualityIndex': random.uniform(0,500)

    }


def generate_emegerncy_incident_data(device_id, timestamp, location):
    return {
        'id':uuid.uuid4(),
        'deviceId': device_id,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident','Fire','Medical','Police','None']),
        'timestamp': timestamp,
        'location': location,
        'status': random.choice(['Active','Resolved']),
        'description': 'Description of the Incident'



    }


def simulate_journey(producer,device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id,vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(device_id,vehicle_data['timestamp'],
                                                           'NikonCam123',
                                                           vehicle_data['location'])
        weather_data = generate_weather_data(device_id,vehicle_data['timestamp'],
                                             vehicle_data['location'])
        emergency_incident_data = generate_emegerncy_incident_data(device_id,
                                                                   vehicle_data['timestamp'],
                                                                   vehicle_data['location'])

        print(vehicle_data)
        print(gps_data)
        print(traffic_camera_data)
        print(weather_data)
        print(emergency_incident_data)



if __name__ == '__main__':
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }

    producer = SerializingProducer(producer_config)
    try:
        simulate_journey(producer,'Vehicle-Bhargav-123')
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected error: {e}')
