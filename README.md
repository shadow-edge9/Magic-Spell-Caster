# Magic Spell Caster
CEAM TASK : Make a project using OpenCV.

## Project Overview
Inspired by the Google Halloween Doodles featuring Momo the Magic Cat, I built a project using OpenCV that turns your drawings into a spell casting magical experience.

## Gameplay
* You need a physical "wand", and it must be blue, like a blue pen.
* There are four "spells" you can "cast" (draw) :
  - A Horizontal Line
  - An upward caret (^)
  - A Downward caret (V)
  - A Circle
* Use your "wand" to "cast" the "spell". If it matches you get a point!

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

## Functions Used

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




