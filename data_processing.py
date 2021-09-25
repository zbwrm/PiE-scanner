import serial, struct, os, time
from datetime import datetime
import numpy as np
import argparse, logging

logging.basicConfig(level=logging.DEBUG)

logging.info('creating global variables...')
HERE = os.path.dirname(os.path.abspath(__file__))

H_ANGLE_RANGE = [-20, 20] # horizontal angular range of motion (in degrees)
V_ANGLE_RANGE = [-30, 30] # vertical range of motion (in degrees)

logging.debug('determining filename...')
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

out_array = np.array(float)
logging.info('initializing serial connection...')

with serial.Serial(device,baud) as ser:
    while (ser.readline().strip() != b'<open>'):
        continue

    for u in range(H_ANGLE_RANGE[0],H_ANGLE_RANGE[1]):
        for v in range(V_ANGLE_RANGE[0],V_ANGLE_RANGE[1]):
            logging.debug(f'ordering arduino to rotate to {round(u,2)} and {round(v,2)}...')

            # this section heavily dependant on 2-way serial communication w/ the arduino. mostly TBD
            # ser.write(struct.pack('2i', u+90, v+90))
            print(struct.pack('2i', u+90, v+90))


            # time.sleep(0.025)
            # logging.debug('accepting averaged measurement from arduino...')
            # d = struct.unpack('f', ser.readline().strip())
            # print(d[0])
            # logging.info(f'measuring {round(d,2)} at {round(u,2)} and {round(v,2)}')
            # x = d * np.cos(v) * np.sin(u)
            # y = d * np.cos(v) * np.cos(u)
            # z = d * np.sin(v)
            # out_array.append(f'{x},{y},{z}\n')

np.savetxt(filename, out_array)