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
        ├── multilingual_translator.py  # 多语言翻译服务器
        └── txt_counter.py               # 桌面文件统计器脚本
```

## MCP 服务器

实现了以下 MCP 服务器：

1. **桌面 TXT 文件统计器** - 统计和管理桌面上的文本文件
2. **多语言翻译工具** - 智能的多语言翻译服务
   - 中文 → 日语 + 英语（双语翻译）
   - 日文 → 中文 + 英语（双语翻译）
   - 英语 → 中文 + 日语（双语翻译）
   - 其他语言 → 中文 + 日语 + 英语（三语翻译）

详细说明请查看 [mcp_servers/README.md](mcp_servers/README.md)

## 快速开始

```bash
cd mcp_servers
uv sync
uv run python txt_counter.py
```
