import cv2
import numpy as np
import time
import math

cap = cv2.VideoCapture(0)

# TIGHTENED HSV BOUNDS: Raised from [90, 50, 50] to eliminate dull background blues
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])

VIBRANT_COLORS = [(0, 255, 0), (255, 0, 128), (255, 255, 0), (0, 215, 255), (255, 0, 255), (0, 165, 255)]
color_index = 0
active_color = VIBRANT_COLORS[color_index]

score = 0
points = []
canvas = None

# STREAMLINED POOL: Only the 4 highly reliable, distinct gestures
spells_pool = ["Circle", "Caret Down (V)", "Caret Up (^)", "Horizontal Line"]
target_spell = np.random.choice(spells_pool)
spell_status = "READY TO CAST"
status_color = (200, 200, 200)

no_pen_frames = 0
detection_threshold = 30
flash_timer = 0
flash_color = (0, 0, 0)


def classify_drawn_spell(raw_points):
    """Clean directional engine focused exclusively on Circle,
    Horizontal Line, Caret Down, and Caret Up."""
    if len(raw_points) < 6:
        return None

    xs = [p[0] for p in raw_points]
    ys = [p[1] for p in raw_points]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)

    width = max(1, xmax - xmin)
    height = max(1, ymax - ymin)
    aspect_ratio = width / height

    start_pt = raw_points[0]
    end_pt = raw_points[-1]
    start_end_dist = math.hypot(end_pt[0] - start_pt[0], end_pt[1] - start_pt[1])

    # 1. Circle Check (Prioritized closed-loop rule)
    if start_end_dist < max(width, height) * 0.55 and 0.55 < aspect_ratio < 1.65:
        return "Circle"

    # 2. Horizontal Line Check
    if aspect_ratio > 2.8 and (end_pt[0] - start_pt[0]) > width * 0.5:
        return "Horizontal Line"

    # Split the path to analyze directional movements
    mid_idx = len(raw_points) // 2
    fh_y_move = raw_points[mid_idx][1] - raw_points[0][1]
    sh_y_move = raw_points[-1][1] - raw_points[mid_idx][1]

    # 3. Caret Down / V-Shape (Down then Up)
    if fh_y_move > height * 0.35 and sh_y_move < -height * 0.35:
        return "Caret Down (V)"

    # 4. Caret Up / ^-Shape (Up then Down)
    if fh_y_move < -height * 0.35 and sh_y_move > height * 0.35:
        return "Caret Up (^)"

    return None


while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    if canvas is None: canvas = np.zeros_like(frame)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pen_detected = False
    force_submit = False

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

        if 2 < radius < 80 and area < 5000:
            pen_detected = True
            no_pen_frames = 0
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                points.append(center)
                cv2.circle(frame, center, 8, active_color, -1)
        else:
            if len(points) > 0: no_pen_frames += 1
    else:
        if len(points) > 0: no_pen_frames += 1

    for i in range(1, len(points)):
        if points[i - 1] is None or points[i] is None: continue
        cv2.line(canvas, points[i - 1], points[i], active_color, 6)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        force_submit = True

    if (no_pen_frames >= detection_threshold or force_submit) and len(points) > 0:
        valid_points = [p for p in points if p is not None]
        detected_spell = classify_drawn_spell(valid_points)

        if detected_spell == target_spell:
            score += 1
            spell_status = f"CAST SUCCESS: {detected_spell}!"
            status_color = (0, 255, 0)
            color_index = (color_index + 1) % len(VIBRANT_COLORS)
            active_color = VIBRANT_COLORS[color_index]
            target_spell = np.random.choice([s for s in spells_pool if s != target_spell])
            flash_timer, flash_color = 6, (0, 255, 0)
        else:
            spell_status = f"CAST FAILED (Saw {detected_spell})" if detected_spell else "CAST FAILED: Shape Unclear"
            status_color = (0, 0, 255)
            flash_timer, flash_color = 6, (0, 0, 150)

        points = []
        canvas = np.zeros_like(frame)
        no_pen_frames = 0

    output_display = cv2.addWeighted(frame, 1, canvas, 1, 0)
    if flash_timer > 0:
        output_display = cv2.addWeighted(output_display, 0.7, np.full_like(output_display, flash_color), 0.3, 0)
        flash_timer -= 1

    # HUD Graphics
    cv2.rectangle(output_display, (10, 10), (340, 140), (20, 20, 20), -1)
    cv2.rectangle(output_display, (10, 10), (340, 140), active_color, 2)
    cv2.putText(output_display, f"TARGET: {target_spell}", (25, 45), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
    cv2.putText(output_display, f"SCORE: {score}", (25, 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, active_color, 2)
    cv2.putText(output_display, f"STATUS: {spell_status}", (25, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)

    if len(points) > 0 and pen_detected:
        cv2.putText(output_display, "Drawing Magic...", (points[-1][0] - 50, points[-1][1] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, active_color, 1)

    cv2.putText(output_display, "Controls: Draw | [SPACE] Cast Now | [C] Clear | [Q] Exit", (20, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.imshow("Momo's Magical Spell Trainer", output_display)

    if key == ord('q'):
        break
    elif key == ord('c'):
        points, canvas = [], np.zeros_like(frame)
        spell_status, status_color = "CANVAS CLEARED", (200, 200, 200)

cap.release()
cv2.destroyAllWindows()