import serial, struct, os, time
from datetime import datetime
import numpy as np
import argparse, logging

logging.basicConfig(level=logging.INFO)

logging.info('creating global variables...')
HERE = os.path.dirname(os.path.abspath(__file__))
H_ANGLE_RANGE_MAX = [-85, 0] # max horizontal angular range of motion (in degrees)
V_ANGLE_RANGE_MAX = [-40, 15] # max vertical range of motion (in degrees)

H_ANGLE_RANGE = [-60, -25] # horizontal angular range of motion (in degrees)
V_ANGLE_RANGE = [-30, 5] # vertical range of motion (in degrees)
DIST = 0;                 # distance from part

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

out_array = np.empty((1,3))
print(out_array)
logging.info('initializing serial connection...')

with serial.Serial(device,baud) as ser:
    while (ser.readline().strip() != b'<open>'):
        continue
    
    for u in range(H_ANGLE_RANGE[0], H_ANGLE_RANGE[1]):
        for v in range(V_ANGLE_RANGE[0], V_ANGLE_RANGE[1]):
            logging.debug("waiting for arduino's ready signal...")

            while (ser.readline().strip() != b'<angles>'):
                continue


            logging.debug(f'ordering arduino to rotate to {u} and {v}...')
            ser.write((u+90).to_bytes(1, 'little')+(v+90).to_bytes(1, 'little'))

            logging.debug('accepting averaged measurement from arduino...')
            d = int(ser.readline().strip().decode('utf-8'))

            DIST = 152 - (8.48*d) + (7.99*(d**2)) - (.775*(d**3)) + (.0344*(d**4))
            
            logging.info(f'measured {d} at {u} and {v}')
            x = DIST * np.cos(np.radians(v)) * np.sin(np.radians(u))
            y = DIST * np.cos(np.radians(v)) * np.cos(np.radians(u))
            z = DIST * np.sin(np.radians(v))
            out_array = np.vstack([out_array,[x,y,z]])

np.savetxt(filename, out_array, delimiter=",")