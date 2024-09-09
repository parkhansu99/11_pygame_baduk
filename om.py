import pygame  # Pygame 모듈을 가져옵니다.
import sys  # 시스템 관련 모듈을 가져옵니다.

##################################
# 1. 기본 초기화

pygame.init()  # Pygame을 초기화합니다.

# 화면 크기 및 설정
width, height = 600, 600  # 화면의 너비와 높이를 설정합니다.
line_color = (0, 0, 0)  # 선의 색상을 검정색으로 설정합니다.
background_color = (255, 255, 255)  # 배경색을 흰색으로 설정합니다.
line_width = 2  # 선의 두께를 설정합니다.
circle_radius = 15  # 동그라미의 반지름을 설정합니다.
black_circle_color = (0, 0, 0)  # 검정색 동그라미의 색상입니다.
white_circle_color = (255, 255, 255)  # 흰색 동그라미의 색상입니다.
circle_border_color = (0, 0, 0)  # 동그라미의 테두리 색상입니다.

# 화면 생성
screen = pygame.display.set_mode((width, height))  # 주어진 크기로 화면을 생성합니다.
pygame.display.set_caption("19x19 Go Board")  # 윈도우의 제목을 설정합니다.

##################################
# 2. 바둑판 및 돌 관련 함수

# 바둑판 격자 그리기
def draw_board():  # 바둑판을 그리는 함수입니다.
    screen.fill(background_color)  # 배경을 흰색으로 채웁니다.
    cell_size = width // 19  # 셀의 크기를 계산합니다.
    for i in range(19):  # 19개의 수평선과 수직선을 그립니다.
        pygame.draw.line(screen, line_color, (0, i * cell_size), (width, i * cell_size), line_width)  # 수평선을 그립니다.
        pygame.draw.line(screen, line_color, (i * cell_size, 0), (i * cell_size, height), line_width)  # 수직선을 그립니다.
    
    for (x, y, color) in stones:  # 동그라미 리스트를 순회합니다.
        pygame.draw.circle(screen, color, (x, y), circle_radius)  # 동그라미를 그립니다.
        pygame.draw.circle(screen, circle_border_color, (x, y), circle_radius, line_width)  # 동그라미의 테두리를 그립니다.
    
    pygame.display.flip()  # 화면을 업데이트합니다.

