import pygame
import math
from minisim.control.command import ControlCommand
from minisim.simulator import Simulator
from minisim.ship import Ship

WIDTH = 800
HEIGHT = 600
PIX_PER_METER = 20


def world_to_screen(x, y):
    
    sx =  WIDTH // 2 + x * PIX_PER_METER 
    sy =  HEIGHT // 2 + y * PIX_PER_METER 

    return sx, sy


def main():

    kcommand = ControlCommand()
    kship = Ship()
    ksim = Simulator(kship)
    

    kcommand.rudder = 0.0
    kship.state.speed = 0.0


    pygame.init()

    font = pygame.font.SysFont(None, 28)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000,700))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
        screen.fill((30,30,30))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            kcommand.rudder -= 0.05
        if keys[pygame.K_RIGHT]:
            kcommand.rudder += 0.05
        if keys[pygame.K_UP]:
            kcommand.speed += 0.05
        if keys[pygame.K_DOWN]:
            kcommand.speed -= 0.05

            
        ksim.step(0.1, kcommand)

        cam_x = kship.state.x
        cam_y = kship.state.y
        rel_x = cam_x - kship.state.x
        rel_y = cam_y - kship.state.y
        cx, cy = world_to_screen(rel_x, rel_y)
        front = (cx + 25 * math.cos(kship.state.heading), cy + 25 * math.sin(kship.state.heading))
        left = (cx - 12  * math.cos(kship.state.heading + 5.5), cy + 12 * math.cos(kship.state.heading + 5.5))
        right = (cx - 12  * math.cos(kship.state.heading - 5.5), cy + 12 * math.cos(kship.state.heading - 5.5))

        pygame.draw.polygon(screen, (100, 200, 255), [front, left, right], 3)
        pygame.draw.line(screen, (255, 255, 255), (cx, cy),(cx, cy), 4)

        rudder_text = font.render(f"rudder = {kcommand.rudder:.2f}", True, (255,255,255))
        speed_text = font.render(f"speed = {kcommand.speed:.2f}", True, (255,255,255))
        screen.blit(rudder_text, (20, 20))
        screen.blit(speed_text, (20, 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()