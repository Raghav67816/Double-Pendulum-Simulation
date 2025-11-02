import pygame
from math import radians, sin, cos

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Double Pendulum Simulation By Cooper")

G = 9.8

class DoublePendulum:
    def __init__(self):
        self.origin_x = 400
        self.origin_y = 100

        self.length_rod_1 = 120
        self.length_rod_2 = 120

        self.mass_bob_a = 10
        self.mass_bob_b = 10

        self.theta_1 = radians(120)
        self.theta_2 = radians(120)

        self.omega_a = 0
        self.omega_b = 0
        self.prev_cords = []

        self.update_cords()

    def update_cords(self):
        self.x1 = self.origin_x + self.length_rod_1 * sin(self.theta_1)
        self.y1 = self.origin_y + self.length_rod_1 * cos(self.theta_1)
        self.x2 = self.x1 + self.length_rod_2 * sin(self.theta_2)
        self.y2 = self.y1 + self.length_rod_2 * cos(self.theta_2)

    def get_cords(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def calc_ang_acc(self):
        theta_change = self.theta_2 - self.theta_1
        d1 = (self.mass_bob_a + self.mass_bob_b) * self.length_rod_1 - self.mass_bob_b * self.length_rod_1 * (cos(theta_change))**2.0
        d2 = (self.length_rod_2 / self.length_rod_1) * d1

        ang_acc_a = (
            self.mass_bob_b * self.length_rod_2 * (self.omega_b**2) * sin(theta_change) * cos(theta_change)
            + self.mass_bob_b * G * sin(self.theta_2) * cos(theta_change)
            + self.mass_bob_b * self.length_rod_2 * (self.omega_b**2) * sin(theta_change)
            - (self.mass_bob_a + self.mass_bob_b) * G * sin(self.theta_1)
        ) / d1

        ang_acc_b = (
            -self.mass_bob_b * self.length_rod_2 * (self.omega_b**2) * sin(theta_change) * cos(theta_change)
            + (self.mass_bob_a + self.mass_bob_b) * G * sin(self.theta_1) * cos(theta_change)
            - (self.mass_bob_a + self.mass_bob_b) * self.length_rod_1 * (self.omega_a**2) * sin(theta_change)
            - (self.mass_bob_a + self.mass_bob_b) * G * sin(self.theta_2)
        ) / d2

        return ang_acc_a, ang_acc_b

    def step(self, dt=0.01):
        alpha_1, alpha_2 = self.calc_ang_acc()

        self.omega_a += alpha_1 * dt
        self.omega_b += alpha_2 * dt

        self.theta_1 += self.omega_a * dt
        self.theta_2 += self.omega_b * dt

        self.update_cords()

        self.prev_cords.insert(0, (self.x2, self.y2))


dp = DoublePendulum()

running = True
clock = pygame.time.Clock()
clock.tick(60)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dp.step(0.05)

    screen.fill((0, 0, 0))
    cords = dp.get_cords()

    pygame.draw.circle(screen, (0, 0, 255), (dp.origin_x, dp.origin_y), 10)
    pygame.draw.line(screen, (255, 255, 255), (dp.origin_x, dp.origin_y), cords[0], 3)
    pygame.draw.circle(screen, (255, 0, 0), cords[0], 10)
    pygame.draw.line(screen, (255, 255, 255), cords[0], cords[1], 3)
    pygame.draw.circle(screen, (0, 255, 0), cords[1], 10)
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (dp.x2, dp.y2), 1, 0
    )
    if len(dp.prev_cords) > 1:
        pygame.draw.aalines(
            screen, (0, 255, 0), False, dp.prev_cords
        )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
