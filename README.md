# AugmentCode-Free
AugmentCode无限免费续杯方案
<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>

# AugmentCode-Free (English)

**AugmentCode-Free** is a Python-based command-line toolkit designed to provide core functionalities for managing and cleaning up aspects of the Visual Studio Code local environment.

The initial version, "AugmentCode Unlimited Free Refill Plan," was created by the user. This project aims to build upon that foundation with robust, modular, and open-source code.

## Features

Currently, AugmentCode-Free offers the following key features:

1.  **VS Code Database Cleaning (`clean-db`)**:
    *   Identifies the VS Code `state.vscdb` SQLite database.
    *   Creates a backup of the database before making any changes.
    *   Connects to the database and removes specific entries based on a keyword (default: "augment"). This helps in clearing cached states or extension-related data.
    *   Includes error handling and attempts to restore from backup if issues occur.

2.  **VS Code Telemetry ID Modification (`modify-ids`)**:
    *   Locates the VS Code `storage.json` file, which stores telemetry and machine identifiers.
    *   Backs up the `storage.json` file.
    *   Generates new, randomized `machineId` (a 64-character hex string) and `devDeviceId` (a UUIDv4).
    *   Updates these IDs in the `storage.json` file. (Future enhancement: create these fields if they don't exist).
    *   Includes error handling.

3.  **Run All Tools (`run-all`)**:
    *   Sequentially executes all available tools (currently database cleaning and telemetry ID modification).

## Project Goals

*   Provide a free, open-source alternative for specific VS Code management tasks.
*   Offer modular and understandable Python code.
*   Ensure robust error handling and user-friendly command-line feedback.

## Installation

1.  **Prerequisites**:
    *   Python 3.8+
    *   `pip` (Python package installer)

2.  **Clone the repository**:
    ```bash
    git clone https://github.com/BasicProtein/AugmentCode-Free.git
    cd AugmentCode-Free
    ```

3.  **Create and activate a virtual environment (recommended)**:
    ```bash
    python -m venv .venv
    ```
    *   On Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies and the package**:
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```
    *Note: Installing in editable mode (`-e .`) allows you to use the CLI tools directly and reflects any code changes you make immediately.*

## Usage

Once installed, the tools are available via the `augment-tools` command-line interface:

*   **Clean VS Code Database**:
    ```bash
    augment-tools clean-db
    ```
    To use a custom keyword:
    ```bash
    augment-tools clean-db --keyword "your_keyword"
    ```

*   **Modify VS Code Telemetry IDs**:
    ```bash
    augment-tools modify-ids
    ```

*   **Run all available tools**:
    ```bash
    augment-tools run-all
    ```

*   **Get Help**:
    For general help:
    ```bash
    augment-tools --help
    ```
    For command-specific help (e.g., `clean-db`):
    ```bash
    augment-tools clean-db --help
    ```

## Project Structure
The core logic is organized within the `augment_tools_core` package:

`augment_tools_core/`:
*   `__init__.py`: Package initializer.
*   `cli.py`: Command-line interface logic using `click`.
*   `common_utils.py`: Shared utility functions (OS path detection, backups, ID generation, colored output).
*   `database_manager.py`: Handles VS Code SQLite database cleaning.
*   `telemetry_manager.py`: Manages modification of telemetry IDs in `storage.json`.

Project-level files:
*   `requirements.txt`: Lists project dependencies (e.g., `click`, `colorama`).
*   `setup.py`: Standard Python package setup script.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## Contributing
Contributions, issues, and feature requests are welcome! Please feel free to:

*   Open an issue for bugs or suggestions.
*   Fork the repository and submit a pull request.

## License
This project is open source. (Consider adding a specific license like MIT License here later by creating a `LICENSE` file).

**Disclaimer**: This project is for educational and utility purposes. Always ensure you understand what the tools do before running them, especially when they modify application files. Backups are created automatically, but caution is advised.

---

<a name="中文"></a>

# AugmentCode-Free (中文)

**AugmentCode-Free** 是一个基于 Python 的命令行工具包，旨在提供管理和清理 Visual Studio Code 本地环境的核心功能。

最初的版本“AugmentCode无限免费续杯方案”由用户创建。本项目旨在以该版本为基础，构建健壮、模块化且开源的代码。

## 主要功能

目前，AugmentCode-Free 提供以下关键功能：

1.  **VS Code 数据库清理 (`clean-db`)**:
    *   识别 VS Code 的 `state.vscdb` SQLite 数据库。
    *   在进行任何更改之前创建数据库的备份。
    *   连接到数据库，并根据关键字（默认为 "augment"）删除特定条目。这有助于清除缓存状态或与扩展相关的数据。
    *   包含错误处理机制，并在出现问题时尝试从备份中恢复。

2.  **VS Code 遥测 ID 修改 (`modify-ids`)**:
    *   定位存储遥测和机器标识符的 VS Code `storage.json` 文件。
    *   备份 `storage.json` 文件。
    *   生成新的、随机的 `machineId`（64 位十六进制字符串）和 `devDeviceId` (UUIDv4)。
    *   在 `storage.json` 文件中更新这些 ID。（未来增强：如果这些字段不存在，则创建它们）。
    *   包含错误处理机制。

3.  **运行所有工具 (`run-all`)**:
    *   按顺序执行所有可用的工具（当前是数据库清理和遥测 ID 修改）。

## 项目目标

*   为特定的 VS Code 管理任务提供一个免费的开源替代方案。
*   提供模块化且易于理解的 Python 代码。
*   确保强大的错误处理和用户友好的命令行反馈。

## 安装指南

1.  **先决条件**:
    *   Python 3.8 或更高版本
    *   `pip` (Python 包安装器)

2.  **克隆仓库**:
    ```bash
    git clone https://github.com/BasicProtein/AugmentCode-Free.git
    cd AugmentCode-Free
    ```

3.  **创建并激活虚拟环境 (推荐)**:
    ```bash
    python -m venv .venv
    ```
    *   Windows 系统:
        ```bash
        .\.venv\Scripts\activate
        ```
    *   macOS/Linux 系统:
        ```bash
        source .venv/bin/activate
        ```

4.  **安装依赖包及本项目**:
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```
    *注意：以可编辑模式 (`-e .`) 安装允许您直接使用命令行工具，并且您所做的任何代码更改都会立即生效。*

## 使用方法

安装完成后，可以通过 `augment-tools` 命令行界面使用这些工具：

*   **清理 VS Code 数据库**:
    ```bash
    augment-tools clean-db
    ```
    使用自定义关键字:
    ```bash
    augment-tools clean-db --keyword "您的关键字"
    ```

*   **修改 VS Code 遥测 ID**:
    ```bash
    augment-tools modify-ids
    ```

*   **运行所有可用工具**:
    ```bash
    augment-tools run-all
    ```

*   **获取帮助**:
    获取常规帮助:
    ```bash
    augment-tools --help
    ```
    获取特定命令的帮助 (例如 `clean-db`):
    ```bash
    augment-tools clean-db --help
    ```

## 项目结构
核心逻辑组织在 `augment_tools_core` 包内：

`augment_tools_core/`:
*   `__init__.py`: 包初始化文件。
*   `cli.py`: 使用 `click` 实现的命令行界面逻辑。
*   `common_utils.py`: 共享的实用函数（操作系统路径检测、备份、ID 生成、彩色输出）。
*   `database_manager.py`: 处理 VS Code SQLite 数据库清理。
*   `telemetry_manager.py`: 管理 `storage.json` 中遥测 ID 的修改。

项目级文件:
*   `requirements.txt`: 列出项目依赖 (例如 `click`, `colorama`)。
*   `setup.py`: 标准的 Python 包安装脚本。
*   `.gitignore`: 指定 Git 应忽略的、无需追踪的文件。

## 如何贡献
欢迎各种贡献、问题报告和功能请求！请随时：

*   针对错误或建议开启一个 issue。
*   Fork 本仓库并提交 Pull Request。

## 许可证
本项目为开源项目。（后续可以考虑通过创建一个 `LICENSE` 文件来添加特定的许可证，例如 MIT 许可证）。

**免责声明**: 本项目仅用于教育和实用目的。在运行这些工具之前，请务必了解它们的功能，尤其是在它们修改应用程序文件时。虽然会自动创建备份，但仍建议谨慎操作。