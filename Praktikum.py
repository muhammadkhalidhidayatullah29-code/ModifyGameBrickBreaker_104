import pygame
import random

pygame.init()

# Ukuran Area (800x600)
WIDTH, HEIGHT = 800, 800

# Tema Gelap & Warna Neon Menyala (Deep Space & Cyberpunk)
BG_COLOR = (8, 8, 14)           # Hitam pekat kebiruan
TEXT_COLOR = (240, 240, 255)    # Putih terang
STRIKER_COLOR = (0, 243, 255)   # Neon Cyan Menyala
BALL_COLOR = (255, 0, 127)      # Neon Pink Menyala

# Palet warna balok neon berpendar
BLOCK_COLORS = [
    (0, 255, 120),    # Neon Green
    (255, 0, 255),    # Neon Magenta
    (255, 230, 0),    # Neon Yellow
    (0, 180, 255)     # Electric Blue
]

font = pygame.font.Font('freesansbold.ttf', 16)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker - Perfect Margin Neon Edition")

clock = pygame.time.Clock()
FPS = 60


# Fungsi Helper untuk Membuat Efek Cahaya Neon Berpendar (Glow)
def draw_glowing_rect(surf, color, rect, border_radius=4):
    x, y, w, h = rect
    glow_surf = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*color, 50), (0, 0, w + 10, h + 10), border_radius=border_radius + 2)
    surf.blit(glow_surf, (x - 5, y - 5))
    
    pygame.draw.rect(surf, color, rect, border_radius=border_radius)
    highlight_rect = pygame.Rect(x + 2, y + 2, w - 4, 2)
    pygame.draw.rect(surf, (255, 255, 255), highlight_rect, border_radius=1)


