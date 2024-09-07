import openai
from .config import Config
config = Config()
openai.api_key = config.openai_apikey
openai.api_base = config.openai_endpoint
async def get_ai_response(title,text):
    try:
        prompt = f"文章标题: {title}\n文章内容: {text}"
        response = await openai.ChatCompletion.acreate(
            model=config.openai_model,
            messages=[
                {"role": "system", "content": "你是一个文章摘要助手，请根据我给你的内容返回摘要，若标题与文章内容不一致，以文章内容为准"},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"