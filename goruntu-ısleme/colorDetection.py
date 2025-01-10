import cv2
import numpy as np
from collections import deque  # tespit edilen objenin merkezini depolamak için kullanılır

# nesne merkezini depolayacak veri tipi
buffer_size = 16  # deque nun boyutu
pts = deque(maxlen=buffer_size)  # nesnenin merkez noktaları

# renk aralıkları HSV formatında
lower_red1 = np.array([1, 170, 100])
upper_red1 = np.array([5, 255, 255])
lower_red2 = np.array([170, 170, 100])
upper_red2 = np.array([179, 255, 255])
lower_yellow = np.array([25, 100, 100])
upper_yellow = np.array([30, 255, 255])
lower_green = np.array([40, 100, 100])
upper_green = np.array([70, 255, 255])

# capture
cap = cv2.VideoCapture(0)
cap.set(3, 960)
cap.set(4, 480)
cap.set(10, 100)

def draw_contour(frame, rect, color, label):
    ((x, y), (width, height), rotation) = rect
    box = cv2.boxPoints(rect)
    box = np.int64(box)
    cv2.drawContours(frame, [box], 0, color, 2)
    cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 0), -1)
    cv2.putText(frame, label, (int(x) - 50, int(y) - 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

def merge_contours(contours, threshold):
    merged_contours = []
    merged_flags = [False] * len(contours)
    for i, cnt1 in enumerate(contours):
        if merged_flags[i]:
            continue
        new_contour_group = [cnt1]
        merged_flags[i] = True
        for j, cnt2 in enumerate(contours):
            if i == j or merged_flags[j]:
                continue
            M1 = cv2.moments(cnt1)
            M2 = cv2.moments(cnt2)
            if M1["m00"] != 0 and M2["m00"] != 0:
                cX1 = int(M1["m10"] / M1["m00"])
                cY1 = int(M1["m01"] / M1["m00"])
                cX2 = int(M2["m10"] / M2["m00"])
                cY2 = int(M2["m01"] / M2["m00"])
                dist = np.sqrt((cX1 - cX2) ** 2 + (cY1 - cY2) ** 2)
                if dist < threshold:
                    new_contour_group.append(cnt2)
                    merged_flags[j] = True
        if len(new_contour_group) > 1:
            combined_contour = np.vstack(new_contour_group)
            hull = cv2.convexHull(combined_contour)
            merged_contours.append(hull)
        else:
            merged_contours.append(cnt1)
    return merged_contours

def color_detect():
    if cap.isOpened():
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Frame okunmuyor")
                    break
                detected_objects = []

                blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                into_hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                mask_red1 = cv2.inRange(into_hsv, lower_red1, upper_red1)
                mask_red2 = cv2.inRange(into_hsv, lower_red2, upper_red2)
                mask_red = mask_red1 + mask_red2
                mask_yellow = cv2.inRange(into_hsv, lower_yellow, upper_yellow)
                mask_green = cv2.inRange(into_hsv, lower_green, upper_green)

                mask_red = cv2.erode(mask_red, None, iterations=2)
                mask_red = cv2.dilate(mask_red, None, iterations=2)
                _, mask_red = cv2.threshold(mask_red, thresh=200, maxval=255, type=cv2.THRESH_BINARY)
                mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
                mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)
                mask_green = cv2.erode(mask_green, None, iterations=2)
                mask_green = cv2.dilate(mask_green, None, iterations=2)

                (contours_red, _) = cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                (contours_yellow, _) = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                (contours_green, _) = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                MIN_CONTOUR_AREA = 200
                contours_red = [cnt for cnt in contours_red if cv2.contourArea(cnt) > MIN_CONTOUR_AREA]
                contours_yellow = [cnt for cnt in contours_yellow if cv2.contourArea(cnt) > MIN_CONTOUR_AREA]
                contours_green = [cnt for cnt in contours_green if cv2.contourArea(cnt) > MIN_CONTOUR_AREA]

                EPSILON = 0.03
                contours_red = [cv2.approxPolyDP(cnt, EPSILON * cv2.arcLength(cnt, True), True) for cnt in contours_red]
                contours_yellow = [cv2.approxPolyDP(cnt, EPSILON * cv2.arcLength(cnt, True), True) for cnt in contours_yellow]
                contours_green = [cv2.approxPolyDP(cnt, EPSILON * cv2.arcLength(cnt, True), True) for cnt in contours_green]

                merge_red = merge_contours(contours_red, 500)
                for c in merge_red:
                    rect = cv2.minAreaRect(c)
                    ((x, y), (width, height), rotation) = rect
                    detected_objects.append(("Red", x, y, width, height, rotation))
                    draw_contour(frame, rect, (0, 0, 255), "Red")

                merge_yellow = merge_contours(contours_yellow, 500)
                for c in merge_yellow:
                    rect = cv2.minAreaRect(c)
                    ((x, y), (width, height), rotation) = rect
                    detected_objects.append(("Yellow", x, y, width, height, rotation))
                    draw_contour(frame, rect, (0, 255, 255), "Yellow")

                merge_green = merge_contours(contours_green, 500)
                for c in merge_green:
                    rect = cv2.minAreaRect(c)
                    ((x, y), (width, height), rotation) = rect
                    detected_objects.append(("Green", x, y, width, height, rotation))
                    draw_contour(frame, rect, (0, 255, 0), "Green")

                cv2.imshow('Original', frame)

                for obj in detected_objects:
                    label, x, y, width, height, rotation = obj
                    print(f"{label}: Object Coordinates - x: {x}, y: {y}, width: {width}, height: {height}, rotation: {rotation}")

                    # Ekranda nesnenin sol, sağ veya ortada olup olmadığını kontrol et
                    if x < frame.shape[1] / 3:  # Eğer x koordinatı ekranın sol 1/3'ünden daha küçükse
                        print("Nesne sol tarafta.")
                    elif x > (2 * frame.shape[1]) / 3:  # Eğer x koordinatı ekranın sağ 1/3'ünden daha büyükse
                        print("Nesne sağ tarafta.")
                    else:
                        print("Nesne ortada.")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":
    color_detect()
