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

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)



def mode_3(difficulty):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    #difficulty
    if difficulty == "Easy":
        moving_time = 5
        add_point = 10
    elif difficulty == "Normal":
        moving_time = 3
        add_point = 15
    elif difficulty == "Hard":
        moving_time = 1.5
        add_point = 25

    # Video Capture Size
    cap_width = 1280
    cap_height = 960

    # Ball variables
    circle_radius = 30
    circle_color = [255, 255, 0]
    # six random ball center
    circle_center = []
    while len(circle_center) < 6:
        new_point = [random.randint(150, 1130), random.randint(150, 550)]
        valid = True
        for point in circle_center:
            if distance(new_point, point) < 65:
                valid = False
                break
        if valid:
            circle_center.append(new_point)


    index_tip = None
    thumb_tip = None
    point_center =[0,0]

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

            for i in range(6):
                cv2.circle(image, circle_center[i], circle_radius, circle_color, -1)

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

                        for i in range(6):
                            ball_distance = distance(circle_center[i], point_center)
                            if ball_distance < circle_radius:
                                game_points += add_point
                                while True:
                                    new_center = [random.randint(150, 1130), random.randint(150, 550)]
                                    valid = True
                                    for j in range(6):
                                        if i != j and distance(new_center, circle_center[j]) < 65:
                                            valid = False
                                            break
                                    if valid:
                                        circle_center[i] = new_center
                                        break

                else:
                    ball_appeared_time = None  # 如果手指分開，重置計時器

                if current_time - last_move_time > moving_time:
                    index = random.randint(0, 5)
                    while True:
                        new_center = [random.randint(150, 1130), random.randint(150, 550)]
                        valid = True
                        for i in range(6):
                            if i != index and distance(new_center, circle_center[i]) < 65:
                                valid = False
                                break
                        if valid:
                            circle_center[index] = new_center
                            break
                    last_move_time = current_time

            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, countdown_seconds - elapsed_time)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, f"Time: {remaining_time}s", (10, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"Game Point: {game_points} points", (900, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Multiple Shooting', image)

            if cv2.waitKey(5) & 0xFF == 27 or remaining_time == 0:
                break
        cap.release()
    save_score(game_points, "Multiple Shooting", difficulty)
    sort_scores('game_scores.csv')
    cv2.destroyAllWindows()
    return game_points