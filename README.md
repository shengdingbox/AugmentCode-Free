# AugmentCode-Free
AugmentCode无限免费续杯方案；新账号可获得600次免费的Claude Sonnet 4调用
<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>

# AugmentCode-Free (English)

**AugmentCode-Free** is a Python-based toolkit, now featuring a modern **Graphical User Interface (GUI)** alongside its command-line interface. It's designed to provide maintenance and tweaking utilities for VS Code, helping users manage aspects like telemetry and local cache.

## Features

### Core Functionality (Available in CLI & GUI)
-   **VS Code Database Cleaning**: Cleans specific entries from VS Code's local databases.
-   **VS Code Telemetry ID Modification**: Helps in resetting or changing telemetry identifiers stored by VS Code.

### New GUI Features
-   **Intuitive Interface**: A user-friendly graphical alternative to command-line operations.
-   **One-Click Operations**: Easily perform tasks like modifying VS Code telemetry IDs and cleaning VS Code databases with a single click.
-   **Process Management**: Automatically detects and offers to close running VS Code instances to ensure operations proceed smoothly.
-   **User Feedback**: Provides clear confirmation dialogs and status messages for all operations.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/BasicProtein/AugmentCode-Free.git](https://github.com/BasicProtein/AugmentCode-Free.git)
    cd AugmentCode-Free
    ```
2.  **Install dependencies (if any specified in `requirements.txt` or `setup.py`):**
    ```bash
    pip install .
    # or
    # pip install -r requirements.txt
    ```

## Usage

You can use AugmentCode-Free in two ways:

### 1. Graphical User Interface (GUI) - Recommended
The GUI provides an easy-to-use interface for all features.

-   **Directly (from project root):**
    ```bash
    python main.py
    ```
    *(As the author kindly noted: "以后直接启动main.py就行喵" - From now on, just run main.py!)*

-   **If installed via pip (as `augment-tools-gui`):**
    ```bash
    augment-tools-gui
    ```

### 2. Command-Line Interface (CLI)
For users who prefer the command line or need to script operations.

-   **If installed via pip (as `augment-tools`):**
    ```bash
    augment-tools --help
    ```
    (Follow on-screen instructions for specific commands like `clean-db` or `modify-telemetry`)

-   **Directly (for development/advanced use, from project root):**
    Refer to `augment_tools_core/cli.py` for direct script execution details if needed.

## Disclaimer
Use these tools at your own risk. Always back up important data before running maintenance functions, especially when they modify application files. While backups might be created automatically by some functions, caution is advised.

---

<a name="中文"></a>

# AugmentCode-Free (中文)

**AugmentCode-Free** 是一个基于 Python 的工具包，现已配备现代化的**图形用户界面 (GUI)** 以及原有的命令行界面。它旨在为 VS Code 提供维护和调整实用程序，帮助用户管理遥测数据和本地缓存等方面。

## 功能特性

###核心功能 (命令行及GUI均可用)
-   **VS Code 数据库清理**: 清理 VS Code 本地数据库中的特定条目。
-   **VS Code 遥测ID修改**: 帮助重置或更改 VS Code 存储的遥测标识符。

### 全新 GUI 特性
-   **直观界面**: 提供用户友好的图形操作界面，作为命令行的替代选择。
-   **一键式操作**: 通过单击即可轻松执行修改 VS Code 遥测ID、清理 VS Code 数据库等任务。
-   **进程管理**: 自动检测并提示关闭正在运行的 VS Code 实例，以确保操作顺利进行。
-   **用户反馈**: 为所有操作提供清晰的确认对话框和状态消息。

## 安装

1.  **克隆仓库:**
    ```bash
    git clone [https://github.com/BasicProtein/AugmentCode-Free.git](https://github.com/BasicProtein/AugmentCode-Free.git)
    cd AugmentCode-Free
    ```
2.  **安装依赖 (如果 `requirements.txt` 或 `setup.py` 中有指定):**
    ```bash
    pip install .
    # 或者
    # pip install -r requirements.txt
    ```

## 使用方法

您可以通过两种方式使用 AugmentCode-Free：

### 1. 图形用户界面 (GUI) - 推荐
GUI 为所有功能提供了简单易用的操作界面。

-   **直接运行 (从项目根目录):**
    ```bash
    python main.py
    ```
    *(正如作者温馨提示："以后直接启动main.py就行喵"！)*

-   **如果通过 pip 安装 (作为 `augment-tools-gui`):**
    ```bash
    augment-tools-gui
    ```

### 2. 命令行界面 (CLI)
适用于喜欢命令行或需要编写脚本自动执行操作的用户。

-   **如果通过 pip 安装 (作为 `augment-tools`):**
    ```bash
    augment-tools --help
    ```
    (根据屏幕提示执行具体命令，如 `clean-db` 或 `modify-telemetry`)

-   **直接运行 (用于开发/高级用户, 从项目根目录):**
    如果需要，请参考 `augment_tools_core/cli.py` 了解直接执行脚本的详细信息。

## 免责声明
请自行承担使用这些工具的风险。在运行维护功能前，请务必备份重要数据，尤其是在它们修改应用程序文件时。虽然某些功能可能会自动创建备份，但仍建议谨慎操作。