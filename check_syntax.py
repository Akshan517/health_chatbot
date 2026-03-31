"""
Quick syntax and import check for bot.py
"""
import sys
import traceback

try:
    import telebot
    print("✅ telebot imported")
    
    import joblib
    print("✅ joblib imported")
    
    import pandas as pd
    print("✅ pandas imported")
    
    import numpy as np
    print("✅ numpy imported")
    
    from simple_generator import SimpleMultilingualGenerator
    print("✅ SimpleMultilingualGenerator imported")
    
    import os
    from dotenv import load_dotenv
    print("✅ dotenv imported")
    
    # Check syntax by compiling (with UTF-8 encoding)
    with open('bot.py', 'r', encoding='utf-8') as f:
        code = f.read()
    compile(code, 'bot.py', 'exec')
    print("✅ bot.py syntax is valid")
    
    print("\n✅ All imports and syntax checks passed!")
    print("\nTo start the bot, run: python bot.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
