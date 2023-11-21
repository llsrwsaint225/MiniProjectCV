import cv2
import mediapipe as mp

# Function to detect key presses on the virtual keyboard
def detect_key_press(key, typed_text):
    global keyboard_layout

    if key in keyboard_layout:
        if key == 'Backspace' and len(typed_text) > 0:
            typed_text = typed_text[:-1]  # Remove the last character
        elif key != 'Backspace' and key != 'Space':
            typed_text += key
        print(f"Typed: {typed_text}")

# Function to get the key based on coordinates
def get_key(x, y, keyboard_layout):
    for key, (key_x, key_y, key_w, key_h) in keyboard_layout.items():
        if key_x <= x <= key_x + key_w and key_y <= y <= key_y + key_h:
            return key
    return None

# Function to process webcam frames and detect the keyboard and hand
def process_webcam():
    global typed_text, keyboard_layout

    fingertip_pressed = False
    cooldown_frames = 30  # Set a cooldown period (adjust as needed)
    current_cooldown = 0
    # Set up hand tracking
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame from the webcam
        ret, frame = cap.read()

        # Resize the frame for better processing speed
        frame = cv2.resize(frame, (1280, 720))

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with hand tracking
        results = hands.process(frame_rgb)

        # Draw landmarks if hand is detected
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                for finger_id, point in enumerate(landmarks.landmark):
                    x, y = int(point.x * frame.shape[1]), int(point.y * frame.shape[0])

                    # Check if fingertip is close to any virtual key
                    key_pressed = get_key(x, y, keyboard_layout)

                    # If a key is pressed and not in cooldown, update the typed text
                    if key_pressed and not fingertip_pressed and current_cooldown == 0:
                        detect_key_press(key_pressed, typed_text)
                        fingertip_pressed = True
                        current_cooldown = cooldown_frames
                        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Highlight fingertip

        # Update cooldown
        if current_cooldown > 0:
            current_cooldown -= 1

        # Reset fingertip_pressed if no fingertips are detected
        if not results.multi_hand_landmarks:
            fingertip_pressed = False

        # Draw the virtual keyboard
        for key, (x, y, w, h) in keyboard_layout.items():
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Check for key presses
        key = cv2.waitKey(1)
        if key == 27:  # Esc key
            break
        elif key != -1 and key != 255:  # Check if any key is pressed
            key_char = chr(key).upper()  # Get the character representation of the key
            detect_key_press(key_char, typed_text)

        # Display the frame
        cv2.imshow('Webcam', frame)

    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    typed_text = ""

    # Define the virtual keyboard layout
    keyboard_layout = {
        'Backspace': (888, 9, 120, 50),

        'Q': (111, 76, 50, 50),
        'W': (179, 76, 50, 50),
        'E': (246, 76, 50, 50),
        'R': (314, 76, 50, 50),
        'T': (382, 76, 50, 50),
        'Y': (449, 76, 50, 50),
        'U': (517, 76, 50, 50),
        'I': (585, 76, 50, 50),
        'O': (652, 76, 50, 50),
        'P': (720, 76, 50, 50),
        '[': (787, 76, 50, 50),
        ']': (855, 76, 50, 50),
        '\\': (921, 76, 89, 50),

        'A': (128, 143, 50, 50),
        'S': (196, 143, 50, 50),
        'D': (264, 143, 50, 50),
        'F': (331, 143, 50, 50),
        'G': (399, 143, 50, 50),
        'H': (466, 143, 50, 50),
        'J': (534, 143, 50, 50),
        'K': (602, 143, 50, 50),
        'L': (669, 143, 50, 50),
        ';': (737, 143, 50, 50),
        "'": (805, 143, 50, 50),

        'Z': (162, 211, 50, 50),
        'X': (229, 211, 50, 50),
        'C': (297, 211, 50, 50),
        'V': (365, 211, 50, 50),
        'B': (432, 211, 50, 50),
        'N': (500, 211, 50, 50),
        'M': (568, 211, 50, 50),
        ',': (635, 211, 50, 50),
        '.': (703, 211, 50, 50),
        '/': (770, 211, 50, 50),

        'Space': (260, 278, 411, 50),
    }

    # Process webcam frames
    process_webcam()