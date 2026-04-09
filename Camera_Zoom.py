import cv2

cap = cv2.VideoCapture(0)

zoom = 2  # zoom level

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Calculate crop area based on zoom
    new_w = int(w / zoom)
    new_h = int(h / zoom)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2

    cropped = frame[y1:y1+new_h, x1:x1+new_w]

    # Resize back to original size
    zoomed_frame = cv2.resize(cropped, (w, h))

    cv2.imshow("Zoom Camera", zoomed_frame)

    key = cv2.waitKey(1)

    # Press 'i' to zoom in
    if key == ord('i'):
        zoom += 0.1

    # Press 'o' to zoom out
    elif key == ord('o'):
        zoom = max(1.0, zoom - 0.1)

    # Press 'q' to quit
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()