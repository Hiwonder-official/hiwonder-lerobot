

## About Hiwonder-Lerobot

Built on top of LeRobot, [Hiwonder LeRobot](https://github.com/Hiwonder-official/LeRobot) is an open-source AI framework that covers the entire pipeline from data collection and model training to deployment. 

At Hiwonder, we've spent years designing and manufacturing robotics hardware. Along the way, we realized that great hardware is only the starting point. The real challenge is helping developers efficiently collect data, train policies, and deploy models to physical robots. That's why we built the LeRobot framework with Hiwonder hardware to deliver this out-of-the-box open-source AI framework.

It provides:

- Integrated drivers for HX-30HM 30 kg magnetic encoder servos.
- Out-of-the-box configurations for **SO-ARM101**, **SO-101**, **HopeJR**, and **LeKiwi**
- A comprehensive workflow spanning calibration, teleoperation, data collection, training, and evaluation.

This repository (`hiwonder-lerobot`) is the **single entry point**: it installs [Hiwonder/LeRobot](https://github.com/Hiwonder-official/LeRobot) as its core dependency, exposes `hiwonder-*` CLI commands, and points you to every relevant resource.

Our goal is to help robotics developers deploy algorithms on physical robotic arms faster and at lower cost.

---

## Supported Hardware

| Robot | Type | Motor | DOF |
|---|---|---|---|
| **SO-ARM101** | 6-DOF robotic arm | Hiwonder HX-30HM (30 kg) | 6 |
| **SO-101** | 6-DOF robotic arm | Feetech STS series | 6 |
| **HopeJR** | Humanoid arm | Feetech STS series | 6 |
| **LeKiwi** | Mobile platform | Feetech STS series | — |

> **SO-ARM101** is the primary Hiwonder platform — high torque, zero backlash magnetic encoders, dual-camera vision.

---

## Repository Layout

```
hiwonder-lerobot/          ← this repo (entry point, docs, install)
├── src/hiwonder_lerobot/
│   ├── __init__.py
│   └── cli.py             ← hiwonder-* CLI commands
├── examples/
│   └── quick_start.py     ← first script to run
├── docs/
│   └── README_cn.md
├── pyproject.toml
└── LICENSE

LeRobot/                   ← Hiwonder's LeRobot fork (installed as dependency)
  https://github.com/Hiwonder-official/LeRobot
```

---

## Installation

### Prerequisites

- Python **3.10 – 3.12**
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A USB-connected Hiwonder arm (for hardware runs)

### 1 — Clone Hiwonder LeRobot and install (SO-ARM101 / SO-101)

```bash
git clone https://github.com/Hiwonder-official/LeRobot.git
cd LeRobot

# with uv (recommended — resolves the torch/lerobot dependency tree faster)
uv pip install -e ".[hiwonder]"

# or with pip
pip install -e ".[hiwonder]"
```

### 2 — Other arms

```bash
pip install -e ".[hopejr]"    # HopeJR humanoid arm
pip install -e ".[lekiwi]"    # LeKiwi mobile platform
pip install -e ".[all]"       # everything
```

### 3 — Verify

```bash
hiwonder-find-port          # lists serial ports; confirms drivers are installed
```

---

## Quick Start

### Step 1 — Find the serial port

```bash
hiwonder-find-port
# Example output:
#   /dev/ttyUSB0   (Linux)
#   COM3           (Windows)
```

### Step 2 — Calibrate the arm

```bash
hiwonder-calibrate \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0
```

Follow the on-screen prompts to move each joint through its full range.  
Calibration data is saved to `~/.cache/huggingface/lerobot/calibration/`.

### Step 3 — Teleoperate (leader → follower)

```bash
hiwonder-teleoperate \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0
```

### Step 4 — Record a dataset

```bash
hiwonder-record \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0 \
  --repo-id YOUR_HF_USERNAME/my_first_dataset \
  --num-episodes 10 \
  --single-task "Pick up the red block"
```

### Step 5 — Train a policy (ACT)

```bash
hiwonder-train \
  --policy-path lerobot/configs/policy/act_so_arm101.yaml \
  --dataset-repo-id YOUR_HF_USERNAME/my_first_dataset \
  --output-dir outputs/train/act_so_arm101
```

### Step 6 — Evaluate

```bash
hiwonder-eval \
  --policy-path outputs/train/act_so_arm101/checkpoints/last/pretrained_model \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0
```

### Minimal Python example

```python
# examples/quick_start.py
from lerobot.robots.so_arm101 import SO_ARM101Config, SO_ARM101Robot

config = SO_ARM101Config(port="/dev/ttyUSB0")
robot = SO_ARM101Robot(config)

robot.connect()
print("Joint positions:", robot.get_observation())
robot.disconnect()
```

Run it:

```bash
python examples/quick_start.py
```

---

## Resources

| | |
|---|---|
| Hiwonder official website | https://www.hiwonder.com/ |
| Product page (SO-ARM101) | https://www.hiwonder.com/products/lerobot-so-101 |
| Full documentation | https://www.hiwonder.com.cn/store/learn/185.html |
| Video tutorial | https://www.youtube.com/watch?v=oitT8geMat0 |
| LeRobot fork source | https://github.com/Hiwonder-official/LeRobot |
| Upstream LeRobot (HuggingFace) | https://github.com/huggingface/lerobot |
| Hugging Face Hub (datasets & models) | https://huggingface.co/lerobot |
| Technical support | support@hiwonder.com |

---

## CLI Reference

All commands accept `--help` for full options.

| Command | What it does |
|---|---|
| `hiwonder-find-port` | Detect the USB serial port of the arm |
| `hiwonder-setup-motors` | Write motor IDs and baud rate |
| `hiwonder-calibrate` | Record per-joint min/max calibration |
| `hiwonder-teleoperate` | Real-time leader → follower control |
| `hiwonder-record` | Collect a demonstration dataset |
| `hiwonder-replay` | Replay a recorded episode |
| `hiwonder-train` | Train a policy on a recorded dataset |
| `hiwonder-eval` | Evaluate a trained policy on the real arm |

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

The underlying [Hiwonder LeRobot](https://github.com/Hiwonder-official/LeRobot) library is licensed under the Apache 2.0 License.
