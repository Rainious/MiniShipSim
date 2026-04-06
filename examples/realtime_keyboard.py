import pygame
import math
from minisim.control.command import ControlCommand
from minisim.simulator import Simulator
from minisim.ship import Ship

DT = 0.1
RUDDER_STEP = 0.005
RUDDER_RETURN_RATE = 0.0025
SPEED_STEP = 0.05
MAX_RUDDER = 0.3
MAX_SPEED = 2.0
WIDTH = 800
HEIGHT = 600
PIX_PER_METER = 20

kcommand = ControlCommand()
kship = Ship()
ksim = Simulator(kship)


def world_to_screen(x, y):
    
    sx =  WIDTH // 2 + x * PIX_PER_METER 
    sy =  HEIGHT // 2 + y * PIX_PER_METER 

    return sx, sy


def draw_ship_triangle(screen, cx, cy, heading, length=28, width=18, color=(100, 200, 255)):
    fx = math.cos(heading)
    fy = math.sin(heading)

    px = -fy
    py = fx

    tip = (cx + fx * (length * 0.5), cy + fy * (length * 0.5))
    base_center = (cx - fx * (length * 0.5), cy - fy * (length * 0.5))

    left = (base_center[0] + px * (width * 0.5), base_center[1] + py * (width * 0.5))
    right = (base_center[0] - px * (width * 0.5), base_center[1] - py * (width * 0.5))

    pygame.draw.polygon(screen, color, [tip, left, right])


def draw_trajectory(screen, history, cam_x, cam_y):
    points = []
    for item in history:
        relx = item["x"] - cam_x
        rely = item["y"] - cam_y
        tempx, tempy = world_to_screen(relx, rely)
        points.append((tempx,tempy))
    if len(points) >= 2:
        pygame.draw.lines(screen, (100, 255, 200), False, points, 3 )


def key_control():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        kcommand.rudder -= RUDDER_STEP
    else :
        if keys[pygame.K_RIGHT]:
            kcommand.rudder += RUDDER_STEP
        else:
            if kcommand.rudder > 0:
                kcommand.rudder -= RUDDER_RETURN_RATE
                if kcommand.rudder < 0:
                    kcommand.rudder = 0
            else:
                if kcommand.rudder < 0:
                    kcommand.rudder += RUDDER_RETURN_RATE
                    if kcommand.rudder > 0:
                        kcommand.rudder = 0
            
    
    if keys[pygame.K_UP]:
        kcommand.target_speed += SPEED_STEP
    else:
        if keys[pygame.K_DOWN]:
            kcommand.target_speed -= SPEED_STEP


    if kcommand.target_speed < 0 :
        kcommand.target_speed = 0
    if kcommand.target_speed > MAX_SPEED:
        kcommand.target_speed = MAX_SPEED
    if kcommand.rudder < - MAX_RUDDER:
        kcommand.rudder = - MAX_RUDDER
    if kcommand.rudder > MAX_RUDDER:
        kcommand.rudder = MAX_RUDDER
        



def main():


    kcommand.rudder = 0.0
    kcommand.target_speed = 0.0


    pygame.init()

    font = pygame.font.SysFont(None, 28)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
        screen.fill((30,30,30))

        key_control()

            
        ksim.step(DT, kcommand)

        cam_x = kship.state.x
        cam_y = kship.state.y
        rel_x = cam_x - kship.state.x
        rel_y = cam_y - kship.state.y
        cx, cy = world_to_screen(rel_x, rel_y)
        draw_ship_triangle(screen, cx, cy, kship.state.heading)
        pygame.draw.line(screen, (255, 255, 255), (cx, cy),(cx, cy), 4)
        draw_trajectory(screen, ksim.history, cam_x, cam_y)

        rudder_text = font.render(f"rudder = {kcommand.rudder:.2f}", True, (255,255,255))
        speed_text = font.render(f"speed = {kship.state.speed:.2f}", True, (255,255,255))
        t_speed_text = font.render(f"target_speed = {kcommand.target_speed:.2f}", True, (255,255,255))
        screen.blit(rudder_text, (20, 20))
        screen.blit(speed_text, (20, 50))
        screen.blit(t_speed_text, (20, 80))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()