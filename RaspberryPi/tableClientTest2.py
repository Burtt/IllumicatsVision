from networktables import NetworkTable
import time

NetworkTable.setIPAddress("10.32.42.20")
NetworkTable.setClientMode()
NetworkTable.initialize()
table = NetworkTable.getTable("rpi")

