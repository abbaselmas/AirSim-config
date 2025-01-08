import airsim
import keyboard  # Make sure to install this library

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

# Arm the drone and take off
client.armDisarm(True)
client.takeoffAsync(5).join()

velocity = 5  # Velocity of the drone

# Control loop
while True:
    if keyboard.is_pressed('w'):  # Move forward
        client.moveByVelocityAsync(velocity, 0, 0, 1).join()
    elif keyboard.is_pressed('s'):  # Move backward
        client.moveByVelocityAsync(-velocity, 0, 0, 1).join()
    elif keyboard.is_pressed('a'):  # Move left
        client.moveByVelocityAsync(0, -velocity, 0, 1).join()
    elif keyboard.is_pressed('d'):  # Move right
        client.moveByVelocityAsync(0, velocity, 0, 1).join()
    elif keyboard.is_pressed('q'):  # Rotate left
        client.rotateByYawRateAsync(-10, 1).join()
    elif keyboard.is_pressed('e'):  # Rotate right
        client.rotateByYawRateAsync(10, 1).join()
    elif keyboard.is_pressed('space'):  # Land
        client.landAsync().join()
        break

# Disarm the drone after landing
client.armDisarm(False)
