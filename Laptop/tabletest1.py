from networktables import NetworkTable

NetworkTable.setIPAddress("10.0.0.2")
NetworkTable.setClientMode()
NetworkTable.initialize()

table = NetworkTable.getTable("rpi")

table.putNumber("visionX", 2)
table.putNumber("visionY", 4)

print("done")