# 클릭한 위치를 격자 선에 맞게 조정하는 함수
def get_grid_position(pos):  # 클릭한 위치를 격자에 맞게 조정하는 함수입니다.
    cell_size = width // 19  # 셀의 크기를 계산합니다.
    x = ((pos[0] + cell_size // 2) // cell_size) * cell_size  # x좌표를 격자에 맞게 조정합니다.
    y = ((pos[1] + cell_size // 2) // cell_size) * cell_size  # y좌표를 격자에 맞게 조정합니다.
    return (x, y)  # 조정된 좌표를 반환합니다.

# 동그라미 정보 리스트 (위치와 색상)
stones = []  # 동그라미의 위치와 색상을 저장하는 리스트입니다.

# 이미 동그라미가 있는지 확인하는 함수
def is_occupied(pos):  # 주어진 위치에 동그라미가 있는지 확인하는 함수입니다.
    for (x, y, _) in stones:  # 동그라미 리스트를 순회합니다.
        if x == pos[0] and y == pos[1]:  # 위치가 겹치면 True를 반환합니다.
            return True
    return False  # 위치가 겹치지 않으면 False를 반환합니다.

# 연속된 돌의 개수를 확인하는 함수
def check_winner(x, y, color):  # 주어진 위치에서 승리 조건을 확인하는 함수입니다.
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]  # 8가지 방향을 정의합니다.
    for dx, dy in directions:  # 각 방향에 대해 체크합니다.
        count = 1  # 현재 돌을 포함하여 세기 시작합니다.
        nx, ny = x, y  # 현재 위치를 설정합니다.
        while True:  # 한 방향으로 연속된 돌을 세기 시작합니다.
            nx += dx * (width // 19)  # 다음 위치로 이동합니다.
            ny += dy * (height // 19)  # 다음 위치로 이동합니다.
            if (nx, ny, color) in stones:  # 해당 위치에 같은 색의 돌이 있는지 확인합니다.
                count += 1  # 돌이 있으면 개수를 증가시킵니다.
            else:
                break  # 더 이상 연속된 돌이 없으면 중단합니다.
        nx, ny = x, y  # 현재 위치로 복원합니다.
        while True:  # 반대 방향으로 연속된 돌을 세기 시작합니다.
            nx -= dx * (width // 19)  # 이전 위치로 이동합니다.
            ny -= dy * (height // 19)  # 이전 위치로 이동합니다.
            if (nx, ny, color) in stones:  # 해당 위치에 같은 색의 돌이 있는지 확인합니다.
                count += 1  # 돌이 있으면 개수를 증가시킵니다.
            else:
                break  # 더 이상 연속된 돌이 없으면 중단합니다.
        if count >= 5:  # 연속된 돌이 5개 이상이면 승리 조건을 만족합니다.
            return True
    return False  # 승리 조건을 만족하지 않으면 False를 반환합니다.

# 게임 종료 메시지 함수
def game_over_message(winner):  # 게임 종료 메시지를 표시하는 함수입니다.
    font = pygame.font.Font(None, 74)  # 폰트를 설정합니다.
    text = font.render(f"{winner} wins!", True, (255, 0, 0))  # 승리 메시지를 생성합니다.
    screen.fill(background_color)  # 배경을 흰색으로 채웁니다.
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))  # 승리 메시지를 화면에 출력합니다.
    
    restart_font = pygame.font.Font(None, 36)  # 재시작 및 종료 메시지 폰트를 설정합니다.
    restart_text = restart_font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))  # 메시지를 생성합니다.
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + text.get_height()))  # 재시작 및 종료 메시지를 화면에 출력합니다.
    
    pygame.display.flip()  # 화면을 업데이트합니다.

# 게임을 초기화하는 함수
def reset_game():  # 게임을 재시작하기 위한 함수입니다.
    global stones  # stones 리스트를 전역 변수로 사용합니다.
    stones = []  # 동그라미 리스트를 초기화합니다.

##################################
# 3. 메인 게임 루프

def main_game_loop():  # 게임의 메인 루프를 처리하는 함수입니다.
    global stones  # stones 리스트를 전역 변수로 사용합니다.
    current_color = black_circle_color  # 현재 색상을 검정색으로 설정합니다.
    reset_game()  # 게임을 초기화합니다.
    running = True  # 게임 루프를 실행합니다.
    while running:  # 게임 루프입니다.
        for event in pygame.event.get():  # 모든 이벤트를 처리합니다.
            if event.type == pygame.QUIT:  # 종료 이벤트 처리
                pygame.quit()  # Pygame을 종료합니다.
                sys.exit()  # 프로그램을 종료합니다.
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트 처리
                pos = pygame.mouse.get_pos()  # 마우스 클릭 위치를 가져옵니다.
                grid_pos = get_grid_position(pos)  # 격자 위치로 변환합니다.
                if not is_occupied(grid_pos):  # 위치가 점유되어 있는지 확인합니다.
                    stones.append((grid_pos[0], grid_pos[1], current_color))  # 동그라미를 추가합니다.
                    if check_winner(grid_pos[0], grid_pos[1], current_color):  # 승리 조건을 확인합니다.
                        game_over_message("Black" if current_color == black_circle_color else "White")  # 승리 메시지를 표시합니다.
                        while True:  # 사용자 입력을 대기합니다.
                            for event in pygame.event.get():  # 모든 이벤트를 처리합니다.
                                if event.type == pygame.QUIT:  # 종료 이벤트 처리
                                    pygame.quit()  # Pygame을 종료합니다.
                                    sys.exit()  # 프로그램을 종료합니다.
                                elif event.type == pygame.KEYDOWN:  # 키보드 이벤트 처리
                                    if event.key == pygame.K_r:  # 재시작 키를 눌렀을 때
                                        reset_game()  # 게임을 재시작합니다.
                                        break  # 내부 루프를 종료합니다.
                                    elif event.key == pygame.K_q:  # 종료 키를 눌렀을 때
                                        pygame.quit()  # Pygame을 종료합니다.
                                        sys.exit()  # 프로그램을 종료합니다.
                            else:
                                continue  # break가 호출되지 않으면 계속 루프를 반복합니다.
                            break  # break가 호출되면 게임 루프를 종료합니다.
                    current_color = white_circle_color if current_color == black_circle_color else black_circle_color  # 색상을 변경합니다.
        draw_board()  # 바둑판을 그립니다.

# 게임 시작
if __name__ == "__main__":  # 스크립트가 직접 실행될 때
    main_game_loop()  # 메인 게임 루프를 실행합니다.
