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
for camera_id in range(2):
    camera_info = client.simGetCameraInfo(str(camera_id))
    print("CameraInfo %d: %s" % (camera_id, pp.pprint(camera_info)))

airsim.wait_key('Press any key to get images')
tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise
    
increment = 0
step = 10
z = -100
degree = -90

for y in range(-150, +150, step):
    for x in range(-150, +150, step):
        client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x, y, z), airsim.to_quaternion(math.radians(degree), 0, 0)), True)
        time.sleep(0.1)

        responses = client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene)])
        response = responses[0]

        print(pprint.pformat(response.camera_position))
        airsim.write_file(os.path.normpath(os.path.join(tmp_dir, str(increment) + "_" + str(x) + "_" + str(y) + str(z) + '.png')), response.image_data_uint8)
        print(str(increment) + "_" + str(x) + "_" + str(y) + str(z) + '.png')
        increment += 1

    pose = client.simGetVehiclePose()
    pp.pprint(pose)

    time.sleep(0.1)

# currently reset() doesn't work in CV mode. Below is the workaround
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)