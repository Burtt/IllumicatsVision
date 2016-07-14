#!/usr/bin/env python

from networktables import NetworkTable

#USB Rio IP: 172.22.11.2
#DHCP Rio IP Range: 10.32.42.20-199


class VisionTable:
  
  def __init__(self, ip="roboRIO-3242-FRC.local"):
    NetworkTable.setIPAddress(ip)
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    self.table = NetworkTable.getTable("rpi")

  def update(self, found, x=-1, y=-1):
    self.table.putNumber("visionX", x)
    self.table.putNumber("visionY", y)
    self.table.putBoolean("found", found)
