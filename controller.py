#import XPS_Q8_drivers

#connection = XPS_Q8_drivers.XPS()
#socketID = connection.TCP_ConnectToServer("192.168.0.254", 5001, 10)

#import XPS_Q8_drivers
import XPS_C8_drivers
import sys
# Display error function: simplify error print out and closes socket
def displayErrorAndClose (socketId, errorCode, APIName):
	if (errorCode != -2) and (errorCode != -108):
		[errorCode2, errorString] = myxps.ErrorStringGet(socketId, errorCode)
		if (errorCode2 != 0):
			print APIName + ': ERROR ' + str(errorCode)
		else:
			print APIName + ': ' + errorString
	else:
		if (errorCode == -2):
			print APIName + ': TCP timeout'
		if (errorCode == -108):
			print APIName + ': The TCP/IP connection was closed by an administrator'
	myxps.TCP_CloseSocket(socketId)
	return
# Instantiate the class
myxps = XPS_C8_drivers.XPS()
# Connect to the XPS
socketId = myxps.TCP_ConnectToServer('192.168.0.254', 5001, 20)
# Check connection passed
if (socketId == -1):
	print 'Connection to XPS failed, check IP & Port'
	sys.exit ()
# Add here your personal codes, below for example:
# Define the positioner
group = 'GROUP1' 
positioner = group + '.POSITIONER'
# Kill the group
[errorCode, returnString] = myxps.GroupKill(socketId, group)
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupKill')
	sys.exit ()
# Initialize the group
[errorCode, returnString] = myxps.GroupInitialize(socketId, group) 
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupInitialize')
	sys.exit ()
# Home search
[errorCode, returnString] = myxps.GroupHomeSearch(socketId, group)
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupHomeSearch')
	exit 
# Make some moves
# example absolute move: myxps.GroupMoveAbsolute(socketId, positioner, [degrees])
# for relative, replace Absolute with Relative
[errorCode, returnString] = myxps.GroupMoveRelative(socketId, positioner, [20.0])
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupMoveAbsolute')
	sys.exit ()

# get/set velocity?
[errorCode, currentVelocity] = myxps.GroupVelocityCurrentGet(socketId, positioner, 1)
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupVelocityCurrentGet')
	sys.exit ()
print 'Positioner ' +positioner + ' has velocity '+str(currentVelocity)
# Get current position
[errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupPositionCurrentGet')
	sys.exit ()
else:
	print 'Positioner ' + positioner + ' is in position ' +  str(currentPosition)
# Backward
[errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [-20.0])
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupMoveAbsolute')
	sys.exit ()
# Get current position
[errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
if (errorCode != 0):
	displayErrorAndClose (socketId, errorCode, 'GroupPositionCurrentGet')
	sys.exit ()
else:
	print 'Positioner ' + positioner + ' is in position ' +  str(currentPosition)
# Close connection
myxps.TCP_CloseSocket(socketId)
#----------- End of the demo program ----------#


