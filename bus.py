from google.transit import gtfs_realtime_pb2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import time
import requests
import folium
import os.path
from sense_hat import SenseHat

BASE_DIR = '/var/www/html/'
db_path = os.path.join(BASE_DIR, "testTable")
map_path = os.path.join(BASE_DIR, "index.html")


sense = SenseHat()
def getVehiclePosition():
     #Free api key from api.transport.nsw.gov.au
        api_key = 'cYYUJIy0P5wuNLTe5KPG1jtOKlL6VroLGN3Z'
        headers = {"Authorization":"apikey " + api_key}
        bus_positions = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses', headers=headers)
        #Parse content to google protobuf
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(bus_positions.content)
        positions_output = [] # a list of lists for bus position data
        # put each bus's key data into the list
        for entity in feed.entity:
            busPosition = Point(entity.vehicle.position.latitude,entity.vehicle.position.longitude)
            if parramatta.contains(busPosition):
                bus_info = [entity.id,
                            entity.vehicle.position.latitude,
                            entity.vehicle.position.longitude,
                            entity.vehicle.position.bearing,
                            entity.vehicle.position.speed,
                            entity.vehicle.trip.trip_id]
                print(bus_info[0][-5:-2])
                positions_output.append(bus_info)
        if positions_output == []:
            print('No BUS')
            sense.load_image('GO.jpg')
        else:
            print('BUS Incoming')
            sense.load_image('STOP.jpg')
        return positions_output


#start of main script
def createHTML(buses):
    vehiclemap = folium.Map(location=(-33.813108, 151.006816), zoom_start=20,tiles='Stamen Toner',width=750, height=500)
    for each in buses:
        vehiclemap.add_child(folium.Marker(location=[each[1],each[2]],
            popup='Bus '+ each[0][-5:-2] + ' going to ' + str(each[3]), icon=folium.Icon(color='green')))
    vehiclemap.save(outfile=map_path)
    

parramatta = Polygon([(-33.813108, 151.006816), (-33.813065, 151.006726), (-33.815153, 151.006107), (-33.815121, 151.006034)])
while True:
        try:
                buses = getVehiclePosition()
                createHTML(buses)
                print("-----------------------------------------------")
                time.sleep(3)
        except Exception as e:
                print(e)

