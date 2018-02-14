from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import time
import requests
import csv
import pandas
import sys
import sqlite3
import folium
from google.transit import gtfs_realtime_pb2
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "testTable.db")
index_path = os.path.join(BASE_DIR, "index.html")
map_path = os.path.join(BASE_DIR, "map.html")
top = '<html>\
        <head>\
            <title>Buses in Parramatta Inter-Exchange</title>\
            <meta http-equiv="refresh" content="4" />\
            <style>\
              table, th, td {\
                border: 1px solid black;\
                }\
            </style>\
        </head>\
        <body>\
          <div align="center">\
            <h1>Buses in Parramatta Interchange!</h1>\
            <h4>This site shows buses in the Parrammatta Interchange Area.</h4>\
            <h4>It only shows active buses and duration of stay in Parramatta</h4>\
          </div>\
          <div align="center">\
          <table>\
            <tr>\
              <th>Bus Route</th>\
              <th>Duration(in seconds)</th>\
            </tr>'

bot='         </table>\
            <a href="map.html"><h3>Click to view Map</h3></a>\
        </div>\
      </body>\
    </html>'

def getVehiclePosition():
     #Free api key from api.transport.nsw.gov.au
        api_key = 'cYYUJIy0P5wuNLTe5KPG1jtOKlL6VroLGN3Z'
        headers = {"Authorization":"apikey " + api_key}
        bus_positions = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses', headers=headers)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(bus_positions.content)
        positions_output = [] # a list of lists for bus position data
        # put each bus's key data into the list
        for entity in feed.entity:
            #buscomp = str(entity.id)
            #if '_2436_' in buscomp:
            busPosition = Point(entity.vehicle.position.latitude,entity.vehicle.position.longitude)
            if parramatta.contains(busPosition):
                try:
                    c.execute("INSERT INTO 'vehicleData' ('routeID','startTime','latitude','longtitude',\
                                                    'bearing','speed','currentTime','totalTime','tripID')\
                    VALUES ('{}',DATETIME('now'),'{}','{}','{}','{}',DATETIME('now'),'0','{}')".format(entity.id,entity.vehicle.position.latitude,\
                                                              entity.vehicle.position.longitude,\
                                                              entity.vehicle.position.bearing,entity.vehicle.position.speed,entity.vehicle.trip.trip_id))

                    conn.commit()
                    print('Data Added {}'.format(entity.id))
                except sqlite3.IntegrityError:
                    c.execute("UPDATE vehicleData SET currentTime = (DATETIME('now')) WHERE routeID = ('{}') AND tripID = ('{}')".format(entity.id,entity.vehicle.trip.trip_id))
                    c.execute("UPDATE vehicleData SET totalTime = (strftime('%s',DATETIME('now')) - strftime('%s',startTime)) WHERE routeID = ('{}')AND tripID = ('{}')".format(entity.id,entity.vehicle.trip.trip_id))
                    c.execute("UPDATE vehicleData SET latitude = '{}' WHERE routeID = ('{}') AND tripID = ('{}')".format(entity.id,entity.vehicle.trip.trip_id))
                    c.execute("UPDATE vehicleData SET longtitude = '{}' WHERE routeID= ('{}')AND tripID = ('{}')".format(entity.id,entity.vehicle.trip.trip_id))
                    conn.commit()
                    print('Data Updated {}'.format(entity.id))





#start of main script
def createHTML():
    c.execute("SELECT routeID,latitude,longtitude,totalTime FROM vehicleData WHERE currentTime > DATETIME('now','-3 seconds')")
    result=''
    vehiclemap = folium.Map(location=(-33.817458, 151.004526), zoom_start=20,tiles='Stamen Toner',width=750, height=500)
    for each in c.fetchall():
        result = result + " <tr> " + "<th>" +each[0][-5:-2]+"</th>"\
                + "<th>" + str(each[3])+"</th></tr>"
        vehiclemap.add_child(folium.Marker(location=[each[1],each[2]],popup='Bus '+ each[0][-5:-2] +' stayed in Parramatta for '+str(each[3])+' seconds',icon=folium.Icon(color='green')))

    html_str=top+result+bot
    Html_file= open(index_path,"w")
    Html_file.write(html_str)
    Html_file.close()
    vehiclemap.save(outfile=map_path)
    if result == '':
            print('No HTML created')
    else:
            print('HTML created')
#python C:\inetpub\wwwroot\bus.py

conn = sqlite3.connect(db_path)
c = conn.cursor()
parramatta = Polygon([(-33.816980,151.003976), (-33.817140,151.003819), (-33.818171,151.005522), (-33.818024,151.005668)])
while True:
        try:
                getVehiclePosition()
                createHTML()
                print("-----------------------------------------------")
                time.sleep(4)
        except Exception as e:
                print(e)

def getVehiclePosition():
     #Free api key from api.transport.nsw.gov.au
        api_key = 'cYYUJIy0P5wuNLTe5KPG1jtOKlL6VroLGN3Z'
        headers = {"Authorization":"apikey " + api_key}
        bus_positions = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses', headers=headers)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(bus_positions.content)
        positions_output = [] # a list of lists for bus position data
        # put each bus's key data into the list
        for entity in feed.entity:
            #buscomp = str(entity.id)
            #if '_2436_' in buscomp:
            busPosition = Point(entity.vehicle.position.latitude,entity.vehicle.position.longitude)
            if parramatta.contains(busPosition):
                try:
                    c.execute("INSERT INTO 'vehicleData' ('routeID','startTime','latitude','longtitude',\
                                                    'bearing','speed','currentTime','totalTime','tripID')\
                    VALUES ('{}',DATETIME('now'),'{}','{}','{}','{}',DATETIME('now'),'0','{}')".format(entity.id,entity.vehicle.position.latitude,\
                                                              entity.vehicle.position.longitude,\
                                                              entity.vehicle.position.bearing,entity.vehicle.position.speed,entity.vehicle.trip.trip_id))

                    conn.commit()
                    print('Data Added {}'.format(entity.id))
                except sqlite3.IntegrityError:

                    c.execute("UPDATE vehicleData SET totalTime = (strftime('%s',DATETIME('now')) - strftime('%s',startTime)) WHERE routeID = ('{}')".format(entity.id))
                    c.execute("UPDATE vehicleData SET latitude = '{}' WHERE routeID = ('{}')".format(entity.id,entity.vehicle.position.latitude))
                    c.execute("UPDATE vehicleData SET longtitude = '{}' WHERE routeID= ('{}')".format(entity.id,entity.vehicle.position.longitude))
                    conn.commit()
                    print('Data Updated {}'.format(entity.id))

        print
