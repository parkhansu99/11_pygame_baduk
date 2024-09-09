import pygame
import sys
import random

##################################
# 1. 기본 초기화

pygame.init()  # Pygame 초기화

width, height = 600, 600  # 화면 크기 설정
line_color = (0, 0, 0)  # 선 색상 설정
background_color = (255, 255, 255)  # 배경 색상 설정
line_width = 2  # 선 두께 설정
circle_radius = 15  # 원의 반지름 설정
black_circle_color = (0, 0, 0)  # 검정색 돌 색상 설정
white_circle_color = (255, 255, 255)  # 흰색 돌 색상 설정
circle_border_color = (0, 0, 0)  # 돌 테두리 색상 설정

screen = pygame.display.set_mode((width, height))  # 화면 모드 설정
pygame.display.set_caption("19x19 Go Board")  # 윈도우 제목 설정

##################################
# 2. 바둑판 및 돌 관련 함수

def draw_board():
    screen.fill(background_color)  # 배경 색상으로 화면을 채움
    cell_size = width // 19  # 셀 크기 계산
    for i in range(19):
        pygame.draw.line(screen, line_color, (0, i * cell_size), (width, i * cell_size), line_width)  # 수평선 그리기
        pygame.draw.line(screen, line_color, (i * cell_size, 0), (i * cell_size, height), line_width)  # 수직선 그리기
    
    for (x, y, color) in stones:
        pygame.draw.circle(screen, color, (x, y), circle_radius)  # 돌 그리기
        pygame.draw.circle(screen, circle_border_color, (x, y), circle_radius, line_width)  # 돌 테두리 그리기
    
    pygame.display.flip()  # 화면 업데이트

