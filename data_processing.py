import serial, os, math
from datetime import datetime
import numpy as np
import argparse, logging

logging.basicConfig(level=logging.INFO)

logging.info('creating global variables...')
HERE = os.path.dirname(os.path.abspath(__file__))

H_ANGLE_RANGE = range(-80, -20) # horizontal angular range of motion (in degrees)
# V_ANGLE_RANGE = range(-60, -15) # vertical range of motion (in degrees)
V_ANGLE_RANGE = range(-23, -22) # vertical range of motion (in degrees)


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
filename_raw = os.path.join(HERE, f"./scans/{args.filename}_raw.csv")
filename_heat = os.path.join(HERE, f"./scans/{args.filename}_heat.csv")

file = open(filename, 'w')
file.close()
file = open(filename_raw, 'w')
file.close()
file = open(filename_heat, 'w')
file.close()




out_array = np.array(['X', 'Y', 'Z'])
raw_array = np.array(['D', 'U', 'V'])
heat_array = np.empty((len(H_ANGLE_RANGE), len(V_ANGLE_RANGE)))
logging.info('initializing serial connection...')

with serial.Serial(device,baud) as ser:
    while (ser.readline().strip() != b'<open>'):
        continue

    for i in range(len(H_ANGLE_RANGE)):
        for j in range(len(V_ANGLE_RANGE)):
            u = H_ANGLE_RANGE[i]
            v = V_ANGLE_RANGE[j]
            logging.debug("waiting for Arduino's ready signal...")

            while (ser.readline().strip() != b'<angles>'):
                continue

            logging.debug(f'ordering arduino to rotate to {u} and {v}...')
            ser.write((u+90).to_bytes(1, 'little')+(v+90).to_bytes(1, 'little'))

            logging.debug('accepting averaged measurement from arduino...')
            d = int(ser.readline().strip().decode('utf-8'))

            # DIST = 152 - (8.48*d) + (7.99*(d**2)) - (.775*(d**3)) + (.0344*(d**4))
            # DIST = 1335 - (23.1*d) + (0.176*d**2) - (.00071*d**3) + (.0000016*d**4) - (.00000000188*d**5) + (.00000000000091*d**6)
            DIST = 153.38 * math.exp(-0.005*d)
            
            logging.info(f'measured {d} at {u} and {v}')
            x = DIST * np.cos(math.radians(v)) * np.sin(math.radians(u))
            y = DIST * np.cos(math.radians(v)) * np.cos(math.radians(u))
            z = DIST * np.sin(math.radians(v))
            if DIST < 200:
                out_array = np.vstack([out_array,[x,y,z]])
            raw_array = np.vstack([raw_array, [d,u,v]])
            heat_array[i, j] = DIST
            

np.savetxt(filename, out_array, delimiter=",", fmt='%s')
np.savetxt(filename_raw, raw_array, delimiter=',', fmt='%s')
np.savetxt(filename_heat, heat_array, delimiter=',', fmt='%s')