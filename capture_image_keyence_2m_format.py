import cv2
from pypylon import pylon


# ================================================
#   Connect to camera
# ================================================

camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice()
)

camera.Open()


# ================================================
#   Capture image
# ================================================

grab_result = camera.GrabOne(
    5000,
    pylon.TimeoutHandling_ThrowException,
)

if grab_result.GrabSucceeded():
    image = grab_result.Array

    print("撮像成功")
    print("元画像サイズ:", image.shape)


    # ================================================
    #   Convert to KEYENCE 2M format
    # ================================================

    # Crop the center 1600 pixels horizontally
    image = image[:, 160:1760]

    # Add 60 black pixels to the top and bottom
    image = cv2.copyMakeBorder(
        image,
        60,
        60,
        0,
        0,
        cv2.BORDER_CONSTANT,
        value=0,
    )

    print("変換後サイズ:", image.shape)


    # ================================================
    #   Save image
    # ================================================

    cv2.imwrite("image.bmp", image)


    # ================================================
    #   Display image
    # ================================================

    cv2.imshow("Basler Camera - KEYENCE 2M Format", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ================================================
#   Cleanup
# ================================================

grab_result.Release()
camera.Close()