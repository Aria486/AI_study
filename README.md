# AI

# AI Study Project

这是一个 AI 学习项目，包含了 MCP (Model Context Protocol) 服务器的实现。

## 项目结构

```
AI_study/
├── README.md
└── mcp_servers/          # MCP服务器集合
    ├── main.py           # 统一启动器
    ├── txt_counter.py    # 桌面文件统计器
    ├── mcp.json          # MCP服务器配置
    ├── pyproject.toml    # 项目配置文件
    ├── uv.lock           # 依赖锁定文件
    ├── README.md         # 详细说明文档
    ├── .gitignore        # Git忽略文件
    ├── .python-version   # Python版本文件
    ├── .venv/            # 虚拟环境目录
    ├── __pycache__/      # Python缓存目录
    └── scripts/          # 脚本目录
        ├── cn_jp_language_translate.py  # 中日翻译服务器
        └── txt_counter.py               # 桌面文件统计器脚本
```

## MCP 服务器

本项目实现了两个功能完整的 MCP 服务器：

1. **桌面 TXT 文件统计器** - 统计和管理桌面上的文本文件
2. **中日翻译工具** - 智能的中日双向翻译服务

详细说明请查看 [mcp_servers/README.md](mcp_servers/README.md)

## 快速开始

```bash
cd mcp_servers
uv sync
uv run python txt_counter.py
```
