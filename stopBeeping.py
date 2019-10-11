from core.peripherals import *

def off():
  try:
   crc = crc8(0,BUZZER)
   crc = crc8(crc,VALS['OFF'])
   bus.write([BUZZER,VALS['OFF'],crc],ADDR_32U4)
   crca = bus.read(1,ADDR_32U4)
   time.sleep(0.001)
   if ([crc] != crca):
    print('crc8 error set clicksound')
  except:
   print('clicksound error')