def draw_glowing_circle(surf, color, center, radius):
    cx, cy = center
    glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*color, 80), (radius * 2, radius * 2), radius * 1.6)
    surf.blit(glow_surf, (cx - radius * 2, cy - radius * 2))
    
    pygame.draw.circle(surf, color, center, radius)
    pygame.draw.circle(surf, (255, 255, 255), (cx - 2, cy - 2), max(1, radius // 3))


# Striker Class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.width_base = width, width
        self.height = height
        self.speed = speed
        self.color = color

    def display(self):
        rect = (self.posx, self.posy, self.width, self.height)
        draw_glowing_rect(screen, self.color, rect, border_radius=8)

    def update(self, xFac):
        self.posx += self.speed * xFac

        # Batas pinggir aplikasi diberi jarak aman agar striker tidak mentok luar
        if self.posx <= 35:
            self.posx = 35
        elif self.posx + self.width >= WIDTH - 35:
            self.posx = WIDTH - 35 - self.width

    def reset_size(self):
        self.width = self.width_base

    def getRect(self):
        return pygame.Rect(self.posx, self.posy, self.width, self.height)


# Block Class
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.health = 100
        self.damage = 100

    def display(self):
        if self.health > 0:
            rect = (self.posx, self.posy, self.width, self.height)
            draw_glowing_rect(screen, self.color, rect, border_radius=4)

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return pygame.Rect(self.posx, self.posy, self.width, self.height)

    def getHealth(self):
        return self.health


# PowerUp Class
class PowerUp:
    def __init__(self, posx, posy, type_name):
        self.posx = posx
        self.posy = posy
        self.width = 30
        self.height = 30
        self.speed = 3
        self.type_name = type_name  

    def update(self):
        self.posy += self.speed

    def display(self):
        if self.type_name == 'multi':
            color = (255, 230, 0)   # Kuning (x2)
            label = "x2"
        elif self.type_name == 'triple':
            color = (255, 100, 255) # Pink (x3)
            label = "x3"
        elif self.type_name == 'fast':
            color = (255, 120, 0)   # Oranye (S+)
            label = "S+"
        elif self.type_name == 'expand':
            color = (200, 0, 255)   # Ungu (W+)
            label = "W+"
        elif self.type_name == 'slow':
            color = (0, 200, 255)   # Biru (S-)
            label = "S-"
        elif self.type_name == 'shrink':
            color = (255, 40, 80)   # Merah (W-)
            label = "W-"
        else:
            color = (0, 255, 100)   # Hijau (+L)
            label = "+L"

        rect = (self.posx, self.posy, self.width, self.height)
        draw_glowing_rect(screen, color, rect, border_radius=6)
        
        txt = font.render(label, True, (255, 255, 255))
        screen.blit(txt, (self.posx + 5, self.posy + 5))

    def getRect(self):
        return pygame.Rect(self.posx, self.posy, self.width, self.height)


# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, color, xFac=1, yFac=-1):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.base_speed = speed
        self.speed = speed
        self.color = color
        self.xFac = xFac
        self.yFac = yFac

    def display(self):
        draw_glowing_circle(screen, self.color, (int(self.posx), int(self.posy)), self.radius)

    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Dinding pembatas bola disesuaikan dengan garis tepi dalam (35px)
        if self.posx - self.radius <= 35:
            self.posx = 35 + self.radius
            self.xFac *= -1
        elif self.posx + self.radius >= WIDTH - 35:
            self.posx = WIDTH - 35 - self.radius
            self.xFac *= -1

        if self.posy - self.radius <= 70:  # Batas atas di bawah HUD/garis
            self.posy = 70 + self.radius
            self.yFac *= -1

        if self.posy >= HEIGHT:
            return True  # Bola jatuh

        return False

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.speed = self.base_speed
        self.xFac, self.yFac = 1, -1

    def hit(self):
        self.yFac *= -1

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)


# Helper Functions
def collisionChecker(rect1, rect2):
    return rect1.colliderect(rect2)


# Fungsi populate blocks dengan margin kanan & kiri yang lebih aman (tidak menempel garis)
def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []
    start_x = 50   # Jarak aman dari sisi kiri bingkai
    end_x = WIDTH - 50  # Jarak aman dari sisi kanan bingkai
    start_y = 90   # Jarak dari bawah HUD
    end_y = int(HEIGHT * 0.48)
    
    # Loop menggunakan range yang diberi batasan tegas agar tidak melewati end_x
    for i in range(start_x, end_x - blockWidth + 1, blockWidth + horizontalGap):
        for j in range(start_y, end_y, blockHeight + verticalGap):
            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight, random.choice(BLOCK_COLORS))
            )
    return listOfBlocks


def gameOver():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


