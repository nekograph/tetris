import pygame
import random

# 初期化
pygame.init()

# グリッドサイズとブロックサイズ
grid_width, grid_height = 10, 20
block_size = 30
score_space = 200
screen_height = grid_height * block_size 
screen_width =  grid_width * block_size + score_space

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
font = pygame.font.Font(None, 36)

# 色の定義
colors = [RED,GREEN,BLUE,YELLOW]  # 赤、緑、青、黄

# ブロックの形状
shapes = [    
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 0, 0], [1, 1, 1]],
    [[0 ,0,-1], [1 ,1 ,1]],
    [[-1, 0, 0],[1, 1, 1]]
]

# ゲームグリッド
grid = [[0] * grid_width for _ in range(grid_height)]

# ブロックのクラス
class Block:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.color = random.choice(colors)
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def can_move(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= grid_width or new_y >= grid_height or grid[new_y][new_x]:
                        return False
        return True

    def fix_to_grid(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color

# 行を消去してスコアを更新する関数
def clear_rows():
    global score,score_get
    new_grid = []  # new_grid を初期化
    removed_rows =0
    removed_rows_same = 0
    score_get = 0
    for row in grid:
        if all(row):  # 全てのセルが埋まっているか確認
            first_color = row[0]  # 行の最初の色を取得
            if all(cell == first_color for cell in row):  # 全て同じ色か確認
                removed_rows_same += 1 # 全て同じ色の場合
                removed_rows += 1
            else:
                removed_rows += 1  # 色が異なる場合、通常のスコアを加算
        else:
            new_grid.append(row)  # 新しい行として追加
    
    if removed_rows_same > 0:
        score_get = (removed_rows - removed_rows_same)*100 + removed_rows_same*500
        score += score_get
        
    else:
        score_get = removed_rows*100
        score += score_get
        

    removed_rows = grid_height - len(new_grid)
    new_grid = [[0] * grid_width for _ in range(removed_rows)] + new_grid
    return new_grid


def draw_score():
    # スコア表示部分の背景
    pygame.draw.rect(screen, GRAY, [screen_width-score_space, 0, score_space, screen_height])

    # スコアのテキスト
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width - 140, 20))


# ゲームループ
current_block = Block()
score = 0
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.7  # ブロックの落下速度 (値を大きくするとゆっくりになる)
speed_count = 0
running = True
score_get = 0

while running:
    screen.fill((0, 0, 0))
    fall_time += clock.get_rawtime()
    clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_block.can_move(-1, 0):
                current_block.move_left()
            elif event.key == pygame.K_RIGHT and current_block.can_move(1, 0):
                current_block.move_right()
            elif event.key == pygame.K_DOWN and current_block.can_move(0, 1):
                current_block.move_down()
            elif event.key == pygame.K_UP:
                current_block.rotate()
                if not current_block.can_move(0, 0):
                    current_block.rotate()  # 元に戻す

    if fall_time / 1000 >= fall_speed:
        if current_block.can_move(0, 1):
            current_block.move_down()
        else:
            current_block.fix_to_grid()
            grid = clear_rows()
            current_block = Block()
            if not current_block.can_move(0, 0):  # 新しいブロックが生成された直後に動けなければゲームオーバー
                running = False
        fall_time = 0
    
    if score_get > 100:
        speed_count += score_get / 100
        score_get = 0
    
    if speed_count >= 10:
        fall_speed = fall_speed/1.5
        speed_count = 0
    # グリッドの描画
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                                 pygame.Rect(x * block_size, y * block_size, block_size, block_size))

    # ブロックの描画
    for y, row in enumerate(current_block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_block.color,
                                 pygame.Rect((current_block.x + x) * block_size, (current_block.y + y) * block_size, block_size, block_size))

            
    draw_score()
    
    pygame.display.flip()

