import cv2
import mediapipe as mp
import numpy as np
import random
import time
import csv
from Data_Sorting import sort_scores

def save_score(game_points, mode, difficulty):
    with open('game_scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([game_points, mode, difficulty, time.strftime('%Y-%m-%d %H:%M:%S')])

def mode_1(difficulty):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    #difficulty
    if difficulty == "Easy":
        moving_time = 5
        add_point = 15
    elif difficulty == "Normal":
        moving_time = 3
        add_point = 20
    elif difficulty == "Hard":
        moving_time = 1.5
        add_point = 30

    # Video Capture Size
    cap_width = 1280
    cap_height = 960

    # Ball variables
    circle_radius = 30
    circle_color = [255, 255, 0]
    circle_center = [random.randint(100, 1180), random.randint(100, 600)]

    index_tip = None
    thumb_tip = None

    game_points = 0

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        countdown_seconds = 30
        start_time = time.time()

        last_move_time = time.time()

        # 在程式開始前新增一個變數
        ball_appeared_time = None

        while cap.isOpened():
            success, image = cap.read()
            current_time = time.time()

            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            cv2.circle(image, circle_center, circle_radius, circle_color, -1)

            if index_tip and thumb_tip:
                index_tip_x = int(index_tip.x * image.shape[1])
                index_tip_y = int(index_tip.y * image.shape[0])
                thumb_tip_x = int(thumb_tip.x * image.shape[1])
                thumb_tip_y = int(thumb_tip.y * image.shape[0])

                finger_distance = np.sqrt((index_tip_x - thumb_tip_x) ** 2 + (index_tip_y - thumb_tip_y) ** 2)

                if finger_distance < 40:
                    if ball_appeared_time is None:
                        ball_appeared_time = current_time  # 在手指合併時開始計時
                    
                        point_center = [(index_tip_x + thumb_tip_x) // 2, (index_tip_y + thumb_tip_y) // 2]
                        point_radius = 8
                        point_color = [0, 0, 255]
                        cv2.circle(image, point_center, point_radius, point_color, -1)
                        ball_distance = np.sqrt((circle_center[0] - point_center[0]) ** 2 + (circle_center[1] - point_center[1]) ** 2)
                        if ball_distance < circle_radius:
                            game_points += add_point
                            old_center = circle_center
                            while old_center == circle_center:
                                circle_center = [random.randint(100, 1180), random.randint(100, 600)]
                            last_move_time = current_time
                else:
                    ball_appeared_time = None  # 如果手指分開，重置計時器

                if current_time - last_move_time > moving_time:
                    old_center = circle_center
                    while old_center == circle_center:
                        circle_center = [random.randint(100, 1180), random.randint(100, 600)]
                    last_move_time = current_time

            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, countdown_seconds - elapsed_time)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, f"Time: {remaining_time}s", (10, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"Game Point: {game_points} points", (900, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Random Shooting', image)

            if cv2.waitKey(5) & 0xFF == 27 or remaining_time == 0: break
        cap.release()
    save_score(game_points, "Random Shooting", difficulty)
    sort_scores('game_scores.csv')
    cv2.destroyAllWindows()
    return game_points