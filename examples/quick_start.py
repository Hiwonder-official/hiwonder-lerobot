"""Minimal example: connect to SO-ARM101 and read joint positions.

Prerequisites:
    git clone https://github.com/Hiwonder-official/LeRobot.git
    cd LeRobot && pip install -e ".[hiwonder]"
"""

from lerobot.robots.so_arm101 import SO_ARM101Config, SO_ARM101Robot

# Update the port to match your system (run `hiwonder-find-port` to discover it).
PORT = "/dev/ttyUSB0"  # Linux — use e.g. "COM3" on Windows


def main() -> None:
    config = SO_ARM101Config(port=PORT)
    robot = SO_ARM101Robot(config)

    robot.connect()
    print("Connected to SO-ARM101")

    obs = robot.get_observation()
    print("Joint positions:", obs)

    robot.disconnect()
    print("Done.")


if __name__ == "__main__":
    main()
