from __future__ import annotations

from usetai_agentic_ai.providers.base import BasePlannerProvider
from usetai_agentic_ai.providers.heuristic import HeuristicPlannerProvider
from usetai_agentic_ai.providers.hf_inference import HFInferencePlannerProvider
from usetai_agentic_ai.providers.ollama import OllamaPlannerProvider
from usetai_agentic_ai.settings import AppSettings


def build_provider(settings: AppSettings) -> BasePlannerProvider:
    provider = settings.provider.lower().strip()
    if provider == "ollama":
        return OllamaPlannerProvider(base_url=settings.ollama_base_url, model=settings.ollama_model)
    if provider == "hf_inference" and settings.hf_api_token:
        return HFInferencePlannerProvider(model=settings.hf_model, token=settings.hf_api_token)
    return HeuristicPlannerProvider()
