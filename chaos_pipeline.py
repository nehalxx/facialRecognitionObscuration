import cv2
import mediapipe as mp
import numpy as np
import time

# -------------------------
# MediaPipe Setup
# -------------------------
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()

# -------------------------
# Webcam Setup
# -------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

# Metric tracking
displacements = []
start_time = time.time()

# -------------------------
# Main Loop
# -------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for lm in face_landmarks.landmark:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])

                # --- Adjusted chaos parameters ---
                strength = 15
                angle = time.time() * 10
                size = 2

                dx = int(strength * np.sin(angle + x * 0.01))
                dy = int(strength * np.cos(angle + y * 0.01))

                new_x = np.clip(x + dx, 0, frame.shape[1] - 1)
                new_y = np.clip(y + dy, 0, frame.shape[0] - 1)

                y1 = max(0, y - size)
                y2 = min(frame.shape[0], y + size)
                x1 = max(0, x - size)
                x2 = min(frame.shape[1], x + size)

                ny1 = max(0, new_y - size)
                ny2 = min(frame.shape[0], new_y + size)
                nx1 = max(0, new_x - size)
                nx2 = min(frame.shape[1], new_x + size)

                # Fix: match shapes before assigning
                src = frame[y1:y2, x1:x2]

                dst_h = ny2 - ny1
                dst_w = nx2 - nx1
                src_h = y2 - y1
                src_w = x2 - x1

                # Only copy if shapes match
                h = min(src_h, dst_h)
                w = min(src_w, dst_w)

                if h > 0 and w > 0:
                    frame[ny1:ny1+h, nx1:nx1+w] = frame[y1:y1+h, x1:x1+w]

                displacements.append(dx * dx + dy * dy)

    # Display text
    cv2.putText(
        frame,
        "Biometric Obfuscation Active",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow("Biometric Obfuscation Output", frame)

    # Stop after 90 seconds
    if time.time() - start_time > 90:
        break

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # Close using the red X
    if cv2.getWindowProperty(
        "Biometric Obfuscation Output",
        cv2.WND_PROP_VISIBLE
    ) < 1:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# -------------------------
# Print Metric
# -------------------------
if displacements:
    print("Displacement Variance:", np.var(displacements))
else:
    print("No face detected.")