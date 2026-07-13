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





