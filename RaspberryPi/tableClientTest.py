from networktables import NetworkTable
import visiontable
import time

table = visiontable.VisionTable()

i = 0
while True:
  table.update(True, 4 + i, 5 + i)
  i += 1
  print(i)
  time.sleep(1)
