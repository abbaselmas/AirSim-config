# In settings.json first activate computer vision mode: 
# https://github.com/Microsoft/AirSim/blob/main/docs/image_apis.md#computer-vision-mode

import airsim
import pprint
import tempfile
import os
import time
import math

pp = pprint.PrettyPrinter(indent=4)

client = airsim.VehicleClient()

airsim.wait_key('Press any key to get camera parameters')
camera_info = client.simGetCameraInfo("front_center")
print("Font Center CameraInfo : %s" % (pp.pprint(camera_info)))

airsim.wait_key('Press any key to start getting images')
tmp_dir = r"G:\Drive'ım\Dataset\AirSimNH"

print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise
    
increment = 1
step = 20
z = -70
up = 111 #150+1 for range last element
down = -110

for layer in [1, 2, 3]:
    for y in range(down, up, step):
        for x in range(down, up, step):
            for pitch in [-120, -90, -60]:
                for yaw in [-90, 0]:
                    if pitch == -90 and yaw == -90:
                        continue
                    client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(math.radians(pitch), 0, math.radians(yaw))), True)
                    time.sleep(0.1)

                    responses = client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene)])
                    response = responses[0]

                    print(pprint.pformat(response.camera_position))
                    airsim.write_file(os.path.normpath(os.path.join(tmp_dir, "Layer" + str(layer) 
                                                                            + "_" + str(increment) 
                                                                            + "_z" + str(z) 
                                                                            + "_y" + str(y) 
                                                                            + "_x" + str(x) 
                                                                            + "_pitch" + str(pitch)
                                                                            + "_yaw" + str(yaw) + '.png')), response.image_data_uint8)
                    print(  "Layer" + str(layer) 
                            + "_" + str(increment) 
                            + "_z" + str(z) 
                            + "_y" + str(y) 
                            + "_x" + str(x) 
                            + "_pitch" + str(pitch)
                            + "_yaw" + str(yaw) + '.png')
                    increment += 1
            
        pose = client.simGetVehiclePose()
        pp.pprint(pose)   
    up -= 10
    down += 10
    z -= 20
step += 5
    

# currently reset() doesn't work in CV mode. Below is the workaround
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)