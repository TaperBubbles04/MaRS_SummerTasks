import cv2
try:
    import cv2.aruco as aruco
    try:
        dictionary = aruco.Dictionary_get(aruco.DICT_5X5_250)
        img = aruco.drawMarker(dictionary, 50, 500)
    except AttributeError:
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
        img = aruco.generateImageMarker(dictionary, 50, 500)
    cv2.imwrite('/home/taper/ros2_ws/src/task3-5/robotsim/worlds/aruco_marker_50.png', img)
    print("SUCCESS: Marker successfully generated and saved!")
except Exception as e:
    print(f"FAILED: {e}")