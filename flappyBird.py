import pygame, sys, random
from pygame.locals import *

pygame.mixer.init()
pygame.mixer.music.load('path/background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

hit_sound = pygame.mixer.Sound('path/hit_effect.wav')

#from video import threadVideo
from nhap import threadVideo  # If need to extract the XYZ coordiantes of the hand and save to the csv file
WINDOWWIDTH = 800
WINDOWHEIGHT = 400

BIRDWIDTH = 30
BIRDHEIGHT = 30
G = 0.02
SPEEDFLY = -0.5
BIRDIMG = pygame.image.load('img/bird.png')

COLUMNWIDTH = 60
COLUMNHEIGHT = 300
BLANK = 150
DISTANCE = 300
COLUMNSPEED = 2
COLUMNIMG = pygame.image.load('img/column.png')
COLUMNIMG = pygame.transform.scale(COLUMNIMG, (COLUMNWIDTH, COLUMNHEIGHT))

BACKGROUND = pygame.image.load('img/background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))

pygame.init()
FPS = 90
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird')

def inputPlayerInfo():
    """Hàm nhập thông tin người chơi"""
    name = ''
    year = ''
    active_input = 'name'  # Hiển thị input hiện tại: 'name' hoặc 'year'
    
    font = pygame.font.SysFont('consolas', 30)
    headingSuface = font.render('Player Info', True, (255, 255, 255))
    headingSize = headingSuface.get_size()
    
    namePrompt = font.render('Name: ', True, (255, 255, 255))
    yearPrompt = font.render('Age: ', True, (255, 255, 255))
    
    while True:
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0]) / 2), 100))
        
        # Hiển thị prompt và input field cho Name
        DISPLAYSURF.blit(namePrompt, (100, 200))  # Căn chỉnh tên
        pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (350, 200, 300, 40), 2)
        nameSurface = font.render(name, True, (255, 255, 255))
        DISPLAYSURF.blit(nameSurface, (360, 205))  # Căn chỉnh tên nhập vào
        
        # Hiển thị prompt và input field cho Year
        DISPLAYSURF.blit(yearPrompt, (100, 300))  # Căn chỉnh năm sinh
        pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (350, 300, 300, 40), 2)
        yearSurface = font.render(year, True, (255, 255, 255))
        DISPLAYSURF.blit(yearSurface, (360, 305))  # Căn chỉnh năm sinh nhập vào
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    # Xóa ký tự cuối của input hiện tại
                    if active_input == 'Name':
                        name = name[:-1]
                    elif active_input == 'Age':
                        year = year[:-1]
                elif event.key == K_TAB:
                    # Chuyển đổi giữa input 'name' và 'year'
                    active_input = 'age' if active_input == 'name' else 'name'
                elif event.key == K_RETURN:
                    # Kết thúc nhập thông tin nếu đủ dữ liệu
                    if name.strip() and year.strip().isdigit():
                        return name.strip(), int(year)
                else:
                    # Thêm ký tự vào input hiện tại
                    if active_input == 'name':
                        name += event.unicode
                    elif active_input == 'age' and event.unicode.isdigit():
                        year += event.unicode

class Bird():
    def __init__(self):
        self.width = BIRDWIDTH
        self.height = BIRDHEIGHT
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
        self.speed = 5
        self.suface = BIRDIMG

    def draw(self):
        DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))
    
    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G
        if mouseClick == True:
            self.speed = SPEEDFLY

class Columns():
    def __init__(self):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMNSPEED
        self.surface = COLUMNIMG
        self.ls = []
        for i in range(3):
            x = WINDOWWIDTH + i*self.distance
            y = random.randrange(50, WINDOWHEIGHT - self.blank - 50, 20)
            self.ls.append([x, y])
        
    def draw(self):
        for i in range(3):
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))
    
    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        
        if self.ls[0][0] < -self.width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 10)
            self.ls.append([x, y])

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(bird, columns):
    for i in range(3):
        rectBird = [bird.x, bird.y, bird.width, bird.height]
        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            hit_sound.play()
            return True
    if bird.y + bird.height < 0 or bird.y > WINDOWHEIGHT:
        hit_sound.play()
        return True
    return False

