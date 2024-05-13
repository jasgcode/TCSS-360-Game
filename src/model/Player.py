import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 0, 0))  # Player color (red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.score = 0
        self.lives = 3

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def move_up(self):
        self.move(0, -1)

    def move_down(self):
        self.move(0, 1)

    def collision(self, walls):
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for wall in collisions:
            if self.rect.right > wall.rect.left and self.rect.left < wall.rect.left:
                self.rect.right = wall.rect.left
            if self.rect.left < wall.rect.right and self.rect.right > wall.rect.right:
                self.rect.left = wall.rect.right
            if self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                self.rect.bottom = wall.rect.top
            if self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                self.rect.top = wall.rect.bottom

    def update(self, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_UP]:
            self.move_up()
        if keys[pygame.K_DOWN]:
            self.move_down()

        self.collision(walls)

    def increase_score(self, points):
        self.score += points

    def decrease_lives(self):
        self.lives -= 1

    def is_alive(self):
        return self.lives > 0