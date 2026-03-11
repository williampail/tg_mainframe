from openai import OpenAI
from config import OPENROUTER_API_KEY, MODEL, WRITING_STYLE

# OpenRouter uses OpenAI-compatible API
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = f"""You are a writing assistant that rewrites content in a specific style.
Your task is to rewrite posts while preserving their core meaning and key information.

Style guidelines:
{WRITING_STYLE}

Rules:
- Keep the main message and facts intact
- Maintain appropriate length (similar to original)
- Make it sound natural and engaging
- Don't add information that wasn't in the original
- Output ONLY the rewritten text, no explanations"""


def rewrite_post(text: str) -> str:
    """
    Rewrite the given text in the configured writing style.
    
    Args:
        text: The original post text
        
    Returns:
        The rewritten text in your style
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Rewrite this post:\n\n{text}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to rewrite post: {e}")
