import asyncio, httpx
from app.core.config import settings

class AIUnavailable(Exception): pass
class GeminiService:
    """Server-side Gemini adapter. No credentials means an explicit unavailable response."""
    def __init__(self): self.key=settings.gemini_api_key
    async def _generate(self, model:str, prompt:str)->str:
        if not self.key: raise AIUnavailable("Gemini is not configured. Set GEMINI_API_KEY on the backend.")
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.key}"
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response=await client.post(url,json={"contents":[{"parts":[{"text":prompt}]}]})
            if response.status_code==429: raise AIUnavailable("Gemini rate limit reached; retry later.")
            response.raise_for_status(); data=response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    async def tutor(self, message:str, target:str, known:str, explanation:str, mode:str="fast"):
        if not self.key: raise AIUnavailable("AI tutor is not configured. Add GEMINI_API_KEY to backend environment.")
        prompt=(f"You are LanguageHub, a careful multilingual language tutor. Teach target language {target}; "
                f"learner knows {known}; explain in {explanation}. Correct gently, give a useful example, "
                f"and do not claim speech evaluation without audio. Learner says: {message}")
        models=[settings.gemini_fallback_model] if mode=="fallback" else [settings.gemini_primary_model,settings.gemini_fallback_model]
        last=None
        for model in dict.fromkeys(models):
            for attempt in range(2):
                try: return await self._generate(model,prompt),model
                except (httpx.HTTPError,KeyError,IndexError,AIUnavailable) as exc:
                    last=exc
                    if isinstance(exc,AIUnavailable) and "not configured" in str(exc): raise
                    if attempt==0: await asyncio.sleep(.5*(2**attempt))
        raise AIUnavailable(f"Configured Gemini models unavailable: {last}")
