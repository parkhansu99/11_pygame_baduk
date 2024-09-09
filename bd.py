import pygame  # Pygame 모듈을 가져옵니다.

# 초기화
pygame.init()  # Pygame을 초기화합니다.

# 화면 크기 및 설정
width, height = 600, 600  # 화면의 너비와 높이를 설정합니다.
line_color = (0, 0, 0)  # 검정색으로 선의 색상을 설정합니다.
background_color = (255, 255, 255)  # 흰색으로 배경색을 설정합니다.

line_width = 2  # 선의 두께를 설정합니다.
circle_radius = 15  # 동그라미의 반지름을 설정합니다.
black_circle_color = (0, 0, 0)  # 검정색으로 동그라미의 색상을 설정합니다.
white_circle_color = (255, 255, 255)  # 흰색으로 동그라미의 색상을 설정합니다.
circle_border_color = (0, 0, 0)  # 검정색으로 동그라미의 테두리 색상을 설정합니다.

# 화면 생성
screen = pygame.display.set_mode((width, height))  # 지정한 크기로 화면을 생성합니다.
pygame.display.set_caption("19x19 Go Board")  # 윈도우 제목을 설정합니다.

# 바둑판 격자 그리기
def draw_board():  # 바둑판을 그리는 함수입니다.
    screen.fill(background_color)  # 배경을 흰색으로 채우기

    cell_size = width // 19  # 각 셀의 크기 계산
    for i in range(19):  # 19개의 수평선을 그립니다.
        # 수평선 그리기
        pygame.draw.line(screen, line_color, (0, i * cell_size), (width, i * cell_size), line_width)  # 수평선을 그립니다.
        # 수직선 그리기
        pygame.draw.line(screen, line_color, (i * cell_size, 0), (i * cell_size, height), line_width)  # 수직선을 그립니다.
    
    # 클릭한 위치에 동그라미 그리기
    for (x, y, color) in stones:  # 동그라미 리스트를 순회합니다.
        pygame.draw.circle(screen, color, (x, y), circle_radius)  # 동그라미를 그립니다.
        pygame.draw.circle(screen, circle_border_color, (x, y), circle_radius, line_width)  # 동그라미의 테두리를 그립니다.
    
    pygame.display.flip()  # 화면을 업데이트합니다.

# 클릭한 위치를 격자 선에 맞게 조정하는 함수
def get_grid_position(pos):  # 클릭한 위치를 격자에 맞게 조정하는 함수입니다.
    cell_size = width // 19  # 각 셀의 크기 계산
    # x = (pos[0] // cell_size) * cell_size  # 클릭한 위치의 x좌표를 격자에 맞게 조정합니다.
    # y = (pos[1] // cell_size) * cell_size  # 클릭한 위치의 y좌표를 격자에 맞게 조정합니다.
    # 위의 수식은 바둑알이 조금만 격자의 교차점에서 벗어나더라도 잘못된 위치에 두는 오류가 발생, 반대로 아래의 수식은 격자 영역의 절반 정도까지의 오차를 허용함
    x = ((pos[0] + cell_size // 2) // cell_size) * cell_size  # 클릭한 위치의 x좌표를 격자에 맞게 조정합니다.
    y = ((pos[1] + cell_size // 2) // cell_size) * cell_size  # 클릭한 위치의 y좌표를 격자에 맞게 조정합니다.
    return (x, y)  # 조정된 좌표를 반환합니다.

# 동그라미 정보 리스트 (위치와 색상)
stones = []  # 동그라미의 위치와 색상을 저장하는 리스트입니다.

# 이미 동그라미가 있는지 확인하는 함수
def is_occupied(pos):  # 주어진 위치에 이미 동그라미가 있는지 확인하는 함수입니다.
    for (x, y, _) in stones:  # 동그라미 리스트를 순회합니다.
        # 동그라미의 위치와 겹치는지 확인합니다.
        if x == pos[0] and y == pos[1]:  # 위치가 겹치면 True를 반환합니다.
            return True
    return False  # 위치가 겹치지 않으면 False를 반환합니다.

# 메인 루프
current_color = black_circle_color  # 현재 색상을 검정색으로 설정합니다.
running = True  # 게임 루프를 실행합니다.
while running:  # 게임 루프입니다.
    for event in pygame.event.get():  # 모든 이벤트를 처리합니다.
        if event.type == pygame.QUIT:  # 종료 이벤트 처리
            running = False  # 루프를 종료합니다.
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼 클릭 이벤트 처리
            pos = pygame.mouse.get_pos()  # 마우스 클릭 위치를 가져옵니다.
            grid_pos = get_grid_position(pos)  # 격자 위치로 변환합니다.
            if not is_occupied(grid_pos):  # 위치가 이미 점유되어 있는지 확인합니다.
                stones.append((grid_pos[0], grid_pos[1], current_color))  # 동그라미를 추가합니다.
                # 색상 전환
                current_color = white_circle_color if current_color == black_circle_color else black_circle_color  # 색상을 전환합니다.
    
    draw_board()  # 바둑판을 다시 그립니다.

pygame.quit()  # Pygame을 종료합니다.
