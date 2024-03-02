import cv2
import numpy as np
from math import hypot

points = []
distances = []
start_point = None
enable_measurement = True  # Flag to enable/disable measurements

def calculate_distance(point1, point2, conversion_factor):
    distance_pixels = np.linalg.norm(np.array(point2) - np.array(point1))
    distance_mm = distance_pixels * conversion_factor
    return distance_mm

def draw_distances(image, distances):
    for i in range(len(distances)):
        dist_text = f"{distances[i]:.2f} mm"
        cv2.putText(image, 'Distance', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.05, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(image, dist_text, (90, 200 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.05, (255, 255, 255), 1, cv2.LINE_AA)

def delete_last_distance():
    global distances, img
    if distances:
        distances.pop()
        img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)  # Reset the image
        draw_distances(img, distances)  # Redraw distances on the updated image
        cv2.imshow('title', img)

def click_event(event, x, y, flags, param):
    global points, distances, img, start_point, enable_measurement
    if enable_measurement:
        if event == cv2.EVENT_LBUTTONDOWN:
            if start_point is None:
                start_point = (x, y)
                cv2.circle(img, start_point, 5, (0, 0, 255), -1)
            else:
                end_point = (x, y)
                points.extend([start_point, end_point])

                # Assuming a conversion factor of 1 pixel = 0.1 millimeters
                conversion_factor = 0.01009  # Change this based on your image's scale

                # Calculate and add distance to the list
                distance = calculate_distance(start_point, end_point, conversion_factor)
                distances.append(distance)

                # Draw distances directly on the image with larger font
                draw_distances(img, distances)

                # Draw a line between the points
                cv2.line(img, start_point, end_point, (255, 0, 0), 2)

                # Draw both start and end points with different markers
                cv2.circle(img, start_point, 5, (0, 0, 255), -1)
                cv2.circle(img, end_point, 5, (0, 255, 0), -1)

                # Clear start_point for the next measurement
                start_point = None

                # Display the updated image
                cv2.imshow('title', img)

# OpenCV video capture
cap = cv2.VideoCapture(1)  # Change the index to 1 for your camera

while True:
    ret, img = cap.read()  # Capture frame-by-frame
    if not ret:
        print("Failed to capture frame")
        break

    # Make the window fullscreen
    cv2.namedWindow('title', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('title', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # TITLE TEXT
    cv2.putText(img, 'STARZ ELECTRONICS', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.05, (255, 255, 255), 1,
                cv2.LINE_AA)

    cv2.putText(img, 'Press "d" key to delete last measurement ', (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.01,
                (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, 'Press "m" key to disable or enable manual mode ', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.01,
                (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, 'Press "e" or "Exit" to close window  ', (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.01,
                (255, 255, 255), 1, cv2.LINE_AA)

    if enable_measurement:
        # PCB RECTANGLE
        cv2.rectangle(img, (1398, 930), (2698, 2070), (255, 0, 0), 2)

        # PCB AXIS RECTANGLE
        cv2.rectangle(img, (2048, 1500), (2698, 2070), (255, 0, 0), 2)
        cv2.rectangle(img, (1398, 930), (2048, 1500), (255, 0, 0), 2)

        # SPRING 6 RECTANGLE
        cv2.rectangle(img, (1623, 1790), (1723, 1550), (255, 0, 0), 2)
        cv2.circle(img, (1673, 1630), 5, (0, 0, 255), 2)
        cv2.putText(img, 'SPF6', (1473, 1630), cv2.FONT_HERSHEY_SIMPLEX, 0.01, (255, 255, 255), 1, cv2.LINE_AA)

        # SPRING 5 RECTANGLE
        cv2.rectangle(img, (1623, 2070), (1723, 1830), (255, 0, 0), 2)
        cv2.circle(img, (1673, 1910), 5, (0, 0, 255), 2)
        cv2.putText(img, 'SPF5', (1623, 2148), cv2.FONT_HERSHEY_SIMPLEX, 0.01, (255, 255, 255), 1, cv2.LINE_AA)

        # SPRING 4 RECTANGLE
        cv2.rectangle(img, (1873, 2060), (1973, 1830), (255, 0, 0), 2)
        cv2.circle(img, (1923, 1910), 5, (0, 0, 255), 2)
        cv2.putText(img, 'SPF4', (1900, 2148), cv2.FONT_HERSHEY_SIMPLEX, 0.01, (255, 255, 255), 1, cv2.LINE_AA)

        # SPRING 3 RECTANGLE
        cv2.rectangle(img, (2123, 2060), (2223, 1830), (255, 0, 0), 2)
        cv2.circle(img, (2173, 1910), 5, (0, 0, 255), 2)
        cv2.putText(img, 'SPF3', (2153, 2148), cv2.FONT_HERSHEY_SIMPLEX, 0.01, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('title', img)

    if cv2.waitKey(1) & 0xFF in [ord('e'), ord('E')]:
        break

cap.release()
cv2.destroyAllWindows()
