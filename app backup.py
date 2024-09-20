from flask import Flask, render_template, Response, send_from_directory
import cv2
import mediapipe as mp
import pyautogui
import time
import threading

app = Flask(__name__, static_folder='templates/assets')

# Initialize PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Define the box dimensions
box_left = 100
box_top = 150
box_right = 400
box_bottom = 250
box_width = box_right - box_left
box_height = box_bottom - box_top

# Parameters for smoothing
MOVEMENT_THRESHOLD = 5
MOVEMENT_BUFFER_SIZE = 5
INDEX_FINGER_OPEN_DURATION = 1
ALL_FINGERS_RAISED_DURATION = 3
GESTURE_DELAY = 2

class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

def smooth_cursor(prev_pos, curr_pos, buffer):
    buffer.append(curr_pos)
    if len(buffer) > MOVEMENT_BUFFER_SIZE:
        buffer.pop(0)
    avg_x = sum(x for x, _ in buffer) / len(buffer)
    avg_y = sum(y for _, y in buffer) / len(buffer)
    return avg_x, avg_y

def generate_frames():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = HandDetector(detectionCon=0.75)
    tipIds = [4, 8, 12, 16, 20]

    finger_states = [False] * 5
    finger_states_before = [False] * 5
    cursor_buffer = []

    index_finger_open_time = 0
    index_finger_last_opened = False

    right_mouse_button_down = False
    left_mouse_button_down = False

    all_fingers_raised_start_time = None
    keyboard_visible = False
    last_gesture_time = time.time()

    while True:
        success, img = cap.read()
        if not success:
            break

        img_for_annotations = img.copy()
        img_for_annotations = detector.findHands(img_for_annotations)
        lmList = detector.findPosition(img_for_annotations, draw=False)

        cv2.rectangle(img_for_annotations, (box_left, box_top), (box_right, box_bottom), (0, 0, 255), 2)

        if len(lmList) != 0:
            fingers = []
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            for i in range(5):
                if fingers[i]:
                    if not finger_states_before[i]:
                        finger_states[i] = True
                    else:
                        finger_states[i] = False
                else:
                    if finger_states_before[i]:
                        finger_states[i] = False
                    finger_states_before[i] = False

            finger_states_before = [state or raised for state, raised in zip(finger_states_before, fingers)]

            current_time = time.time()
            if fingers[1] and fingers[2] and not fingers[3] and not fingers[4] and not fingers[0]:
                pyautogui.scroll(50)
            elif fingers[1] and fingers[2] and fingers[3] and not fingers[4] and not fingers[0]:
                pyautogui.scroll(-50)

            if all(fingers[1:5]) and not fingers[0]:
                if current_time - last_gesture_time >= GESTURE_DELAY:
                    keyboard_visible = not keyboard_visible
                    pyautogui.hotkey('win', 'ctrl', 'o')  # Toggle keyboard visibility
                    last_gesture_time = current_time
            else:
                last_gesture_time = current_time

            if len(lmList) > 8:
                finger_x = lmList[8][1]
                finger_y = lmList[8][2]

                # Calculate screen coordinates based on finger position
                if finger_x < box_left:
                    screen_x = screen_width - 1
                    normalized_y = (finger_y - box_top) / box_height
                    screen_y = int(normalized_y * screen_height)
                elif finger_x > box_right:
                    screen_x = 0
                    normalized_y = (finger_y - box_top) / box_height
                    screen_y = int(normalized_y * screen_height)
                elif finger_y < box_top:
                    screen_y = 0
                    normalized_x = (finger_x - box_left) / box_width
                    screen_x = int((1 - normalized_x) * screen_width)
                elif finger_y > box_bottom:
                    screen_y = screen_height
                    normalized_x = (finger_x - box_left) / box_width
                    screen_x = int((1 - normalized_x) * screen_width)
                else:
                    normalized_x = (finger_x - box_left) / box_width
                    normalized_y = (finger_y - box_top) / box_height
                    normalized_x = min(max(normalized_x, 0), 1)
                    normalized_y = min(max(normalized_y, 0), 1)
                    screen_x = int(normalized_x * screen_width)
                    screen_y = int(normalized_y * screen_height)
                    screen_x = screen_width - screen_x

                # Clamp screen coordinates
                screen_x = max(0, min(screen_x, screen_width - 1))
                screen_y = max(0, min(screen_y, screen_height - 1))

                # Handle cursor movement
                if (fingers[1] and  fingers[0] and  fingers[2]  and not fingers[3] and not fingers[4]) or (fingers[1] and not fingers[0] and not fingers[2]  and not fingers[3] and not fingers[4]) :
                    if not index_finger_last_opened:
                        index_finger_open_time = time.time()
                        index_finger_last_opened = True
                    else:
                        elapsed_time = time.time() - index_finger_open_time
                        if elapsed_time >= INDEX_FINGER_OPEN_DURATION:
                            if cursor_buffer:
                                prev_x, prev_y = cursor_buffer[-1]
                            else:
                                prev_x, prev_y = screen_x, screen_y

                            avg_x, avg_y = smooth_cursor((prev_x, prev_y), (screen_x, screen_y), cursor_buffer)

                            if abs(avg_x - prev_x) > MOVEMENT_THRESHOLD or abs(avg_y - prev_y) > MOVEMENT_THRESHOLD:
                                try:
                                    pyautogui.moveTo(avg_x, avg_y)
                                except pyautogui.FailSafeException:
                                    avg_x = screen_width // 2
                                    avg_y = screen_height // 2
                                    pyautogui.moveTo(avg_x, avg_y)
                else:
                    index_finger_last_opened = False

                # Handle mouse button actions
                if fingers[4] and fingers[1] and not fingers[3] and not fingers[2] and not fingers[0]:
                    if not right_mouse_button_down:
                        pyautogui.mouseDown(button='right')
                        right_mouse_button_down = True
                else:
                    if right_mouse_button_down:
                        pyautogui.mouseUp(button='right')
                        right_mouse_button_down = False

                if fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
                        pyautogui.mouseDown(button='left')
                        pyautogui.mouseUp(button='left')


                if fingers[0] and fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                    if not left_mouse_button_down:
                        pyautogui.mouseDown(button='left')
                        left_mouse_button_down = True
                else:
                    if left_mouse_button_down:
                        pyautogui.mouseUp(button='left')
                        left_mouse_button_down = False

            if all(fingers):
                if all_fingers_raised_start_time is None:
                    all_fingers_raised_start_time = time.time()
                elif time.time() - all_fingers_raised_start_time >= ALL_FINGERS_RAISED_DURATION:
                    break  # Exit the loop if all fingers are raised for the specified duration
            else:
                all_fingers_raised_start_time = None

        # Prepare the frame for streaming
        img_for_annotations_flipped = cv2.flip(img_for_annotations, 1)
        img[0:img_for_annotations_flipped.shape[0], 0:img_for_annotations_flipped.shape[1]] = img_for_annotations_flipped
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera_capture')
def camera_capture():
    return render_template('camera_capture.html')
    
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('templates/assets', filename)

if __name__ == "__main__":
    app.run(debug=True)