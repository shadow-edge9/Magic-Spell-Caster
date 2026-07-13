# Magic Spell Caster
CEAM TASK : Make a project using OpenCV.

## Project Overview
Inspired by the Google Halloween Doodles featuring Momo the Magic Cat, I built a project using OpenCV that turns your drawings into a spell casting magical experience.

<img width="1003" height="492" alt="Screenshot 2026-07-13 at 5 22 54 PM" src="https://github.com/user-attachments/assets/8cd24b5c-8e44-43b0-8666-b3f53135cd4f" />
<img width="1003" height="492" alt="Screenshot 2026-07-13 at 5 23 35 PM" src="https://github.com/user-attachments/assets/4e9410d7-4fc0-4177-bf9c-7d557d8906c5" />
<img width="1003" height="492" alt="Screenshot 2026-07-13 at 5 24 21 PM" src="https://github.com/user-attachments/assets/79264f2e-f6e9-4d51-bfe3-1749c2e27769" />


## Gameplay
* You need a physical "wand", and it must be blue, like a blue pen.
* There are four "spells" you can "cast" (draw) :
  - A Horizontal Line
  - An upward caret (^)
  - A Downward caret (V)
  - A Circle
* Use your "wand" to "cast" the "spell". If it matches you get a point!
* If your drawing isn't neat and you want to clear the screen, press 'C' on your keyboard.
* To submit the drawing, press spacebar.
* To exit press 'Q' on your keybaord.

> NOTE: The tracking works best if your background doesn't have anything blue. A plain background works best.

## Technical Documentation

### STEP 1: THE MASK LAYER
Tested whether my camera was working. Confirmed it was. Then I set up the range of hues to detect for blue. Instead of going for standard BGR, I went for HSV (Hue, Saturation and Value). This is because standard BGR will not suffice in different lighting conditions and operates on fixed values, whereas it actually depends on the lighting. HSV handles that perfectly because it looks for a range and not a specific value.

<img width="800" height="674" alt="ScreenRecording2026-07-13at4 18 24PM-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/86daa882-5ad6-463d-b6f2-a5bb169f26c9" />

### STEP 2: DRAWING
Made an empty list that collects my coordinates and appends to it with every stroke. pressing C on your keybaord clears the artwork in green. Your object, in this case a blue pen, can now be used a stylus to draw doodles in the air. 

### STEP 3: THE GAME LOGIC, DETECTION & USER INTERFACE
The math calculates the distances between the start and end points. 
* For a circle it checks if the start and end points are very close and if bounding box is nearly a square.
* For a horizontal line, if overall direction moves from left to right and bounding box is wider than taller (i.e width>height).
* For the carets, it checks the movement of my hand, whether it went up-then-down or down-then-up.

In the upper left corner is your status board. It tells you your score, the spell you have to cast and if you make a mistake, the system tells you what shape it detected.

## OpenCV Functions Used

| Function | What it does (Plain English) | How I used it in my project |
| :--- | :--- | :--- |
| **`cv2.VideoCapture()`** | Turns on the camera. | Opens default webcam (`0`) to capture live video frames. |
| **`cv2.flip()`** | Flips the video feed. | Mirrors the camera feed horizontally so moving your hand left moves the drawing left. |
| **`cv2.GaussianBlur()`** | Blurs the image. | Smooths out pixel noise and grainy background details so tracking is cleaner. |
| **`cv2.cvtColor()`** | Changes color modes. | Converts the video from normal BGR color to HSV mode, making it easier to track color ranges. |
| **`cv2.inRange()`** | Filters for a specific color. | Creates a black-and-white mask where only the blue pen shows up as white. |
| **`cv2.erode()`** | Shrinks white spots. | Cleans up the mask by erasing tiny, accidental blue dots from the background. |
| **`cv2.dilate()`** | Expands white spots. | Makes the remaining white spots bigger so the computer clearly sees the pen tip. |
| **`cv2.findContours()`** | Finds shapes/outlines. | Traces the outlines of the white shapes left on the black-and-white mask. |
| **`cv2.contourArea()`** | Measures the size of a shape. | Checks the size of outlines so the code ignores tiny reflections or huge blue shirts. |
| **`cv2.minEnclosingCircle()`** | Fits a circle around a shape. | Finds the exact center point and width of the pen tip to lock onto it. |
| **`cv2.moments()`** | Finds the center of gravity (COM) | Calculates the exact mathematical center coordinate of the tracked pen. |
| **`cv2.circle()`** | Draws a circle. | Draws a small tracking dot on the screen exactly where the pen is located. |
| **`cv2.line()`** | Draws a straight line. | Connects saved tracking coordinates together to draw the magical ink trail. |
| **`cv2.addWeighted()`** | Blends two images together. | Overlays drawing canvas on top of the live webcam feed with transparency. |
| **`cv2.rectangle()`** | Draws a box. | Creates the dark boxes and neon borders used to build the game's score display UI. |
| **`cv2.putText()`** | Writes text on the screen. | Displays the target spells, player score, and current system messages on the screen. |
| **`cv2.imshow()`** | Opens a display window. | Creates the actual desktop game window so you can watch the program run. |
| **`cv2.waitKey()`** | Waits for keyboard buttons. | Keeps the game running smoothly and checks if I press `SPACE` to cast, `C` to clear, or `Q` to quit. |
| **`cap.release()`** | Turns off the camera. | Safely disconnects and shuts down the webcam when the program closes. |
| **`cv2.destroyAllWindows()`** | Closes windows. | Shuts down all open game windows smoothly when exiting the script. |

## Prerequisites
This project was built with Python 3
Modules used are:
* `cv2`
* `numpy`
* `time`
* `math`

## How to Run

To clone this repository:
```bash
git clone https://github.com/shadow-edge9/Magic-Spell-Caster
cd Magic-Spell-Caster
```

To run:
```bash
python3 spell_caster.py
```




