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
app = FastMCP('multilingual_translator')

def detect_language(text: str) -> str:
    """
    检测文本语言（中文、日文、英文或其他）
    通过字符集特征来判断主要语言
    """
    # 中文字符范围（简体和繁体）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 日文平假名
    hiragana_chars = len(re.findall(r'[\u3040-\u309f]', text))
    # 日文片假名
    katakana_chars = len(re.findall(r'[\u30a0-\u30ff]', text))
    # 英文字符
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    # 其他常见欧洲语言字符
    other_chars = len(re.findall(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', text.lower()))
    
    japanese_chars = hiragana_chars + katakana_chars
    total_cjk_chars = chinese_chars + japanese_chars
    total_latin_chars = english_chars + other_chars
    
    # 如果有平假名或片假名，很可能是日文
    if japanese_chars > 0:
        return 'japanese'
    # 如果主要是汉字，判断为中文
    elif chinese_chars > 0 and chinese_chars >= total_latin_chars:
        return 'chinese'
    # 如果主要是英文字符且其他欧洲字符较少，判断为英文
    elif english_chars > 0 and other_chars == 0:
        return 'english'
    # 如果有其他欧洲语言字符，判断为其他语言
    elif total_latin_chars > 0:
        return 'other'
    # 否则未知
    else:
        return 'unknown'

@app.tool('translate')
async def translate_text(text: str) -> str:
    """
    智能多语言翻译工具
    
    Args:
        text: 需要翻译的文本
        
    Returns:
        包含翻译结果、语言检测、详细解释和标注的完整信息
    """
    # 检测输入语言
    detected_lang = detect_language(text.strip())
    
    if detected_lang == 'chinese':
        # 中文默认翻译成日语和英语（双语）
        translation_prompt = f"""
你是专业的多语言翻译专家。请将以下中文翻译成日语和英语，并提供详细的解释：

原文：{text}

请按以下格式输出：

## 翻译结果

### 日语翻译
[日文翻译]

### 英语翻译
[英文翻译]

## 语言检测
- 源语言：中文
- 目标语言：日语 + 英语

## 详细解释

### 中文语法分析
[分析中文句子的语法结构]

### 日语翻译要点
[解释中译日的关键点和难点]
- 敬语使用情况
- 语法结构说明
- 文化差异处理

### 英语翻译要点
[解释中译英的关键点和难点]
- 语序调整
- 时态处理
- 文化背景转换

## 重点标注

### 中日对照
[重要词汇的中日对照]

### 中英对照
[重要词汇的中英对照]

### 文化背景
[如果有文化差异，进行说明]

## 替代表达
### 日语替代表达
[提供其他可能的日语翻译方式]

### 英语替代表达
[提供其他可能的英语翻译方式]
"""
    
    elif detected_lang == 'japanese':
        # 日文翻译成中文、英语（双语）
        translation_prompt = f"""
你是专业的多语言翻译专家。请将以下日文翻译成中文和英语，并提供详细的解释：

原文：{text}

请按以下格式输出：

## 翻译结果

### 中文翻译
[中文翻译]

### 英语翻译
[英文翻译]

## 语言检测
- 源语言：日文
- 目标语言：中文 + 英语

## 详细解释

### 日语语法分析
[分析日文句子的语法结构，包括助词、动词变位、敬语等]

### 中文翻译要点
[解释日译中的关键点和难点]
- 敬语级别转换
- 语法结构调整
- 文化表达本土化

### 英语翻译要点
[解释日译英的关键点和难点]
- 语序转换
- 敬语体现方式
- 文化概念翻译

## 重点标注

### 日中对照
[重要词汇的日中对照]

### 日英对照
[重要词汇的日英对照]

### 敬语分析
[详细分析敬语级别和使用场合]

### 文化背景
[如果有文化差异，进行说明]

## 替代表达
### 中文替代表达
[提供其他可能的中文翻译方式]

### 英语替代表达
[提供其他可能的英语翻译方式]
"""
    
    elif detected_lang == 'english':
        # 英语翻译成中文、日语（双语）
        translation_prompt = f"""
你是专业的多语言翻译专家。请将以下英文翻译成中文和日语，并提供详细的解释：

原文：{text}

请按以下格式输出：

## 翻译结果

### 中文翻译
[中文翻译]

### 日语翻译
[日文翻译]

## 语言检测
- 源语言：英语
- 目标语言：中文 + 日语

## 详细解释

### 英语语法分析
[分析英文句子的语法结构]

### 中文翻译要点
[解释英译中的关键点和难点]
- 语序调整
- 时态处理
- 文化背景转换

### 日语翻译要点
[解释英译日的关键点和难点]
- 敬语选择
- 语法结构转换
- 文化表达适配

## 重点标注

### 英中对照
[重要词汇的英中对照]

### 英日对照
[重要词汇的英日对照]

### 文化背景
[如果有文化差异，进行说明]

## 替代表达
### 中文替代表达
[提供其他可能的中文翻译方式]

### 日语替代表达
[提供其他可能的日语翻译方式]
"""
    
    elif detected_lang == 'other':
        # 其他语言默认翻译成中文、日语、英语（三语）
        translation_prompt = f"""
你是专业的多语言翻译专家。请将以下文本翻译成中文、日语和英语，并提供详细的解释：

原文：{text}

请按以下格式输出：

## 翻译结果

### 中文翻译
[中文翻译]

### 日语翻译
[日文翻译]

### 英语翻译
[英文翻译]

## 语言检测
- 源语言：其他欧洲语言
- 目标语言：中文 + 日语 + 英语

## 详细解释

### 原文语法分析
[分析原文的语法结构]

### 中文翻译要点
[解释译成中文的关键点和难点]
- 语序调整
- 时态处理
- 文化背景转换

### 日语翻译要点
[解释译成日语的关键点和难点]
- 敬语选择
- 语法结构转换
- 文化表达适配

### 英语翻译要点
[解释译成英语的关键点和难点]

## 重点标注

### 多语言词汇对照
[重要词汇的多语言对照表]

### 语法要素对比
[不同语言的语法特点对比]

### 文化背景
[如果有文化差异，进行说明]

## 替代表达
### 中文替代表达
[提供其他可能的中文翻译方式]

### 日语替代表达
[提供其他可能的日语翻译方式]

### 英语替代表达
[提供其他可能的英语翻译方式]
"""
    
    else:
        return f"""
## 错误提示
无法识别输入文本的语言类型。

## 支持的语言
- 中文（简体/繁体）→ 翻译为日语 + 英语
- 日文（平假名/片假名/汉字）→ 翻译为中文 + 英语
- 英语 → 翻译为中文 + 日语
- 其他欧洲语言 → 翻译为中文 + 日语 + 英语

## 输入文本
{text}

请确保输入的是支持的语言文本。
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
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    other_chars = len(re.findall(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', text.lower()))
    numbers = len(re.findall(r'[0-9]', text))
    
    detected_lang = detect_language(text)
    
    result = f"""
## 语言检测结果

### 主要语言
{detected_lang.upper().replace('_', ' ') if detected_lang != 'unknown' else '未知语言'}

### 字符统计
- 中日韩汉字：{chinese_chars} 个
- 日文平假名：{hiragana_chars} 个  
- 日文片假名：{katakana_chars} 个
- 英文字母：{english_chars} 个
- 其他欧洲字符：{other_chars} 个
- 数字：{numbers} 个

### 翻译策略
"""
    
    if detected_lang == 'chinese':
        result += "- 中文 → 日语 + 英语（双语翻译）"
    elif detected_lang == 'japanese':
        result += "- 日文 → 中文 + 英语（双语翻译）"
    elif detected_lang == 'english':
        result += "- 英语 → 中文 + 日语（双语翻译）"
    elif detected_lang == 'other':
        result += "- 其他语言 → 中文 + 日语 + 英语（三语翻译）"
    else:
        result += "- 未识别语言，无法提供翻译"

    result += f"""

### 检测说明
"""
    
    if detected_lang == 'chinese':
        result += "- 主要包含汉字，无日文假名，判断为中文"
    elif detected_lang == 'japanese':
        result += "- 包含日文假名或日文特有表达，判断为日文"
    elif detected_lang == 'english':
        result += "- 主要包含英文字符，无其他欧洲语言特殊字符，判断为英语"
    elif detected_lang == 'other':
        result += "- 包含其他欧洲语言特殊字符，判断为其他欧洲语言"
    else:
        result += "- 无法识别为支持的语言类型"
    
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
    多语言翻译专家提示词模板
    
    Args:
        source_language: 源语言 (chinese/japanese/english/auto)
        target_language: 目标语言 (chinese/japanese/english/auto)  
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
你是资深的多语言翻译专家，具备以下专业能力：

## 专业技能
- 精通中文（简体/繁体）、日文（敬语体系、方言差异）、英文
- 深度理解多种语言的文化背景和表达习惯
- 能够准确识别语言类型并进行高质量多语言翻译
- 熟悉各种文本类型：商务、学术、文学、日常对话等

## 翻译策略
- 中文 → 日语 + 英语（双语翻译）
- 日文 → 中文 + 英语（双语翻译）
- 英语 → 中文 + 日语（双语翻译）
- 其他语言 → 中文 + 日语 + 英语（三语翻译）

## 翻译原则
- 准确传达原文含义，保持语言风格
- 考虑文化差异，适当进行本土化处理
- 注重语法正确性和自然流畅度
- 提供详细的翻译解释和多语言对照

## 当前设置
- 翻译风格：{style_descriptions.get(style, style)}
- 语言检测：自动识别中文/日文/英文
- 输出格式：包含多语言翻译、解释、标注的完整信息

请输入需要翻译的文本，我将为您提供专业的多语言翻译服务。
"""
    
    else:
        source_desc = {'chinese': '中文', 'japanese': '日文', 'english': '英文', 'auto': '自动检测'}.get(source_language, source_language)
        target_desc = {'chinese': '中文', 'japanese': '日文', 'english': '英文', 'auto': '自动检测'}.get(target_language, target_language)
        
        return f"""
你是专业的多语言翻译专家，当前配置：

## 翻译设置
- 源语言：{source_desc}
- 目标语言：{target_desc}
- 翻译风格：{style_descriptions.get(style, style)}

## 服务内容
- 提供准确的多语言翻译结果
- 详细的语法和词汇解释
- 重点内容标注和说明
- 文化背景和使用场合说明
- 多语言替代表达方式推荐

请提供需要翻译的文本。
"""

if __name__ == '__main__':
    try:
        # 使用简化的启动方式
        app.run(transport='stdio')
    except Exception as e:
        print(f"启动失败: {e}", file=sys.stderr)
        sys.exit(1)