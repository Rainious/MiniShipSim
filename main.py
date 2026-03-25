from minisim.ship import Ship

def main():
    ship = Ship()

    ship.state.speed = 2.0
    ship.state.rudder = 0.5

    for i in range(20):
        ship.step(0.1)
        print("step", i)
        print("x = ", ship.state.x)
        print("y = ", ship.state.y)
        print("heading = ", ship.state.heading)
        print("turn_rate = ", ship.state.turn_rate)
        print("Ipad lg2 test.")


if __name__ == "__main__":
    main()