class Score():
    def __init__(self):
        self.score = 0
        self.addScore = True
        self.columns_passed = 0

    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        scoreSuface = font.render(str(self.score), True, (255, 255, 255))
        textSize = scoreSuface.get_size()
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))
    
    def update(self, bird, columns):
        collision = False
        for i in range(3):
            rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
            rectBird = [bird.x, bird.y, bird.width, bird.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
                self.columns_passed += 1  # Tăng biến đếm cột
            self.addScore = False
        else:
            self.addScore = True

def gameStart(bird):  # Gọi hàm hiển thị màn hình hướng dẫnn
    bird.__init__()

    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('FLAPPY BIRD', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Click to start', True, (255, 255, 255))
    commentSize = commentSuface.get_size()
# Thêm hướng dẫn về điều khiển
    instructionSuface = font.render(
        'Điều khiển chim Flappy bằng tay qua camera.', True, (255, 255, 255))
    instructionSize = instructionSuface.get_size()
    
    instructionDetailsSuface = font.render(
        'Chạm các đầu ngón tay để chim bay lên, duỗi tay để chim rơi xuống.', True, (255, 255, 255))
    instructionDetailsSize = instructionDetailsSuface.get_size()
    
    fontSmall = pygame.font.SysFont('consolas', 15)
    moreDetailsSuface = fontSmall.render(
        'Nhấn "Click" để bắt đầu trò chơi. Chúc bạn chơi vui vẻ!', True, (255, 255, 255))
    moreDetailsSize = moreDetailsSuface.get_size()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                return

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        bird.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))

        DISPLAYSURF.blit(instructionSuface, (int((WINDOWWIDTH - instructionSize[0])/2), 200))
        DISPLAYSURF.blit(instructionDetailsSuface, (int((WINDOWWIDTH - instructionDetailsSize[0])/2), 250))
        DISPLAYSURF.blit(moreDetailsSuface, (int((WINDOWWIDTH - moreDetailsSize[0])/2), 300))

        pygame.display.update()
        fpsClock.tick(FPS)

def gamePlay(bird, columns, score, xyz):
    bird.__init__()
    bird.speed = SPEEDFLY
    columns.__init__()
    score.__init__()
    current_speed = COLUMNSPEED  # Lưu tốc độ hiện tại
    current_distance = DISTANCE  # Lưu khoảng cách hiện tại
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True
        if xyz.dist < 0.1:
            mouseClick = True
        print(xyz.dist)
        if score.columns_passed > 0 and score.columns_passed % 10 == 0:
            current_speed += 0.3  # Tăng tốc độ cột
            current_distance = max(200, current_distance - 10)  # Giảm khoảng cách tối thiểu giữa các cột
            columns.speed = current_speed  # Áp dụng tốc độ mới
            columns.distance = current_distance  # Áp dụng khoảng cách mới
            score.columns_passed += 1  # Ngăn tăng tốc lặp lại trong cùng một lượt
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        columns.update()
        bird.draw()
        bird.update(mouseClick)
        score.draw()
        score.update(bird, columns)

        if isGameOver(bird, columns) == True:
            return

        pygame.display.update()
        fpsClock.tick(FPS)

def gameOver(bird, columns, score, player_info):
    """Hiển thị màn hình kết thúc trò chơi"""
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 255, 255))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (255, 255, 255))
    commentSize = commentSuface.get_size()

    font = pygame.font.SysFont('consolas', 30)
    scoreSuface = font.render(f'Score: {score.score}', True, (255, 255, 255))
    scoreSize = scoreSuface.get_size()
    
    playerNameSurface = font.render(f'Name: {player_info[0]}', True, (255, 255, 255))
    playerNameSize = playerNameSurface.get_size()
    
    playerYearSurface = font.render(f'Year: {player_info[1]}', True, (255, 255, 255))
    playerYearSize = playerYearSurface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    return
        
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        bird.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))
        DISPLAYSURF.blit(playerNameSurface, (int((WINDOWWIDTH - playerNameSize[0])/2), 200))
        DISPLAYSURF.blit(playerYearSurface, (int((WINDOWWIDTH - playerYearSize[0])/2), 250))

        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    bird = Bird()
    columns = Columns()
    score = Score()
    xyz = threadVideo()
    xyz.start()
    player_info = inputPlayerInfo()  # Gọi hàm nhập thông tin người chơi

    while True:
        
        gameStart(bird)
        gamePlay(bird, columns, score, xyz)
        gameOver(bird, columns, score, player_info)
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
    main()