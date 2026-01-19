# Agent Utilities and LLM Setup

The `src/agents` directory contains the core logic for the AI agents used throughout the 100 Days curriculum.

## \u26a1 Using Real LLMs

By default, this repository runs in **Mock Mode** (Simulation) so you can complete the curriculum without API keys or internet access.
However, for advanced testing and Red Teaming (Phases 3 & 4), you can "eject" to using real LLMs like GPT-5, Claude 3.5, or Gemini.

### 1. Installation

Ensure you have the latest providers installed:

```bash
pip install -r requirements.txt
```

### 2. Configuration

You can control which LLM is used by setting environment variables in your terminal or `.env` file.

#### Option A: OpenAI (Default Global Standard)
```bash
export LLM_PROVIDER="openai"
export OPENAI_API_KEY="sk-..."

# Optional: Override the default model (Defaults to gpt-5.2-turbo)
export LLM_MODEL="gpt-4o"
```

#### Option B: Anthropic (Claude)
```bash
export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: Override the default model (Defaults to claude-3-5-sonnet-20240620)
export LLM_MODEL="claude-3-opus-20240229"
```

#### Option C: Google (Gemini)
```bash
export LLM_PROVIDER="gemini"
export GOOGLE_API_KEY="AIza..."

# Optional: Override the default model (Defaults to gemini-1.5-pro)
export LLM_MODEL="gemini-1.5-flash"
```

### 3. Usage inside Notebooks

Once the variables are set, the `VulnerableBot` and other agents will automatically use the live model.

```python
from src.agents.vulnerable_bot import VulnerableBot

# Uses the provider defined in environment variables
bot = VulnerableBot() 
print(bot.chat("Hello!")) 
```

### 4. Fallback Behavior

If `LLM_PROVIDER` is not set, or if the API key is missing, the system will silently fall back to `MockLLM`. This ensures that your code doesn't crash if you share it with someone who doesn't have keys.
