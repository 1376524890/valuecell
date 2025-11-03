import os
from pathlib import Path

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    # First try to load from parent project's .env file
    parent_env_file = Path(__file__).parent.parent.parent.parent.parent / ".env"
    if parent_env_file.exists():
        load_dotenv(parent_env_file, override=True)
        print(f"✅ Loaded environment variables from parent project: {parent_env_file}")
    else:
        # Then try to load from current project's .env file
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=True)
            print(f"✅ Loaded environment variables from {env_file} (with override)")
        else:
            print(f"ℹ️  No .env file found, using system environment variables")
except ImportError:
    print("⚠️  python-dotenv not installed. Install it with: pip install python-dotenv")
    print("   Environment variables will be read from system environment only.")

def str_to_bool(value):
    """Convert string to boolean, handling various string representations."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return bool(value)

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": os.getenv("TRADINGAGENTS_DATA_DIR", "./data"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings - 使用DashScope替代OpenAI
    "llm_provider": os.getenv("TRADINGAGENTS_LLM_PROVIDER", "openai"),  # 保持名称为openai以兼容现有代码
    "deep_think_llm": os.getenv("TRADINGAGENTS_DEEP_THINK_LLM", "qwen3-max"),  # 使用DashScope支持的模型
    "quick_think_llm": os.getenv("TRADINGAGENTS_QUICK_THINK_LLM", "qwen3-max"),
    "backend_url": os.getenv("OPENAI_COMPATIBLE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    # Embeddings settings - 也使用DashScope
    "EMBEDDER_BASE_URL": os.getenv("OPENAI_COMPATIBLE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    "EMBEDDER_MODEL_ID": os.getenv("EMBEDDER_MODEL_ID", "text-embedding-v1"),  # 使用DashScope的嵌入模型
    # Debate and discussion settings
    "max_debate_rounds": int(os.getenv("TRADINGAGENTS_MAX_DEBATE_ROUNDS", "1")),
    "max_risk_discuss_rounds": int(os.getenv("TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS", "1")),
    "max_recur_limit": int(os.getenv("TRADINGAGENTS_MAX_RECUR_LIMIT", "100")),
    # Tool settings
    "online_tools": str_to_bool(os.getenv("TRADINGAGENTS_ONLINE_TOOLS", "True")),
}
