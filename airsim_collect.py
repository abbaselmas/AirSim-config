import airsim
import pprint
import os
import time
import math

pp = pprint.PrettyPrinter(indent=4)
client = airsim.VehicleClient()

airsim.wait_key('Press any key to start getting images')
tmp_dir = r"D:\GDrive\Drive'ım\Dataset\AirSimNH"
print("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir, exist_ok=True)  # Ensure the root directory exists
except OSError:
    raise

increment = 1
step = 40
z = -60
up = 160  # Y-axis upper bound
down = -160  # Y-axis lower bound

for layer in [1, 2, 3]:
    serpentine = True  # Used to toggle y-direction
    for y in range(down, up+1, step):  # Move along x-axis in one direction for the entire layer
        if serpentine:
            x_range = range(down, up+1, step)  # Move upwards
        else:
            x_range = range(up, down-1, -step)  # Move downwards
            
        for x in x_range:
            for pitch in [-120, -90, -60]:
                for yaw in [-90, 0]:
                    if pitch == -90 and yaw == -90:
                        continue
                    
                    # Set vehicle pose
                    client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(math.radians(pitch), 0, math.radians(yaw))), True)
                    time.sleep(0.1)

                    # Get image response
                    responses = client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene)])
                    response = responses[0]

                    # Create the necessary folder for each combination of Layer, pitch, and yaw
                    folder_path = os.path.join(tmp_dir, f"Layer{layer}/pitch{pitch}_yaw{yaw}")
                    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder is created

                    # Save the image to the folder
                    image_path = os.path.join(folder_path, f"{increment}_z{z}_y{y}_x{x}.png")
                    airsim.write_file(os.path.normpath(image_path), response.image_data_uint8)

                    print(f"Saved {image_path}")
                    increment += 1
        
        # Toggle y-direction after each x-row to get serpentine effect
        serpentine = not serpentine

    down += step
    up -= step
    z -= step

# Reset vehicle pose
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)