from mlx90632.mlx90632 import *
from datetime import datetime
import sys


def main():
  if len(sys.argv) <= 1:
    print("Usage:")
    print("mlx90632-dump <interface> <read_count>\n")

    print("The first argument needs to be the url of the interface to connect (e.g. I2C-1, ftdi://ftdi:2232/1, mlx://evb:90632/1)")
    print("  This argument can also be 'auto', works only when 1 comport on system\n")
    print("examples:")
    print(" - mlx90632-dump mlx://evb:90632/2        ==> read 10 frames from 2nd EVB90632 connected to the computer")
    print(" - mlx90632-dump I2C-1                    ==> read 10 frames on I2C-1 bus on single board computer")
    print(" - mlx90632-dump ftdi://ftdi:2232/1       ==> read 10 frames on FTDI FT232H or FT2232H on USB port")
    print(" - mlx90632-dump auto                     ==> read 10 frames from 1st EVB90632")
    print(" - mlx90632-dump auto 1                   ==> read 1 frame from 1st EVB90632")
    print(" - mlx90632-dump 100                      ==> read 100 frames")
    print(" - mlx90632-dump 1000                     ==> read 1000 frames")
    print(" - mlx90632-dump 100                      ==> read 100 frames")
    print(" - mlx90632-dump 0                        ==> read 0 frames -> find out which comport is assigned")
    print("")
    exit(1)

  max_readings = 10
  interface = 'auto'

  if len(sys.argv) >= 2:
    if sys.argv[1].isdigit():
      max_readings = int(float(sys.argv[1]))
    else:
      interface = sys.argv[1]

  if len(sys.argv) >= 3:
    if sys.argv[2].isdigit():
      max_readings = int(float(sys.argv[2]))

  dev = Mlx90632(interface)
  dev.init()
  dev.read_chipid()
  print ("chipid = {}".format (dev.chipid))
  print ("chipid = {}".format (dev.chipid_str))

  reading_count = 0
  previous_time = datetime.now()
  dev.reset()

  print ("\n\nReading {}x".format(max_readings))

  dev.write_control_mode(STEP_SLEEP)
  dev.write_control_sob()

  import time

  sleep_start = datetime.now()
  state = 0 # measure; wait new_data
  while reading_count < max_readings:
    raw_data = None
    try:
      # if dev.wait_new_data(2):
      #   raw_data = dev.read_measurement_data()
      #   dev.reset()
      #   dev.set_brownout()
      if state == 1: # sleep
        time.sleep(0.01)
        if (datetime.now() - sleep_start).total_seconds() > 5: # awake after 5 sec..
          print ('SOB start trigger!')
          dev.write_control_sob()
          state = 0

      if state == 0: # measuring
        if dev.wait_eoc(0.1): # check if new_data...
          # print ("EOC", EOC)
          raw_data = dev.read_measurement_data()
          # dev.read_status()
          # new_status_value = dev.reg_status & ~0x0002
          # dev.hw.i2c_write (dev.i2c_addr, 0x3FFF, new_status_value)

          print ('cycle_pos', dev.reg_status_cycle_position, 'RAM[4..9]', raw_data)
          sleep_start = datetime.now()
          state = 1

      # print (raw_data)
    except Exception as e:
      dev.clear_error()
      print(e)
      pass

    if raw_data is not None:
      ta, to = dev.do_compensation(raw_data)
      now_time = datetime.now()
      delta_time = now_time - previous_time
      previous_time = now_time

      print("TA = {:6.2f}  | TO = {:6.2f}  | VddMon = {:6.2f}  -- {}".format (ta, to, dev.read_vddmonitor(), str(delta_time)))
  
      reading_count += 1

  dev.disconnect()



if __name__ == '__main__':
    main()
