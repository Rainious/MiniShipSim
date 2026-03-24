from minisim.ship import Ship

def main():
    ship = Ship()

    ship.state.speed = 2.0
    ship.state.heading = 0.0
    ship.state.turn_rate = 0.5

    for i in range(5):
        ship.step(0.1)
        print("step", i)
        print("x = ", ship.state.x)
        print("y = ", ship.state.y)
        print("heading = ", ship.state.heading)


if __name__ == "__main__":
    main()