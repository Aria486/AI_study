#!/usr/bin/env python3

import asyncio
import logging
import sys
import re
from typing import Optional

# 配置日志以便调试
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from mcp.server import FastMCP
except ImportError as e:
    print(f"导入MCP模块失败: {e}", file=sys.stderr)
    print("请确保已安装mcp包: uv add mcp", file=sys.stderr)
    sys.exit(1)

# 创建MCP应用实例
app = FastMCP('chinese_japanese_translator')

def detect_language(text: str) -> str:
    """
    检测文本语言（中文或日文）
    通过字符集特征来判断主要语言
    """
    # 中文字符范围（简体和繁体）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 日文平假名
    hiragana_chars = len(re.findall(r'[\u3040-\u309f]', text))
    # 日文片假名
    katakana_chars = len(re.findall(r'[\u30a0-\u30ff]', text))
    
    japanese_chars = hiragana_chars + katakana_chars
    total_cjk_chars = chinese_chars + japanese_chars
    
    if total_cjk_chars == 0:
        return 'unknown'
    
    # 如果有平假名或片假名，很可能是日文
    if japanese_chars > 0:
        return 'japanese'
    # 否则判断为中文
    else:
        return 'chinese'

@app.tool('translate')
async def translate_text(text: str) -> str:
    """
    智能中日双向翻译工具
    
    Args:
        text: 需要翻译的文本
        
    Returns:
        包含翻译结果、语言检测、详细解释和标注的完整信息
    """
    # 检测输入语言
    detected_lang = detect_language(text.strip())
    
    if detected_lang == 'chinese':
        # 中文翻译成日文
        target_lang = 'Japanese'
        source_lang = 'Chinese'
        translation_prompt = f"""
你是专业的中日翻译专家。请将以下中文翻译成日文，并提供详细的解释和标注：

原文：{text}

请按以下格式输出：

## 翻译结果
[日文翻译]

## 语言检测
- 源语言：中文
- 目标语言：日文

## 详细解释
### 语法分析
[分析中文句子的语法结构]

### 翻译要点
[解释翻译过程中的关键点和难点]

### 日文语法说明
[解释日文译文的语法结构]

## 重点标注
### 词汇对照
[重要词汇的中日对照]

### 敬语使用
[如果涉及敬语，说明使用情况]

### 文化背景
[如果有文化差异，进行说明]

## 替代表达
[提供其他可能的翻译方式]
"""
    
    elif detected_lang == 'japanese':
        # 日文翻译成中文
        target_lang = 'Chinese'
        source_lang = 'Japanese'
        translation_prompt = f"""
你是专业的日中翻译专家。请将以下日文翻译成中文，并提供详细的解释和标注：

原文：{text}

请按以下格式输出：

## 翻译结果
[中文翻译]

## 语言检测
- 源语言：日文
- 目标语言：中文

## 详细解释
### 语法分析
[分析日文句子的语法结构，包括助词、动词变位等]

### 翻译要点
[解释翻译过程中的关键点和难点]

### 中文表达说明
[解释中文译文的表达方式选择]

## 重点标注
### 词汇对照
[重要词汇的日中对照]

### 敬语分析
[如果涉及敬语，详细分析敬语级别和使用场合]

### 语法要素
[标注重要的日文语法要素：助词、敬语、时态等]

### 文化背景
[如果有文化差异，进行说明]

## 替代表达
[提供其他可能的翻译方式]
"""
    
    else:
        return f"""
## 错误提示
无法识别输入文本的语言类型。

## 支持的语言
- 中文（简体/繁体）
- 日文（平假名/片假名/汉字）

## 输入文本
{text}

请确保输入的是中文或日文文本。
"""
    
    return translation_prompt

@app.tool('language_detect')
async def detect_text_language(text: str) -> str:
    """
    检测文本语言的详细信息
    
    Args:
        text: 需要检测的文本
        
    Returns:
        详细的语言检测结果
    """
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    hiragana_chars = len(re.findall(r'[\u3040-\u309f]', text))
    katakana_chars = len(re.findall(r'[\u30a0-\u30ff]', text))
    ascii_chars = len(re.findall(r'[a-zA-Z]', text))
    numbers = len(re.findall(r'[0-9]', text))
    
    detected_lang = detect_language(text)
    
    result = f"""
## 语言检测结果

### 主要语言
{detected_lang.upper() if detected_lang != 'unknown' else '未知语言'}

### 字符统计
- 中日韩汉字：{chinese_chars} 个
- 日文平假名：{hiragana_chars} 个  
- 日文片假名：{katakana_chars} 个
- 英文字母：{ascii_chars} 个
- 数字：{numbers} 个

### 检测说明
"""
    
    if detected_lang == 'chinese':
        result += "- 主要包含汉字，无日文假名，判断为中文"
    elif detected_lang == 'japanese':
        result += "- 包含日文假名或日文特有表达，判断为日文"
    else:
        result += "- 无法识别为中文或日文，可能包含其他语言或字符"
    
    result += f"""

### 原文本
{text}
"""
    
    return result

@app.prompt('translation_expert')
async def translation_expert_prompt(
    source_language: str = 'auto',
    target_language: str = 'auto',
    style: str = 'standard'
) -> str:
    """
    翻译专家提示词模板
    
    Args:
        source_language: 源语言 (chinese/japanese/auto)
        target_language: 目标语言 (chinese/japanese/auto)  
        style: 翻译风格 (standard/formal/casual/literary)
    """
    
    style_descriptions = {
        'standard': '标准翻译，保持原文语气和风格',
        'formal': '正式翻译，使用敬语和正式表达',
        'casual': '口语化翻译，使用日常表达',
        'literary': '文学性翻译，注重文学美感'
    }
    
    if source_language == 'auto' and target_language == 'auto':
        return f"""
你是资深的中日双向翻译专家，具备以下专业能力：

## 专业技能
- 精通中文（简体/繁体）和日文（敬语体系、方言差异）
- 深度理解两种语言的文化背景和表达习惯
- 能够准确识别语言类型并进行高质量翻译
- 熟悉各种文本类型：商务、学术、文学、日常对话等

## 翻译原则
- 准确传达原文含义，保持语言风格
- 考虑文化差异，适当进行本土化处理
- 注重语法正确性和自然流畅度
- 提供详细的翻译解释和标注

## 当前设置
- 翻译风格：{style_descriptions.get(style, style)}
- 语言检测：自动识别中文/日文
- 输出格式：包含翻译、解释、标注的完整信息

请输入需要翻译的文本，我将为您提供专业的翻译服务。
"""
    
    else:
        source_desc = {'chinese': '中文', 'japanese': '日文', 'auto': '自动检测'}.get(source_language, source_language)
        target_desc = {'chinese': '中文', 'japanese': '日文', 'auto': '自动检测'}.get(target_language, target_language)
        
        return f"""
你是专业的翻译专家，当前配置：

## 翻译设置
- 源语言：{source_desc}
- 目标语言：{target_desc}
- 翻译风格：{style_descriptions.get(style, style)}

## 服务内容
- 提供准确的翻译结果
- 详细的语法和词汇解释
- 重点内容标注和说明
- 文化背景和使用场合说明
- 替代表达方式推荐

请提供需要翻译的文本。
"""

if __name__ == '__main__':
    try:
        # 使用简化的启动方式
        app.run(transport='stdio')
    except Exception as e:
        print(f"启动失败: {e}", file=sys.stderr)
        sys.exit(1)