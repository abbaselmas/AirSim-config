# Import necessary libraries
import airgen
import time
import cv2
import numpy as np
# Initialize the AirGen client
client = airgen.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
# Takeoff to a safe altitude
#client.takeoffAsync().join()
client.moveToPositionAsync(0, 0, -60, 10).join()

# Function to move the drone and capture images
def capture_image_at_position(x, y, z, image_name):
    client.moveToPositionAsync(x, y, z, 10).join()  # Move to the specified position
    time.sleep(2)  # Allow time for the drone to stabilize

    # Capture image from the front center camera
    responses = client.simGetImages([airgen.ImageRequest("bottom_center", airgen.ImageType.Scene)])
    image_data = responses[0].image_data_uint8

    # Save the image
    image = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite(image_name, image)
    print(f"Captured image: {image_name}")

# Define grid boundaries and parameters
x_min, x_max = -100, 100  # X boundaries
y_min, y_max = -100, 100  # Y boundaries
step_size = 50            # Step size for each movement (meters)

# Set the altitude for capturing images
z = -60  # Flying altitude

# Start the grid traversal from the bottom-left corner of the grid
image_counter = 1
# Traverse the grid in a serpentine (zigzag) pattern
for y in range(y_min, y_max + step_size, step_size):
    x_range = range(x_min, x_max + step_size, step_size) if (y - y_min) // step_size % 2 == 0 else range(x_max, x_min - step_size, -step_size)
    for x in x_range:
        image_name = f"neighborhood_image_{image_counter}.png"
        capture_image_at_position(x, y, z, image_name)
        image_counter += 1

# Land the drone after capturing images
client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)

print("Grid traversal complete.")