import pygame
import random

pygame.init()

#Ekran ayarları
screen = pygame.display.set_mode((600, 650))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#Minnak kullanışlı fonksiyonum
def load_image(name):
    return pygame.image.load(name)

#Fotolar
head_left = load_image("leftHead.png")
head_right = load_image("rightHead.png")
head_up = load_image("upHead.png")
head_down = load_image("downHead.png")
apple_image = load_image("apple.png")
tail_image = load_image("tail.png")

#Başlangıç konumları
head_position = head_left.get_rect(topleft=(250, 250))
apple_position = apple_image.get_rect()

#Kuyruk segmentleri
tail_segments = []

# Ses yükleme
voice = pygame.mixer.Sound("dırıt.mp3")

#Yazılar
myFont = pygame.font.SysFont("arialblack", 32)
score = 0
score_text = myFont.render(f"Score: {score}", True, (222, 222, 222))
score_position = score_text.get_rect(topleft=(200, 600))

#Yılanın gidişaat
speed = 50
direction = None
head_image = head_left



#Rastgele elma oluşturma
def new_apple():
    while True:
        position = pygame.Rect(random.randint(0, 550 // 50) * 50, random.randint(0, 550 // 50) * 50, apple_image.get_width(), apple_image.get_height())
        if position.colliderect(head_position) or any(segment.colliderect(position) for segment in tail_segments):
            continue
        return position

apple_position = new_apple()

#Game Over
def game_over():
    global running
    game_over_text = myFont.render("GAME OVER", True, (255, 0, 0))
    game_over_position = game_over_text.get_rect(center=(300, 300))
    screen.blit(game_over_text, game_over_position)
    pygame.display.update()
    pygame.time.wait(3000)
    running = False

#Loopumuz
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if direction != 'right':
                    direction = 'left'
            elif event.key == pygame.K_RIGHT:
                if direction != 'left':
                    direction = 'right'
            elif event.key == pygame.K_UP:
                if direction != 'down':
                    direction = 'up'
            elif event.key == pygame.K_DOWN:
                if direction != 'up':
                    direction = 'down'

    #Kuyruk segmentlerini güncelle
    if tail_segments:
        for i in range(len(tail_segments) - 1, 0, -1):
            tail_segments[i].topleft = tail_segments[i - 1].topleft
        tail_segments[0].topleft = head_position.topleft

    #Yönlere göre hareket et
    if direction == 'left':
        head_position.x -= speed
        head_image = head_left
    elif direction == 'right':
        head_position.x += speed
        head_image = head_right
    elif direction == 'up':
        head_position.y -= speed
        head_image = head_up
    elif direction == 'down':
        head_position.y += speed
        head_image = head_down

    #Duvara çarpma
    if head_position.x < 0 or head_position.x >= 600 or head_position.y < 0 or head_position.y >= 600:
        game_over()
    elif any(segment.colliderect(head_position) for segment in tail_segments):
        game_over()

    #Çarpışma
    if head_position.colliderect(apple_position):
        score += 1
        score_text = myFont.render(f"Score: {score}", True, (222, 222, 222))
        voice.play()
        apple_position = new_apple()
        tail_segments.append(head_position.copy())

    #Ekranı güncelle
    screen.fill((244, 244, 244))
    pygame.draw.line(screen, (39, 215, 255), (0, 650), (600, 650), 102)
    for segment in tail_segments:
        screen.blit(tail_image, segment)
    screen.blit(head_image, head_position)
    screen.blit(apple_image, apple_position)
    screen.blit(score_text, score_position)

    pygame.display.update()
    clock.tick(7)

pygame.quit()