def get_grid_position(pos):
    cell_size = width // 19  # 셀 크기 계산
    x = ((pos[0] + cell_size // 2) // cell_size) * cell_size  # X 좌표 계산
    y = ((pos[1] + cell_size // 2) // cell_size) * cell_size  # Y 좌표 계산
    return (x, y)  # 계산된 그리드 좌표 반환

stones = []  # 돌 목록 초기화

def is_occupied(pos):
    for (x, y, _) in stones:
        if x == pos[0] and y == pos[1]:  # 위치가 점유되었는지 확인
            return True
    return False  # 점유되지 않았으면 False 반환

def check_winner(x, y, color):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]  # 방향 정의
    for dx, dy in directions:
        count = 1  # 현재 돌 포함
        nx, ny = x, y
        while True:
            nx += dx * (width // 19)  # X 좌표 이동
            ny += dy * (height // 19)  # Y 좌표 이동
            if (nx, ny, color) in stones:
                count += 1  # 돌이 일치하면 카운트 증가
            else:
                break  # 일치하지 않으면 루프 종료
        nx, ny = x, y
        while True:
            nx -= dx * (width // 19)  # X 좌표 되돌리기
            ny -= dy * (height // 19)  # Y 좌표 되돌리기
            if (nx, ny, color) in stones:
                count += 1  # 돌이 일치하면 카운트 증가
            else:
                break  # 일치하지 않으면 루프 종료
        if count >= 5:
            return True  # 5개 이상의 돌이 일치하면 승리
    return False  # 승리 조건을 만족하지 않으면 False 반환

def game_over_message(winner):
    font = pygame.font.Font(None, 74)  # 큰 글꼴 설정
    text = font.render(f"{winner} wins!", True, (255, 0, 0))  # 승리 메시지 생성
    screen.fill(background_color)  # 배경으로 화면을 채움
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))  # 메시지 표시
    
    restart_font = pygame.font.Font(None, 36)  # 작은 글꼴 설정
    restart_text = restart_font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))  # 재시작 및 종료 메시지 생성
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + text.get_height()))  # 메시지 표시
    
    pygame.display.flip()  # 화면 업데이트

def reset_game():
    global stones
    stones = []  # 돌 목록 초기화

def evaluate_move(x, y, color):
    """Evaluate the score of a potential move, including offensive and defensive aspects."""  # 잠재적 이동 평가 함수
    score = 0  # 점수 초기화
    opponent_color = black_circle_color if color == white_circle_color else white_circle_color  # 상대방 색상 설정
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]  # 방향 정의
    
    for dx, dy in directions:
        count = 1  # 현재 돌 포함
        nx, ny = x, y
        while True:
            nx += dx * (width // 19)  # X 좌표 이동
            ny += dy * (height // 19)  # Y 좌표 이동
            if (nx, ny, color) in stones:
                count += 1  # 돌이 일치하면 카운트 증가
            else:
                break  # 일치하지 않으면 루프 종료
        nx, ny = x, y
        while True:
            nx -= dx * (width // 19)  # X 좌표 되돌리기
            ny -= dy * (height // 19)  # Y 좌표 되돌리기
            if (nx, ny, color) in stones:
                count += 1  # 돌이 일치하면 카운트 증가
            else:
                break  # 일치하지 않으면 루프 종료
        if count >= 5:
            score += 1000  # 승리 이동에 대해 큰 점수 추가
        
        # Defensive evaluation
        opponent_count = 1  # 상대방 돌 카운트 초기화
        nx, ny = x, y
        while True:
            nx += dx * (width // 19)  # X 좌표 이동
            ny += dy * (height // 19)  # Y 좌표 이동
            if (nx, ny, opponent_color) in stones:
                opponent_count += 1  # 돌이 일치하면 카운트 증가
            else:
                break  # 일치하지 않으면 루프 종료
        nx, ny = x, y
        while True:
            nx -= dx * (width // 19)  # X 좌표 되돌리기
            ny -= dy * (height // 19)  # Y 좌표 되돌리기
            if (nx, ny, opponent_color) in stones:
                opponent_count += 1  # 돌이 일치하면 카운트 증가
            else:
                break  # 일치하지 않으면 루프 종료
        if opponent_count >= 4:
            score += 500  # 상대방의 승리 이동 차단에 대해 높은 점수 추가
        elif opponent_count == 3:
            score += 200  # 잠재적 위협 차단에 대해 중간 점수 추가
    return score  # 점수 반환

def ai_move():
    """Choose the best move for the AI, considering both offense and defense."""  # AI의 최적 이동 선택 함수
    best_score = -1  # 최고의 점수 초기화
    best_move = None  # 최고의 이동 초기화
    for x in range(0, width, width // 19):
        for y in range(0, height, height // 19):
            if not is_occupied((x, y)):  # 위치가 점유되지 않았으면
                score = evaluate_move(x, y, white_circle_color)  # 이동 평가
                if score > best_score:
                    best_score = score  # 최고의 점수 갱신
                    best_move = (x, y)  # 최고의 이동 갱신
    return best_move  # 최고의 이동 반환

##################################
# 3. 메인 게임 루프

def main_game_loop():
    global stones
    current_color = black_circle_color  # 현재 색상 초기화
    reset_game()  # 게임 초기화
    running = True  # 게임 실행 상태 초기화
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # 게임 종료
                sys.exit()  # 시스템 종료
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # 마우스 클릭 위치 가져오기
                grid_pos = get_grid_position(pos)  # 그리드 위치 계산
                if current_color == black_circle_color:
                    if not is_occupied(grid_pos):  # 위치가 점유되지 않았으면
                        stones.append((grid_pos[0], grid_pos[1], current_color))  # 돌 추가
                        if check_winner(grid_pos[0], grid_pos[1], current_color):
                            game_over_message("Black")  # 검정색 승리 메시지 표시
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()  # 게임 종료
                                        sys.exit()  # 시스템 종료
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_r:
                                            reset_game()  # 게임 재시작
                                            break
                                        elif event.key == pygame.K_q:
                                            pygame.quit()  # 게임 종료
                                            sys.exit()  # 시스템 종료
                                else:
                                    continue
                                break
                        current_color = white_circle_color  # 색상 전환
                else:
                    ai_pos = ai_move()  # AI의 이동 선택
                    if ai_pos:
                        stones.append((ai_pos[0], ai_pos[1], current_color))  # AI 돌 추가
                        if check_winner(ai_pos[0], ai_pos[1], current_color):
                            game_over_message("White")  # 흰색 승리 메시지 표시
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()  # 게임 종료
                                        sys.exit()  # 시스템 종료
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_r:
                                            reset_game()  # 게임 재시작
                                            break
                                        elif event.key == pygame.K_q:
                                            pygame.quit()  # 게임 종료
                                            sys.exit()  # 시스템 종료
                                else:
                                    continue
                                break
                    current_color = black_circle_color  # 색상 전환
        draw_board()  # 바둑판 그리기

if __name__ == "__main__":
    main_game_loop()  # 메인 게임 루프 실행
