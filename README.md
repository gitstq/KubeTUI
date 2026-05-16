<div align="center">

# 🚀 KubeTUI

**A Modern, Fast, and Intuitive TUI for Kubernetes Cluster Management**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/KubeTUI?style=social)](https://github.com/gitstq/KubeTUI/stargazers)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

<img src="https://via.placeholder.com/800x400?text=KubeTUI+Screenshot" alt="KubeTUI Screenshot" width="80%">

</div>

---

<a name="english"></a>
## 📖 English

### 🎉 Introduction

**KubeTUI** is a modern Terminal User Interface (TUI) tool designed for Kubernetes cluster management. It provides an intuitive, keyboard-driven interface for monitoring and managing your K8s clusters efficiently.

**Why KubeTUI?**
- 🔥 **Fast & Lightweight**: Built with Python and Textual, starts in milliseconds
- 🎨 **Beautiful TUI**: Modern, colorful interface with zebra-striped tables
- ⌨️ **Keyboard-First**: Efficient shortcuts for all operations
- 🔌 **Zero Config**: Works out of the box with your existing kubeconfig
- 📦 **Easy Install**: Single pip command installation

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📊 **Real-time Monitoring** | View Pods, Deployments, Services, Nodes with live updates |
| 📝 **Log Viewer** | Stream pod logs with follow mode and copy support |
| 🔄 **Resource Operations** | Delete pods, scale deployments, restart workloads |
| 🎯 **Context Switching** | Quickly switch between Kubernetes contexts |
| 📁 **Namespace Navigation** | Browse and select namespaces with ease |
| 🔍 **Resource Search** | Filter and find resources quickly |
| ⌨️ **Keyboard Shortcuts** | Efficient navigation without mouse |

### 🚀 Quick Start

#### Prerequisites
- Python 3.10 or higher
- Kubernetes cluster with kubeconfig configured
- kubectl installed and configured

#### Installation

```bash
# Install from PyPI
pip install kubetui

# Or install from source
git clone https://github.com/gitstq/KubeTUI.git
cd KubeTUI
pip install -e .
```

#### Run

```bash
# Start KubeTUI
kubetui

# Or run directly
python -m kubetui
```

### 📖 Usage Guide

#### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit |
| `r` | Refresh data |
| `n` | Select namespace |
| `c` | Select context |
| `l` | View pod logs |
| `d` | Describe resource |
| `?` | Show help |
| `1-4` | Switch tabs (Pods, Deployments, Services, Nodes) |
| `↑/↓` | Navigate rows |
| `Enter` | Select item |

#### Tabs Overview

1. **Pods Tab** (`1`): View all pods with status, ready count, restarts, age, IP, and node
2. **Deployments Tab** (`2`): Monitor deployments with replica status
3. **Services Tab** (`3`): View services with type, cluster IP, and ports
4. **Nodes Tab** (`4`): Check node status, roles, and versions

### 💡 Design Philosophy

KubeTUI is built with these principles:
- **Simplicity**: Minimal dependencies, easy to understand codebase
- **Performance**: Async operations, efficient data fetching
- **Extensibility**: Modular architecture for easy feature additions
- **User Experience**: Intuitive interface inspired by htop and k9s

### 📦 Building & Deployment

```bash
# Build package
pip install build
python -m build

# Run tests
pytest

# Type checking
mypy src/kubetui

# Linting
ruff check src/kubetui
```

### 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 📖 简体中文

### 🎉 项目介绍

**KubeTUI** 是一款现代化的终端用户界面（TUI）工具，专为 Kubernetes 集群管理而设计。它提供了直观、键盘驱动的界面，让您高效地监控和管理 K8s 集群。

**为什么选择 KubeTUI？**
- 🔥 **快速轻量**：基于 Python 和 Textual 构建，毫秒级启动
- 🎨 **美观界面**：现代化的彩色界面，带有斑马纹表格
- ⌨️ **键盘优先**：所有操作都可通过快捷键完成
- 🔌 **零配置**：直接使用现有的 kubeconfig，开箱即用
- 📦 **简单安装**：一条 pip 命令即可安装

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📊 **实时监控** | 查看 Pods、Deployments、Services、Nodes，实时更新 |
| 📝 **日志查看** | 流式查看 Pod 日志，支持跟随模式和复制 |
| 🔄 **资源操作** | 删除 Pod、扩缩容 Deployment、重启工作负载 |
| 🎯 **上下文切换** | 快速切换 Kubernetes 上下文 |
| 📁 **命名空间导航** | 轻松浏览和选择命名空间 |
| 🔍 **资源搜索** | 快速过滤和查找资源 |
| ⌨️ **快捷键** | 无需鼠标，高效导航 |

### 🚀 快速开始

#### 环境要求
- Python 3.10 或更高版本
- 已配置 kubeconfig 的 Kubernetes 集群
- 已安装并配置 kubectl

#### 安装

```bash
# 从 PyPI 安装
pip install kubetui

# 或从源码安装
git clone https://github.com/gitstq/KubeTUI.git
cd KubeTUI
pip install -e .
```

#### 运行

```bash
# 启动 KubeTUI
kubetui

# 或直接运行
python -m kubetui
```

### 📖 使用指南

#### 快捷键

| 按键 | 操作 |
|------|------|
| `q` | 退出 |
| `r` | 刷新数据 |
| `n` | 选择命名空间 |
| `c` | 选择上下文 |
| `l` | 查看 Pod 日志 |
| `d` | 描述资源 |
| `?` | 显示帮助 |
| `1-4` | 切换标签页（Pods、Deployments、Services、Nodes） |
| `↑/↓` | 导航行 |
| `Enter` | 选择项目 |

#### 标签页概览

1. **Pods 标签页** (`1`)：查看所有 Pod，显示状态、就绪数、重启次数、年龄、IP 和节点
2. **Deployments 标签页** (`2`)：监控 Deployment 及其副本状态
3. **Services 标签页** (`3`)：查看服务类型、集群 IP 和端口
4. **Nodes 标签页** (`4`)：检查节点状态、角色和版本

### 💡 设计思路

KubeTUI 基于以下原则构建：
- **简洁性**：最小依赖，易于理解的代码库
- **高性能**：异步操作，高效数据获取
- **可扩展性**：模块化架构，便于添加新功能
- **用户体验**：受 htop 和 k9s 启发的直观界面

### 📦 打包与部署

```bash
# 构建包
pip install build
python -m build

# 运行测试
pytest

# 类型检查
mypy src/kubetui

# 代码检查
ruff check src/kubetui
```

### 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 📖 繁體中文

### 🎉 專案介紹

**KubeTUI** 是一款現代化的終端使用者介面（TUI）工具，專為 Kubernetes 叢集管理而設計。它提供了直觀、鍵盤驅動的介面，讓您高效地監控和管理 K8s 叢集。

**為什麼選擇 KubeTUI？**
- 🔥 **快速輕量**：基於 Python 和 Textual 建立，毫秒級啟動
- 🎨 **美觀介面**：現代化的彩色介面，帶有斑馬紋表格
- ⌨️ **鍵盤優先**：所有操作都可透過快捷鍵完成
- 🔌 **零設定**：直接使用現有的 kubeconfig，開箱即用
- 📦 **簡單安裝**：一條 pip 指令即可安裝

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📊 **即時監控** | 查看 Pods、Deployments、Services、Nodes，即時更新 |
| 📝 **日誌檢視** | 串流檢視 Pod 日誌，支援跟隨模式和複製 |
| 🔄 **資源操作** | 刪除 Pod、擴縮容 Deployment、重啟工作負載 |
| 🎯 **情境切換** | 快速切換 Kubernetes 情境 |
| 📁 **命名空間導航** | 輕鬆瀏覽和選擇命名空間 |
| 🔍 **資源搜尋** | 快速過濾和尋找資源 |
| ⌨️ **快捷鍵** | 無需滑鼠，高效導航 |

### 🚀 快速開始

#### 環境要求
- Python 3.10 或更高版本
- 已設定 kubeconfig 的 Kubernetes 叢集
- 已安裝並設定 kubectl

#### 安裝

```bash
# 從 PyPI 安裝
pip install kubetui

# 或從原始碼安裝
git clone https://github.com/gitstq/KubeTUI.git
cd KubeTUI
pip install -e .
```

#### 執行

```bash
# 啟動 KubeTUI
kubetui

# 或直接執行
python -m kubetui
```

### 📖 使用指南

#### 快捷鍵

| 按鍵 | 操作 |
|------|------|
| `q` | 離開 |
| `r` | 重新整理資料 |
| `n` | 選擇命名空間 |
| `c` | 選擇情境 |
| `l` | 檢視 Pod 日誌 |
| `d` | 描述資源 |
| `?` | 顯示說明 |
| `1-4` | 切換標籤頁（Pods、Deployments、Services、Nodes） |
| `↑/↓` | 導航行 |
| `Enter` | 選擇項目 |

#### 標籤頁概覽

1. **Pods 標籤頁** (`1`)：檢視所有 Pod，顯示狀態、就緒數、重啟次數、年齡、IP 和節點
2. **Deployments 標籤頁** (`2`)：監控 Deployment 及其副本狀態
3. **Services 標籤頁** (`3`)：檢視服務類型、叢集 IP 和連接埠
4. **Nodes 標籤頁** (`4`)：檢查節點狀態、角色和版本

### 💡 設計思路

KubeTUI 基於以下原則建立：
- **簡潔性**：最小依賴，易於理解的程式碼庫
- **高效能**：非同步操作，高效資料獲取
- **可擴展性**：模組化架構，便於新增功能
- **使用者體驗**：受 htop 和 k9s 啟發的直觀介面

### 📦 打包與部署

```bash
# 建置套件
pip install build
python -m build

# 執行測試
pytest

# 類型檢查
mypy src/kubetui

# 程式碼檢查
ruff check src/kubetui
```

### 🤝 貢獻指南

歡迎貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

### 📄 開源授權

本專案採用 MIT 授權條款開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by SOLO Agent**

[⬆ Back to Top](#-kubetui)

</div>
