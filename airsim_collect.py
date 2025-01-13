import airsim
import pprint
import os
import time
import math

pp = pprint.PrettyPrinter(indent=4)
client = airsim.VehicleClient()

# Configuration
tmp_dir = r"D:\GDrive\Drive'ım\Dataset\AirSimNH-natural"
print("Saving images to %s" % tmp_dir)

try:
    os.makedirs(tmp_dir, exist_ok=True)
except OSError:
    raise

# Photogrammetry parameters
FOV = 90  # degrees
STEP = 53  # Optimized step size
OVERLAP = 0.70  # 70% overlap

# Layer configurations with optimized heights and aligned nodes
layer_configs = {
    1: {  # Top layer (3x3)
        "size": 3,
        "altitude": -140,
        "points": [-50, 0, 50]
    },
    2: {  # Middle layer (5x5)
        "size": 5,
        "altitude": -110,
        "points": [-100, -50, 0, 50, 100]
    },
    3: {  # Bottom layer (7x7)
        "size": 7,
        "altitude": -80,
        "points": [-150, -100, -50, 0, 50, 100, 150]
    }
}

# Camera settings
PITCH_ANGLE = -60
increment = 1

print(f"\nPhotogrammetry Survey Configuration:")
print(f"Field of View: {FOV}°")
print(f"Overlap: {OVERLAP*100}%")
print(f"Step size: {STEP} units")

for layer in [1, 2, 3]:
    config = layer_configs[layer]
    altitude = config["altitude"]
    size = config["size"]
    points = config["points"]
    
    # Calculate ground coverage at this height
    ground_coverage = 2 * abs(altitude)
    effective_overlap = 1 - (STEP / ground_coverage)
    
    print(f"\nLayer {layer} ({size}x{size}):")
    print(f"Altitude: {abs(altitude)} units")
    print(f"Ground coverage per image: {ground_coverage:.1f} units")
    print(f"Effective overlap: {effective_overlap*100:.1f}%")
    print(f"Points: {points}")
    
    moving_right = True
    
    for y in points:
        if moving_right:
            x_range = points
            YAW_ANGLE = 0
        else:
            x_range = points[::-1]
            YAW_ANGLE = 180
        
        for x in x_range:
            pose = airsim.Pose(
                airsim.Vector3r(x, y, altitude),
                airsim.to_quaternion(math.radians(PITCH_ANGLE), 0, math.radians(YAW_ANGLE))
            )
            client.simSetVehiclePose(pose, True)
            
            time.sleep(0.1)
            
            responses = client.simGetImages([
                airsim.ImageRequest("front_center", airsim.ImageType.Scene)
            ])
            
            folder_path = os.path.join(tmp_dir, f"Layer{layer}")
            os.makedirs(folder_path, exist_ok=True)
            
            image_path = os.path.join(folder_path, f"{increment}_z{altitude}_y{y}_x{x}.png")
            airsim.write_file(os.path.normpath(image_path), responses[0].image_data_uint8)
            
            print(f"Saved {image_path}")
            increment += 1
        
        moving_right = not moving_right

# Reset vehicle pose
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)