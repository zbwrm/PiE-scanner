import serial, os
from datetime import datetime, time
import numpy as np
import argparse, logging

logging.info('creating global variables...')
HERE = os.path.dirname(os.path.abspath(__file__))
H_RESOLUTION = 100
V_RESOLUTION = 100

logging.info('initializing...')
start_time = datetime.now()
parser = argparse.ArgumentParser(description='3D Scanner Interface Program')
parser.add_argument('filename', type=str,
                    help='Names the CSV that is created. ([filename].csv)')
args = parser.parse_args()
device = "/dev/cu.usbmodem14101"
baud   = "9600"

logging.info('creating file to write to...')
if f"{args.filename}.csv" in os.listdir("./scans"):
    logging.error(f"scans/{args.filename}.csv already exists")
    exit()
filename = os.path.join(HERE, f"./scans/{args.filename}.csv")
file = open(filename, 'w')
file.close()

logging.info('generating horizontal angles...')
u_angles = []
for i in range(H_RESOLUTION):
    pass
logging.info('generating vertical angles...')

# generate v angles
v_angles = []
for i in range(V_RESOLUTION):
    pass


# take data
out_array = np.zeros((u, v))
with serial.Serial(device,baud) as ser:
    for u in u_angles:
        for v in v_angles:
            logging.debug(f'ordering arduino to rotate to {round(u,2)} and {round(v,2)}...')
            ser.write(bytes(str(u) + " " + str(v)))
            time.sleep(0.025)
            logging.debug(f'accepting averaged measurement from arduino...')
            in_data = ser.readline()
            logging.info(f'measuring {round(in_data,2)} at {round(u,2)} and {round(v,2)}')
            out_array[u, v] = in_data
    # while 1:
    #     line = serial_port.readline()

    #     # input_1 = int(new_data[0]) / 1024.0
    #     # rolling_1 = array_rotate(rolling_1, input_1)
    #     # rolling_1_avg = avg(rolling_1)

    #     # input_2 = int(new_data[1]) / 1024.0
    #     # rolling_2 = array_rotate(rolling_2, input_2)
    #     # rolling_2_avg = avg(rolling_2)

    #     timediff = (datetime.now() - start_time).total_seconds()

    #     outstring = f"{timediff},{rolling_1_avg},{rolling_2_avg}\n"
    #     log_file.write(outstring)
    #     print(outstring)
    #     log_file.flush()

np.savetxt(filename, out_array)