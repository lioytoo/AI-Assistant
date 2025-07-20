import cv2 as cv
import numpy as np
import time

def detect_motion_in_bed(debug = True):
    cap = cv.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("❌ Could not open camera. Please check your camera and try again.")
        return False
    backsub = cv.createBackgroundSubtractorMOG2()

    # Bed polygon points ( must match your red box)
    bed_area = np.array([[30,190],[580,180],[580,330],[30,330]])
    motion_in_bed = False
    
    # 🔄 Warm-up: Let the model learn the background
    for _ in range(60):
        ret, frame = cap.read()
        if not ret:
            print("cant grab frames")
            break
        backsub.apply(frame) # Just update background model - no detection here

    # Start actual motion detection for 5 seconds so it won't run forever
    start_time = time.time()
    while time.time() - time.time() < 5:
        ret, image = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
         
        if time.time() - start_time > 5:
            break
        

        fgmask = backsub.apply(image)

        # Clean up mask: remove small white dots and fill gaps
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel, iterations=1)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel, iterations=2)

        # Detect motion in the bed area (find contours)
        contours, _= cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Convert fgmask to color so we can dwaw in red
        fg_bgr = cv.cvtColor(fgmask, cv.COLOR_GRAY2BGR)

        for cnt in contours:
            if cv.contourArea(cnt) < 500: # Skip small movment
                continue
            x, y, w, h = cv.boundingRect(cnt)
            center = (x + w // 2, y + h // 2)

            # check if center of motion is inside the bed area
            if cv.pointPolygonTest(bed_area, center, False) >= 0:
                motion_in_bed = True
                # Draw the detected motion
                cv.rectangle(fg_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if debug:
                    print("Motion detected")

        # Lines to set bed boundaries
        lines = [
            ((30, 190), (580, 180)),  # Top boundary
            ((70, 330), (580, 330)),  # Bottom boundary
            ((30, 190), (70, 330)),  # Left boundary
            ((580, 330), (580, 180))   # Right boundary
        ]
        for line in lines:
            cv.line(fg_bgr, line[0], line[1], (0, 0, 255), 2)
            cv.line(image, line[0], line[1], (0, 0, 255), 2)

            # Display status box
            text = "motion detected in area" if motion_in_bed else "no motion in area"
            color = (0, 0, 255) if motion_in_bed else (0, 255, 0)


            cv.rectangle(image, (10, 10), (270,40), (255,255,255), -1)
            cv.putText(image, text, (15, 33), cv.FONT_HERSHEY_SIMPLEX, 0.6 , color, 2)

            cv.rectangle(fg_bgr, (10, 10), (270,40), (255,255,255), -1)
            cv.putText(fg_bgr, text, (15, 33), cv.FONT_HERSHEY_SIMPLEX, 0.6 , color, 2)

           
        if debug:
            # Show frames with lines and text
            cv.imshow('Live Feed', image)
            cv.imshow('Foreground Mask + Motion', fg_bgr)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        #time.time(20)
            
    cap.release()
    cv.destroyAllWindows()
    return motion_in_bed

if __name__ == "__main__":
    print("Checking for motion in bed area...")
    result = detect_motion_in_bed(debug = True)
    if result:
        print("✅ Motion detected inside bed area!")
    else:
        print("❌ No motion detected in bed area.")
