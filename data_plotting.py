import os, argparse, logging
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logging.basicConfig(level=logging.INFO)

HERE = os.path.dirname(os.path.abspath(__file__))


parser = argparse.ArgumentParser(description='3D Scanner Plotting Program')
parser.add_argument('filename', type=str,
                    help='The filename to be read and plotted. (scans/[filename].csv)')

parser.add_argument('data_type', type=str,
                    help="Whether you're accessing data pre- or post-processing. ('raw' looks at raw sensor data, 'post' looks at data after conversion to Cartesian coordinates)")

args = parser.parse_args()

logging.info(f"looking for file {args.filename} in ./scans/...")
if f"{args.filename}.csv" not in os.listdir("./scans"):
    logging.error(f"there is no file named {args.filename} in ./scans/")
logging.info(f"./scans/{args.filename} found!")

logging.info(f'reading in data...')
df = pd.read_csv(f'./scans/{args.filename}.csv')

sns.set(style = "darkgrid")

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

if args.data_type == 'post':
    x = df['X']
    y = df['Y']
    z = df['Z']

    ax.set_xlabel("X (cm)")
    ax.set_ylabel("Y (cm)")
    ax.set_zlabel("Z (cm)")

    ax.scatter(x, y, z, marker='.', s=5)
    plt.show()
    
if args.data_type == 'raw':
    d = df['D']
    u = df['U']
    v = df['V']

    ax.set_zlabel("D (?)")
    ax.set_xlabel("U (deg)")
    ax.set_ylabel("V (deg)")

    ax.scatter(u, v, d, marker='.', s=5)
    plt.show()