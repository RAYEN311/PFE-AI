import cv2
import numpy as np

# Load the design image with alpha channel
design_image = cv2.imread('design.png', cv2.IMREAD_UNCHANGED)

# Function to detect PCBs in an image
def detect_pcbs(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop over contours
    for contour in contours:
        # Approximate the contour
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        # If the contour has 4 vertices, check if it resembles a PCB
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            
            # Adjust these thresholds based PCB characteristics
            if 0.8 <= aspect_ratio <= 1.2 and cv2.contourArea(contour) > 1000:
                # Get the color of the PCB
                color = detect_color(frame, x, y, w, h)
                
                # Draw rectangle around PCB
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Get the minimum area bounding rectangle

                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                # Draw the rotated bounding box
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
#prop solution
                try:
                   seg = int(( (box[1][0] - box[0][0] )**2 - (box[1][1] - box[0][1] )**2) **0.5)
                except:
                   seg = 120  
            
                print(seg)
                # Extract the angle of rotation
                angle = rect[2]

                # Put text with angle
                cv2.putText(frame, f"Angle: {angle}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Put text with shape and color
                cv2.putText(frame, f"Shape: PCB\nColor: {color}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                # Place the design image in the middle of the PCB
                if 'design_image' in globals():


                    design_height = int(seg / 2.4)
                    design_width = design_height
                    # Calculate offsets to place design image at the center of the bounding box
                    offset_x = int(x + (w - design_width) / 2)
                    offset_y = int(y + (h - design_height) / 2)
                    # Ensure the design image fits into the frame
                    if offset_x >= 0 and offset_y >= 0:
                        # Extract the region of interest for the design image
                        roi = frame[offset_y:offset_y + design_height, offset_x:offset_x + design_width]
                        # Resize the design image to match the size of the ROI if necessary
                        design_image_resized = cv2.resize(design_image, (roi.shape[1], roi.shape[0]))
                        # Create a binary mask for the design image
                        mask = design_image_resized[:, :, 3] / 255.0
                        # Invert the mask
                        mask_inv = 1.0 - mask
                        # Blend the design image and the frame
                        for c in range(3):
                            roi[:, :, c] = (mask * design_image_resized[:, :, c] + mask_inv * roi[:, :, c]).astype(np.uint8)
                        # Update the frame with the blended image
                        frame[offset_y:offset_y + design_height, offset_x:offset_x + design_width] = roi
                        
    return frame

# Function to detect color of PCB
def detect_color(frame, x, y, w, h):
    roi = frame[y:y+h, x:x+w]
    
    # Convert ROI to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Define color ranges
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])
    
    lower_green = np.array([40, 50, 50])  # Adjusted green range
    upper_green = np.array([80, 255, 255]) # Adjusted green range
    
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # Threshold the HSV image to get only desired colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Combine masks for red since it's in two ranges
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Find the largest contour in each mask
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the color with the largest contour
    color = None
    if len(contours_blue) > len(contours_green) and len(contours_blue) > len(contours_red):
        color = "Blue"
    elif len(contours_green) > len(contours_blue) and len(contours_green) > len(contours_red):
        color = "Green"
    elif len(contours_red) > len(contours_blue) and len(contours_red) > len(contours_green):
        color = "Red"
    else:
        color = "Unknown"
    
    return color

# Main function
def main():
    # Open webcam with index 1
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Detect PCBs in the frame
            frame_with_pcbs = detect_pcbs(frame)

            # Display the resulting frame
            cv2.imshow('PCB Detection', frame_with_pcbs)

            # Exit on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Failed to capture frame.")
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
