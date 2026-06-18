# hiwonder-lerobot（幻尔 LeRobot 入口）

[English](../README.md) | 中文

> **幻尔 LeRobot 机器人 AI 方案的官方入口仓库。**  
> 初次接触项目的用户从这里开始——包含产品介绍、支持机型、安装方式和第一个示例。

---

## 这是什么？

[幻尔 LeRobot](https://github.com/Hiwonder-official/LeRobot) 是幻尔推出的机器人 AI 全栈方案，专为幻尔机械臂优化，提供从硬件驱动到策略训练的完整工具链。  
主要包含：

- **HX-30HM** 30 kg 磁编码舵机驱动
- **SO-ARM101、SO-101、HopeJR、LeKiwi** 的开箱即用配置
- 完整的标定 → 遥操作 → 数据采集 → 训练 → 评估工作流

本仓库（`hiwonder-lerobot`）是**唯一入口**：以 [Hiwonder/LeRobot](https://github.com/Hiwonder-official/LeRobot) 为核心依赖，提供 `hiwonder-*` 命令行工具，并指向所有相关资源。

---

## 支持机型

| 机器人 | 类型 | 舵机 | 自由度 |
|---|---|---|---|
| **SO-ARM101** | 6-DOF 机械臂 | 幻尔 HX-30HM（30 kg） | 6 |
| **SO-101** | 6-DOF 机械臂 | Feetech STS 系列 | 6 |
| **HopeJR** | 人形机械臂 | Feetech STS 系列 | 6 |
| **LeKiwi** | 移动平台 | Feetech STS 系列 | — |

---

## 安装

### 环境要求

- Python **3.10 – 3.12**
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip
- USB 连接的幻尔机械臂（硬件运行时需要）

### 克隆并安装（SO-ARM101 / SO-101）

```bash
git clone https://github.com/Hiwonder-official/-hiwonder-lerobot.git
cd hiwonder-lerobot

# 推荐使用 uv
uv pip install -e ".[so-arm101]"

# 或使用 pip
pip install -e ".[so-arm101]"
```

### 其他机型

```bash
pip install -e ".[hopejr]"    # HopeJR 人形臂
pip install -e ".[lekiwi]"    # LeKiwi 移动平台
pip install -e ".[all]"       # 全部安装
```

### 验证安装

```bash
hiwonder-find-port   # 列出串口，确认驱动正常
```

---

## 快速开始

### 第 1 步 — 查找串口

```bash
hiwonder-find-port
# 示例输出：
#   /dev/ttyUSB0   (Linux)
#   COM3           (Windows)
```

### 第 2 步 — 标定机械臂

```bash
hiwonder-calibrate \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0
```

按屏幕提示依次移动每个关节至极限位置，标定数据保存至 `~/.cache/huggingface/lerobot/calibration/`。

### 第 3 步 — 遥操作（主手 → 从手）

```bash
hiwonder-teleoperate \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0
```

### 第 4 步 — 采集数据集

```bash
hiwonder-record \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0 \
  --repo-id YOUR_HF_USERNAME/my_first_dataset \
  --num-episodes 10 \
  --single-task "拿起红色积木"
```

### 第 5 步 — 训练策略（ACT）

```bash
hiwonder-train \
  --policy-path lerobot/configs/policy/act_so_arm101.yaml \
  --dataset-repo-id YOUR_HF_USERNAME/my_first_dataset \
  --output-dir outputs/train/act_so_arm101
```

### 第 6 步 — 评估

```bash
hiwonder-eval \
  --policy-path outputs/train/act_so_arm101/checkpoints/last/pretrained_model \
  --robot-path lerobot/configs/robot/so_arm101.yaml \
  --robot-overrides '~motors' port=/dev/ttyUSB0
```

---

## 资源链接

| | |
|---|---|
| 幻尔官网 | https://www.hiwonder.com/ |
| SO-ARM101 产品页 | https://www.hiwonder.com/products/lerobot-so-101 |
| 完整文档 | https://www.hiwonder.com.cn/store/learn/185.html |
| 视频教程 | https://www.youtube.com/watch?v=oitT8geMat0 |
| LeRobot 幻尔分支 | https://github.com/Hiwonder-official/LeRobot |
| 上游 LeRobot | https://github.com/huggingface/lerobot |
| 技术支持邮箱 | support@hiwonder.com |

---

## 命令行参考

所有命令均支持 `--help` 查看完整参数。

| 命令 | 功能 |
|---|---|
| `hiwonder-find-port` | 检测机械臂 USB 串口 |
| `hiwonder-setup-motors` | 写入舵机 ID 与波特率 |
| `hiwonder-calibrate` | 逐关节行程标定 |
| `hiwonder-teleoperate` | 主从实时遥操作 |
| `hiwonder-record` | 示教数据集采集 |
| `hiwonder-replay` | 回放已录制片段 |
| `hiwonder-train` | 用数据集训练策略 |
| `hiwonder-eval` | 在真实机械臂上评估策略 |

---

## 许可证

本项目采用 **MIT 许可证**，详见 [LICENSE](../LICENSE)。  
底层 [LeRobot](https://github.com/huggingface/lerobot) 框架采用 Apache 2.0 许可证。
