"""
Script to check if API keys are properly configured
Run this to debug API key issues
"""

import os
import sys

# Try to load .env file
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"✓ Loaded .env file from: {env_path}")
    else:
        load_dotenv()
        print("✓ Tried to load .env file (not found, using system env vars)")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("  Using system environment variables only.")

# Check API keys
print("\n=== API Keys Check ===")
openai_key = os.getenv('OPENAI_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

if openai_key:
    print(f"✓ OpenAI API Key: Found")
    print(f"  Length: {len(openai_key)}")
    print(f"  Starts with: {openai_key[:7]}...")
    print(f"  Valid format: {'Yes' if openai_key.startswith('sk-') else 'No (should start with sk-)'}")
else:
    print("✗ OpenAI API Key: Not found")
    print("  Set it with: export OPENAI_API_KEY='your-key'")
    print("  Or add to .env file: OPENAI_API_KEY=your-key")

if gemini_key:
    print(f"\n✓ Gemini API Key: Found")
    print(f"  Length: {len(gemini_key)}")
    print(f"  Starts with: {gemini_key[:7]}...")
else:
    print("\n✗ Gemini API Key: Not found")
    print("  Set it with: export GEMINI_API_KEY='your-key'")
    print("  Or add to .env file: GEMINI_API_KEY=your-key")

# Check if packages are installed
print("\n=== Package Check ===")
try:
    import openai
    print("✓ openai package: Installed")
except ImportError:
    print("✗ openai package: Not installed")
    print("  Install with: pip install openai")

try:
    import google.generativeai
    print("✓ google-generativeai package: Installed")
except ImportError:
    print("✗ google-generativeai package: Not installed")
    print("  Install with: pip install google-generativeai")

# Try to initialize clients
print("\n=== Client Initialization Test ===")
if openai_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        print("✓ OpenAI client: Initialized successfully")
    except Exception as e:
        print(f"✗ OpenAI client: Failed to initialize")
        print(f"  Error: {e}")

if gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✓ Gemini client: Initialized successfully")
    except Exception as e:
        print(f"✗ Gemini client: Failed to initialize")
        print(f"  Error: {e}")

print("\n=== Summary ===")
if openai_key or gemini_key:
    print("✓ At least one API key is configured")
    if not openai_key:
        print("  → Consider adding OpenAI API key for better coverage")
    if not gemini_key:
        print("  → Consider adding Gemini API key for better coverage")
else:
    print("✗ No API keys found")
    print("  → The system will work but won't fetch new restaurant data from AI")
    print("  → Add API keys to enable AI data fetching")

print("\nDone!")

