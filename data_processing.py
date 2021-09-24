import serial, struct, os, time
from datetime import datetime
import numpy as np
import argparse, logging

logging.basicConfig(level=logging.DEBUG)

logging.info('creating global variables...')
HERE = os.path.dirname(os.path.abspath(__file__))
H_RESOLUTION  = 100       # how many horizontal samples
V_RESOLUTION  = 100       # how many vertical samples
H_ANGLE_RANGE = [-20, 20] # horizontal angular range of motion (in degrees)
V_ANGLE_RANGE = [-30, 30] # vertical range of motion (in degrees)
DIST = 0;                 # distance from part
logging.debug('determining filename...')
start_time = datetime.now()
parser = argparse.ArgumentParser(description='3D Scanner Interface Program')
parser.add_argument('filename', type=str,
                    help='Names the CSV that is created. ([filename].csv)')
args = parser.parse_args()

device = "/dev/cu.usbmodem14301"
baud   = "9600"

logging.info('creating file to write to...')
if f"{args.filename}.csv" in os.listdir("./scans"):
    logging.error(f"scans/{args.filename}.csv already exists")
    exit()
filename = os.path.join(HERE, f"./scans/{args.filename}.csv")
file = open(filename, 'w')
file.close()

logging.info('generating horizontal angles...')
u_angles = np.linspace(H_ANGLE_RANGE[0], H_ANGLE_RANGE[1], H_RESOLUTION)

logging.info('generating vertical angles...')
v_angles = np.linspace(V_ANGLE_RANGE[0], V_ANGLE_RANGE[1], V_RESOLUTION)

out_array = np.array(float)
logging.info('initializing serial connection...')

with serial.Serial(device,baud) as ser:
    while (ser.readline().strip() != b'<open>'):
        continue
    
    for u in u_angles:
        for v in v_angles:
            logging.debug(f'ordering arduino to rotate to {round(u,2)} and {round(v,2)}...')

            # this section heavily dependant on 2-way serial communication w/ the arduino. mostly TBD
            ser.write(struct.pack('2f', u, v))


            time.sleep(0.025)
            logging.debug('accepting averaged measurement from arduino...')
            d = struct.unpack('f', ser.readline().strip())
            q=d[0]
            DIST = 874+ -24.7*q+.341q^2+ -2.33*10^-3*q^3+6.68*10^6*q^4
            print(d[0])
            
             logging.info(f'measuring {round(d,2)} at {round(u,2)} and {round(v,2)}')
             x = DIST * np.cos(v) * np.sin(u)
             y = DIST * np.cos(v) * np.cos(u)
             z = DIST * np.sin(v)
             out_array.append(f'{x},{y},{z}\n')

np.savetxt(filename, out_array)
