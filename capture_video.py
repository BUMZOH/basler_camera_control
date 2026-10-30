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
#   Start continuous capture
# ================================================

# Start continuous image acquisition
# LatestImageOnly keeps only the latest image when processing falls behind
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)


# ================================================
#   Capture and display images
# ================================================

while camera.IsGrabbing():
    # Retrieve one image from the camera
    # Timeout: 5000 ms
    grab_result = camera.RetrieveResult(
        5000,
        pylon.TimeoutHandling_ThrowException,
    )

    if grab_result.GrabSucceeded():
        # Convert the captured image to a NumPy array
        image = grab_result.Array

        # Display the image using OpenCV
        cv2.imshow("Basler Camera", image)

    # Release the captured image buffer
    grab_result.Release()

    # Press ESC to stop continuous capture
    if cv2.waitKey(1) == 27:
        break


# ================================================
#   Cleanup
# ================================================

# Stop continuous image acquisition
camera.StopGrabbing()

# Close the camera
camera.Close()

# Close the OpenCV window
cv2.destroyAllWindows()