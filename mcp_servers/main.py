#!/usr/bin/env python3
"""
MCP服务器启动器
支持启动桌面文件统计器和多语言翻译服务器
"""

import sys
import argparse
import importlib

def main():
    parser = argparse.ArgumentParser(description='MCP服务器启动器')
    parser.add_argument('server', choices=['txt-counter', 'multilingual-translator'], 
                       help='选择要启动的服务器')
    
    args = parser.parse_args()
    
    if args.server == 'txt-counter':
        print("启动桌面TXT文件统计器...", file=sys.stderr)
        from txt_counter import mcp
        mcp.run()
    elif args.server == 'multilingual-translator':
        print("启动多语言翻译服务器...", file=sys.stderr)
        from scripts.multilingual_translator import app
        app.run()

if __name__ == "__main__":
    main()
