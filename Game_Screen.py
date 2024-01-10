import pygame
import sys
import time
import csv
from Random_Shotting import mode_1
from Random_and_Decreasing import mode_2
from Mulitple_Shooting import mode_3
from Data_Sorting import sort_scores


#進入遊戲前的倒數計時
def count_time():
    # 開始倒數計時
    countdown_seconds = 3
    while time.time() - start_countdown_time < countdown_seconds + 1:
        # 顯示倒數計時
        screen.blit(background_image, (0, 0))
        text = font.render(
                            f"Starting in {countdown_seconds - int(time.time() - start_countdown_time)} seconds",
                            True, white)
        text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(text, text_rect)
        pygame.time.delay(1000)
        pygame.display.flip()
        

# 檢查 CSV 檔案是否為空
def is_csv_empty(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                return False  # 有資料，不是空的
            return True  # 沒有資料，是空的  
    except IndexError:
        return True  # 檔案不存在，視為空的
    
    except Exception as e:
        #print(f"Error reading CSV: {e}")
        return True  # 讀取時發生錯誤，視為空的

# 讀取 CSV 檔案的函式
def read_csv(filename):
    if is_csv_empty(filename):
        return []  # 如果是空的，回傳空列表
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data[1:]


# 初始化 Pygame
pygame.init()

# 初始化 Pygame mixer
pygame.mixer.init()

# 載入按鈕點擊音效
button_click_sound = pygame.mixer.Sound("button_click_sound.mp3")

# 設定音量（0.0 到 1.0 之間）
button_click_sound.set_volume(1.0)

# 載入背景音樂
background_music = pygame.mixer.Sound("background_music.mp3")

# 設定音量（0.0 到 1.0 之間）
background_music.set_volume(0.3)

# 設定視窗大小
window_size = (1024, 576)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Shooting Game")

# 設定顏色
white = (255, 255, 255)
black = (0, 0, 0)
button_color = (50, 50, 50)
hover_color = (100, 100, 100)
click_color = (150, 150, 150)
button_text_color = white

# 設定字體
font = pygame.font.Font(None, 36)

# 設定按鈕
button_width = 140
button_height = 60

mode_button_rects = [
    pygame.Rect(400, 200, button_width, button_height),
    pygame.Rect(400, 280, button_width, button_height),
    pygame.Rect(400, 360, button_width, button_height)
]

difficulty_button_rects = [
    pygame.Rect(400, 200, button_width, button_height),  # Easy
    pygame.Rect(400, 280, button_width, button_height),  # Normal
    pygame.Rect(400, 360, button_width, button_height)   # Hard
]

back_button_rect = pygame.Rect(50, 520, button_width, 30)
restart_button_rect = pygame.Rect(window_size[0] // 2, 280, button_width, 30)

button_texts = ["Mode 1", "Mode 2", "Mode 3", "Easy", "Normal", "Hard", "Back", "restart"]

# 設定初始遊戲模式
current_mode = None
current_difficulty = None
show_difficulty_screen = False
show_end_screen = False
start_countdown_time = None

# 背景圖片
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, window_size)

game_scores_texts = []
current_score = 0
background_music.play(-1)  # -1表示無限循環播放，你也可以指定播放次數


# 遊戲迴圈
running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_difficulty_screen:
                # 檢查回上一頁按鈕點擊
                if back_button_rect.collidepoint(event.pos):
                    button_click_sound.play()  # 按下模式按鈕時的聲音
                    show_difficulty_screen = False
                # 檢查難易度按鈕點擊
                for i, rect in enumerate(difficulty_button_rects):
                    if rect.collidepoint(event.pos):
                        button_click_sound.play()  # 按下模式按鈕時的聲音
                        current_difficulty = button_texts[i + 3]  # 對應到 "Easy", "Normal", "Hard"

                        # 顯示回上一頁按鈕
                        pygame.draw.rect(screen, black, back_button_rect, 2)
                        text_back = font.render(button_texts[6], True, black)
                        screen.blit(text_back, (back_button_rect.centerx - text_back.get_width() // 2,
                                                back_button_rect.centery - text_back.get_height() // 2))

                        # 在這裡可以根據 current_mode 和 current_difficulty 開始相應的遊戲或執行其他邏輯
                        print(f"Mode {current_mode + 1}, Difficulty {current_difficulty}")
                        show_difficulty_screen = False

                        # 進入遊戲模式
                        if current_mode == 0:
                            #開始進入倒數計時
                            count_time()
                            current_score=mode_1(current_difficulty)
                            show_end_screen = True
                            show_difficulty_screen = False

                        elif current_mode == 1:
                            #開始進入倒數計時
                            count_time()
                            current_score=mode_2(current_difficulty)
                            show_end_screen = True
                            show_difficulty_screen = False
                                
                        elif current_mode == 2:
                           #開始進入倒數計時
                           count_time()
                           current_score=mode_3(current_difficulty)
                           show_end_screen = True
                           show_difficulty_screen = False
            elif show_end_screen:
                #按restart後跳回主畫面
                if restart_button_rect.collidepoint(event.pos):
                    # 重設相關變數到初始狀態
                    current_mode = None
                    current_difficulty = None
                    show_difficulty_screen = False
                    show_end_screen = False
                    start_countdown_time = None
            else:
                # 檢查模式按鈕點擊
                for i, rect in enumerate(mode_button_rects):
                    if rect.collidepoint(event.pos):
                        button_click_sound.play()  # 按下模式按鈕時的聲音
                        current_mode = i
                        time.sleep(0.2)
                        show_difficulty_screen = True
                        start_countdown_time = time.time()
                

                




    # 繪製背景
    screen.blit(background_image, (0, 0))

    # 繪製 CSV 檔案中的資料
    

    # 繪製按鈕
    if show_difficulty_screen:
        for i, rect in enumerate(difficulty_button_rects):
            pygame.draw.rect(screen, button_color, rect)
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, hover_color, rect)
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, click_color, rect)
            text = font.render(button_texts[i + 3], True, button_text_color)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        # 繪製回上一頁按鈕
        pygame.draw.rect(screen, button_color, back_button_rect)
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, hover_color, back_button_rect)
        if back_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, click_color, back_button_rect)
        text_back = font.render(button_texts[6], True, button_text_color)
        screen.blit(text_back, (back_button_rect.centerx - text_back.get_width() // 2,
                                back_button_rect.centery - text_back.get_height() // 2))
    elif show_end_screen:
        high_scores_data = read_csv('game_scores.csv')
        # 找到玩家的分數在排行榜中的位置
        player_rank = -1
        for i, row in enumerate(high_scores_data):
            if int(row[0]) <= current_score:
                player_rank = i + 1
                break
        if player_rank <= 10:
            rank_text = font.render(f"Your Rank: {player_rank} - Score: {current_score}", True, white)
            rank_rect = rank_text.get_rect(center=(window_size[0] // 2, 360))
            screen.blit(rank_text, rank_rect)
        else:
            rank_text = font.render(f"Your Score: {current_score} - Rank: >10", True, white)
            rank_rect = rank_text.get_rect(center=(window_size[0] // 2, 360))
            screen.blit(rank_text, rank_rect)
        pygame.draw.rect(screen, button_color, restart_button_rect)
        if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, hover_color, restart_button_rect)
        if restart_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, click_color, restart_button_rect)
        text_back = font.render(button_texts[-1], True, button_text_color)
        screen.blit(text_back, (restart_button_rect.centerx - text_back.get_width() // 2,
                                restart_button_rect.centery - text_back.get_height() // 2))
    else:
        # 檢查 CSV 檔案是否為空
        if not is_csv_empty('game_scores.csv'):

            # 呼叫讀取 CSV 檔案的函式
            sort_scores('game_scores.csv')
            high_scores_data = read_csv('game_scores.csv')

            # 只取前 10 列資料
            if len(high_scores_data) > 10:
                high_scores_data = high_scores_data[:10]

            # 顯示 CSV 檔案中的資料
            small_font = pygame.font.Font(None, 28)  # 使用較小的字型
            
            for i, row in enumerate(high_scores_data):
                text = small_font.render(f"Rank: {i + 1} - Score: {row[0]}", True, white)
                text_rect = text.get_rect(topright=(window_size[0] - 10, (i + 1) * 30))
                game_scores_texts.append((text, text_rect))
                
        for text, text_rect in game_scores_texts:
            screen.blit(text, text_rect)
        for i, rect in enumerate(mode_button_rects):
            pygame.draw.rect(screen, button_color, rect)
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, hover_color, rect)
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, click_color, rect)
            text = font.render(button_texts[i], True, button_text_color)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
        
    # 更新視窗
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()





