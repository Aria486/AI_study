# MCP 服务器集合

这个项目包含了两个 Model Context Protocol (MCP) 服务器：

## 服务器列表

### 1. 桌面 TXT 文件统计器 (`txt_counter.py`)

- **功能**: 统计和列出桌面上的 TXT 文件
- **工具**:
  - `count_desktop_txt_files`: 统计桌面 TXT 文件数量
  - `list_desktop_txt_files`: 列出桌面所有 TXT 文件名

### 2. 多语言翻译服务器 (`multilingual_translator.py`)

- **功能**: 智能多语言翻译
   - 中文 → 日语 + 英语（双语翻译）
   - 日文 → 中文 + 英语（双语翻译）
   - 英语 → 中文 + 日语（双语翻译）
   - 其他语言 → 中文 + 日语 + 英语（三语翻译）
- **工具**:
  - `translate`: 自动检测语言并进行多语言翻译
  - `language_detect`: 详细的语言检测分析
- **提示词**: `translation_expert` - 多语言翻译专家提示词模板

## 安装和使用

### 环境要求

- Python >= 3.12
- uv (推荐的包管理器)

### 安装依赖

```bash
cd mcp_servers
uv sync
```

### 单独运行服务器

#### 启动桌面文件统计器

```bash
uv run python txt_counter.py
```

#### 启动多语言翻译服务器

```bash
uv run python multilingual_translator.py
```

### 使用统一启动器

```bash
# 启动文件统计器
uv run python main.py txt-counter

# 启动翻译服务器
uv run python main.py multilingual-translator
```

## MCP 客户端配置

将以下配置添加到您的 MCP 客户端配置文件中：

### Claude Desktop 配置

在 `~/Library/Application Support/Claude/claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "txt-counter": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "/Users/r_wang/Documents/study/AI_study/mcp_servers/txt_counter.py"
      ],
      "cwd": "/Users/r_wang/Documents/study/AI_study/mcp_servers"
    },
    "multilingual-translator": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "/Users/r_wang/Documents/study/AI_study/mcp_servers/scripts/multilingual_translator.py"
      ],
      "cwd": "/Users/r_wang/Documents/study/AI_study/mcp_servers"
    }
  }
}
```

## 功能特点

### 桌面文件统计器

- 自动获取当前用户的桌面路径
- 支持统计和列出 TXT 文件
- 跨平台兼容性

### 多语言翻译工具

- 智能语言检测（通过字符集分析）
- 多语言翻译支持：
  - 中文 → 日语 + 英语
  - 日文 → 中文 + 英语
  - 英语/其他语言 → 中文 + 日语 + 英语
- 详细的翻译解释和标注
- 语法分析和文化背景说明
- 多种翻译风格支持

## 开发说明

所有服务器都使用 FastMCP 框架构建，支持：

- 标准 MCP 协议
- stdio 传输方式
- 自动工具注册
- 错误处理和日志记录
