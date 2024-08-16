import random
import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

GESTURES = ["Rock", "Paper", "Scissors"]

def get_computer_choice():
    return random.choice(GESTURES)

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a draw!"
    elif (player_choice == "Rock" and computer_choice == "Scissors") or \
            (player_choice == "Paper" and computer_choice == "Rock") or \
            (player_choice == "Scissors" and computer_choice == "Paper"):
        return "You win!"
    else:
        return "Computer wins!"

def classify_gesture(landmarks):
    thumb_is_open = landmarks[4].x < landmarks[3].x
    index_is_open = landmarks[8].y < landmarks[6].y
    middle_is_open = landmarks[12].y < landmarks[10].y

    if not thumb_is_open and not index_is_open and not middle_is_open:
        return "Rock"
    elif thumb_is_open and index_is_open and middle_is_open:
        return "Paper"
    elif not thumb_is_open and index_is_open and middle_is_open:
        return "Scissors"
    return None

def draw_info(frame, text, position, color=(255, 255, 255), scale=1, thickness=2):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)

def countdown_timer(frame, duration, start_message="Starting in"):
    start_time = time.time()
    while time.time() - start_time < duration:
        temp_frame = frame.copy()
        seconds_left = int(duration - (time.time() - start_time))
        draw_info(temp_frame, f"{start_message} {seconds_left}...", (50, 200), color=(0, 255, 255), scale=2,
                  thickness=3)
        cv2.imshow("Rock Paper Scissors", temp_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
    ret, frame = cap.read()
    if ret:
        countdown_timer(frame, 5)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        player_choice = None

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )
                player_choice = classify_gesture(hand_landmarks.landmark)

        if player_choice:
            draw_info(frame, f"Your choice: {player_choice}", (10, 50), color=(0, 255, 0), scale=1.2, thickness=2)

            computer_choice = get_computer_choice()
            winner = determine_winner(player_choice, computer_choice)

            draw_info(frame, f"Computer: {computer_choice}", (10, 100), color=(255, 0, 0), scale=1.2, thickness=2)
            draw_info(frame, f"Result: {winner}", (10, 150), color=(0, 0, 255), scale=1.4, thickness=3)

            start_time = time.time()
            while time.time() - start_time < 2:
                cv2.imshow("Rock Paper Scissors", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            countdown_timer(frame, 3, start_message="Next round in")
            continue

        cv2.imshow("Rock Paper Scissors", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nGame interrupted...")

finally:
    cap.release()
    cv2.destroyAllWindows()