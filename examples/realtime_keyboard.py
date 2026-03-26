import pygame
import math
from minisim.control.command import ControlCommand
from minisim.simulator import Simulator
from minisim.ship import Ship



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
            kship.state.speed += 0.05
        if keys[pygame.K_DOWN]:
            kship.state.speed -= 0.05

        rudder_text = font.render(f"rudder = {kcommand.rudder:.2f}", True, (255,255,255))
        speed_text = font.render(f"speed = {kship.state.speed:.2f}", True, (255,255,255))
        screen.blit(rudder_text, (20, 20))
        screen.blit(speed_text, (20, 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()