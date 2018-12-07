from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
from threading import Timer

import argparse

prop = False

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % args.connect
vehicle = connect(args.connect, baud=115200, wait_ready=True)


def checkAlt():
    if vehicle.location.global_relative_frame.alt <= 0.3:
	print "Vehicle takeoff failed! Props not engaged!"
        print("Alt: zero!")
        #vehicle.armed = False
        vehicle.mode = VehicleMode("LAND")
        time.sleep(3)
        vehicle.armed = False
        vehicle.close()
        #break


# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

	print "Basic pre-arm checks"
  	# Don't let the user try to arm until autopilot is ready
  	while not vehicle.is_armable:
    		print " Waiting for vehicle to initialise..."
    		time.sleep(1)

  	print "Arming motors"
  	# Copter should arm in GUIDED mode
  	vehicle.mode    = VehicleMode("GUIDED")
  	vehicle.armed   = True

	while not vehicle.armed:
    		print " Waiting for arming..."
		time.sleep(10)

	countTime = 0
	print "Taking off!"
	vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
	#t = Timer(15.0, checkAlt)
  	#t.start()
  # Check that vehicle has reached takeoff altitude
	while True:
		#t.start()
		print " Altitude: ", vehicle.location.global_relative_frame.alt

		if countTime == 15:
       		# Disarm the vehicle
        		checkAlt()
			break
			#time.sleep(1)
		#Break and return from function just below target altitude.
		if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
			print "Reached target altitude"
      			break
    		time.sleep(1)
		countTime = countTime + 1


print "Mode: %s" % vehicle.mode.name    # settable

# Initialize the takeoff sequence to 20m
arm_and_takeoff(1)

if prop == False:
	print("Take off complete")
	# Hover for 10 seconds
	time.sleep(30)

	print("Now let's land")
	vehicle.mode = VehicleMode("LAND")

	# Close vehicle object
	vehicle.close()

