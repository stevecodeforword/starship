import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space dodge")

Background = pygame.transform.scale(pygame.image.load("stars.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 10
PLAYER_HEIGHT = 20
# VELOCITY
PLAYER_VEL = 3
STAR_WIDTH = 10
STAR_HEIGHT = 10
font = pygame.font.SysFont("comicsans", 30)
STAR_VEL = 2

# 載入背景
def draw(player, elapsed_time, stars):
    WIN.blit(Background, (0, 0))
    # 裡面的 1 是把字反鋸齒
    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    # 畫在哪裡>>WIN, 顏色, 主體
    pygame.draw.rect(WIN, "red", player)
    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)
    pygame.display.update()


def main():
    player = pygame.Rect(300, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False
    run = True
    # 優先做關閉頁面
    while run:
        # 注意每台電腦的秒針移動的毫秒數不一樣所以假設現在這台電腦每20毫秒一個tick 就是三秒加一次
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                # 第二個參數星星y軸用負號是為了讓他從螢幕外掉下來 (x位置, y位置, 寬, 高)
                star = pygame.Rect(star_x, - STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            # 增加星星的時間愈來愈短
            star_add_increment = max(200, star_add_increment-50)
            star_count = 0
        # event 可以想成是每一偵畫面
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            # 減號是因為x軸往左
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            # 加號是因為x軸往右
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        if hit:
            lost_text = font.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2-lost_text.get_width()/2,HEIGHT/2-lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        # 每一偵都要有背景被畫出來
        draw(player, elapsed_time, stars)

    pygame.quit()


# 下面這行的條件單純是指說只讓這個檔案在main被啟用
if __name__ == '__main__':
    main()
