#!/usr/bin/env python

from networktables import NetworkTable
import time

table = NetworkTable.getTable("rpi")

while True:
  print(table.getNumber("visionX",-1))
  time.sleep(1)
