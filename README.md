# Biometric / Facial Recognition Obfuscation

A small real-time webcam project that applies a subtle distortion to facial features to make biometric tracking and facial recognition less reliable.

It uses **OpenCV** for the webcam/video processing and **MediaPipe Face Mesh** to find facial landmarks.

## How it works

The basic idea is pretty simple:

1. The program opens the default webcam and captures live video.
2. MediaPipe Face Mesh detects around **468 facial landmarks** on each frame.
3. Each landmark is given a small movement using sine and cosine functions.
4. A small patch around the original landmark is copied to the new, slightly shifted position.
5. Since this happens across the face and changes over time, it creates a moving/shimmering distortion around features such as the eyes, nose, mouth, and jaw.
6. The processed video is shown in a window called **"Biometric Obfuscation Output"**.
7. When the program stops, it calculates and prints the variance of the landmark displacement as a basic measure of how much the face was being distorted.

The goal is to keep the video recognizable to a person while making the facial data less consistent for automated recognition.

## Requirements

You'll need:

* Python 3.8+
* OpenCV
* MediaPipe
* NumPy
* A working webcam

Install everything with:

```bash
pip install opencv-python mediapipe numpy
```

## Running the project

Run:

```bash
python obfuscate.py
```

The program will open your default webcam automatically.

* The session runs for a maximum of **90 seconds**.
* Press **ESC** to stop it early.
* You can also close the webcam window using the **X** button.
* Once the program exits, the displacement variance is printed in the terminal.
* If no face was detected during the session, it will simply print **"No face detected."**

## Changing the distortion

A few values in the main loop control how strong the effect looks:

| Parameter  | What it controls                      | Default |
| ---------- | ------------------------------------- | ------: |
| `strength` | Maximum amount a landmark can move    |    `15` |
| `size`     | Size of the pixel patch being moved   |     `2` |
| `angle`    | Time-based movement of the distortion | Dynamic |

If you increase `strength` or `size`, the distortion becomes more noticeable, but the video can start looking messy.

Lower values give a cleaner and more subtle effect.

## What the metric means

The program keeps track of how far each landmark is moved.

The displacement for a landmark is represented as:

```text
dx² + dy²
```

At the end of the session, the program calculates the **variance** of these displacement values.

This isn't a measure of how "secure" the obfuscation is. It's just a simple way to see how much the landmark movements varied during a run.

## Limitations

This is mainly a **proof-of-concept / visual demo**, not a guaranteed way to defeat facial recognition.

How effective the distortion is can depend on things like:

* The facial recognition model being used
* Lighting conditions
* Camera quality
* Distance from the camera
* How well MediaPipe detects the face
* The `strength` and `size` values

The distortion is also applied independently on each frame, so the exact output can look slightly different between runs.

For the best results, use a reasonably well-lit environment and keep your face roughly facing the camera.

## Project structure

```text
.
└── obfuscate.py
```

`obfuscate.py` contains the entire implementation, including webcam capture, face landmark detection, distortion, live preview, and the displacement metric.

## Note

This project is intended for **learning and experimentation with computer vision and biometric privacy**. It demonstrates how manipulating facial landmarks can change the visual representation of a face, but it shouldn't be treated as a reliable privacy or security solution.