# Game Manager
def main():
    running = True
    lives = 3
    score = 0

    striker = Striker(WIDTH // 2 - 50, HEIGHT - 40, 100, 15, 8, STRIKER_COLOR)
    strikerXFac = 0

    balls = [Ball(WIDTH // 2, HEIGHT // 2, 8, 4, BALL_COLOR)]

    # Ukuran balok dan jarak renggang disesuaikan agar pas di tengah
    blockWidth, blockHeight = 48, 18
    horizontalGap, verticalGap = 12, 10

    listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
    listOfPowerUps = []

    # Game loop
    while running:
        screen.fill(BG_COLOR)

        # Menggambar Bingkai/Border Area Bermain di dalam Jendela Aplikasi (Margin 30px dari tepi layar)
        pygame.draw.rect(screen, (30, 30, 50), (30, 70, WIDTH - 60, HEIGHT - 90), 2, border_radius=6)
        # Garis pembatas HUD bagian atas
        pygame.draw.line(screen, (30, 30, 50), (0, 60), (WIDTH, 60), 2)

        # Render Score, Lives & Total Bola Teks
        scoreText = font.render(f"SCORE : {score}", True, TEXT_COLOR)
        livesText = font.render(f"LIVES : {lives}", True, TEXT_COLOR)
        ballsText = font.render(f"BALLS : {len(balls)}", True, TEXT_COLOR)
        
        screen.blit(scoreText, (30, 20))
        screen.blit(ballsText, (WIDTH // 2 - 45, 20))
        screen.blit(livesText, (WIDTH - 120, 20))

        # Repopulate blocks if empty
        if not listOfBlocks:
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

        if lives <= 0:
            overSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overSurf.fill((8, 8, 14, 200))
            screen.blit(overSurf, (0, 0))

            overText = font.render("GAME OVER - Tekan SPASI untuk main lagi", True, (255, 0, 127))
            screen.blit(overText, (WIDTH // 2 - 170, HEIGHT // 2))
            pygame.display.update()
            
            running = gameOver()
            if running:
                lives = 3
                score = 0
                striker.reset_size()
                listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
                listOfPowerUps.clear()
                balls = [Ball(WIDTH // 2, HEIGHT // 2, 8, 4, BALL_COLOR)]
            else:
                break

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Update & Collision untuk setiap bola
        for ball in balls[:]:
            if collisionChecker(striker.getRect(), ball.getRect()):
                ball.hit()

            for block in listOfBlocks[:]:
                if collisionChecker(block.getRect(), ball.getRect()):
                    ball.hit()
                    block.hit()
                    score += 10

                    if block.getHealth() <= 0:
                        listOfBlocks.remove(block)
                        # Peluang skill muncul 15% (0.15)
                        if random.random() < 0.15:
                            p_type = random.choice(['multi', 'triple', 'fast', 'expand', 'slow', 'shrink', 'life'])
                            listOfPowerUps.append(PowerUp(block.posx + block.width // 2, block.posy, p_type))

            lifeLost = ball.update()
            if lifeLost:
                balls.remove(ball)

        if len(balls) == 0:
            lives -= 1
            striker.reset_size()
            balls.append(Ball(WIDTH // 2, HEIGHT // 2, 8, 4, BALL_COLOR))

        # Update Power-Ups & Efek Skill
        for pUp in listOfPowerUps[:]:
            pUp.update()
            if collisionChecker(striker.getRect(), pUp.getRect()):
                if pUp.type_name == 'multi':
                    new_balls = []
                    for b in balls:
                        new_balls.append(Ball(b.posx, b.posy, b.radius, b.speed, b.color, xFac=1, yFac=-1))
                        new_balls.append(Ball(b.posx, b.posy, b.radius, b.speed, b.color, xFac=-1, yFac=-1))
                    balls.extend(new_balls)
                
                elif pUp.type_name == 'triple':
                    new_balls = []
                    for b in balls:
                        new_balls.append(Ball(b.posx, b.posy, b.radius, b.speed, b.color, xFac=1, yFac=-1))
                        new_balls.append(Ball(b.posx, b.posy, b.radius, b.speed, b.color, xFac=0.5, yFac=-1))
                        new_balls.append(Ball(b.posx, b.posy, b.radius, b.speed, b.color, xFac=-1, yFac=-1))
                    balls.extend(new_balls)
                
                elif pUp.type_name == 'fast':
                    for b in balls:
                        b.speed += 1.5
                
                elif pUp.type_name == 'expand':
                    striker.width = min(220, striker.width + 40)

                elif pUp.type_name == 'slow':
                    for b.speed in balls: # Perbaikan kecil pada iterasi kecepatan bola
                        pass
                    for b in balls:
                        b.speed = max(2.0, b.speed - 1.5)

                elif pUp.type_name == 'shrink':
                    striker.width = max(50, striker.width - 30)

                elif pUp.type_name == 'life':
                    lives += 1

                listOfPowerUps.remove(pUp)
            elif pUp.posy > HEIGHT:
                listOfPowerUps.remove(pUp)

        striker.update(strikerXFac)

        # Display Elements
        striker.display()
        
        for ball in balls:
            ball.display()

        for block in listOfBlocks:
            block.display()

        for pUp in listOfPowerUps:
            pUp.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
    