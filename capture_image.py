import cv2
from pypylon import pylon


# ================================================
#   Connect to camera
# ================================================

# Create a camera object using the first detected Basler camera
camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice()
)

# Open the camera
camera.Open()


# ================================================
#   Capture image
# ================================================

# Capture one image
# Timeout: 5000 ms
grab_result = camera.GrabOne(
    5000,
    pylon.TimeoutHandling_ThrowException,
)

if grab_result.GrabSucceeded():
    # Convert the captured image to a NumPy array
    image = grab_result.Array

    print("撮像成功")
    print("画像サイズ:", image.shape)
    print("データ型:", image.dtype)


    # ================================================
    #   Save image
    # ================================================

    # Save the captured image as a PNG file
    cv2.imwrite("image.png", image)


    # ================================================
    #   Display image
    # ================================================

    # Display the captured image using OpenCV
    cv2.imshow("Basler Camera", image)

    # Wait until any key is pressed
    cv2.waitKey(0)

    # Close the OpenCV window
    cv2.destroyAllWindows()


# ================================================
#   Cleanup
# ================================================

# Release the captured image buffer
grab_result.Release()

# Close the camera
camera.Close()