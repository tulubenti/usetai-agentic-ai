from usetai_agentic_ai.providers.factory import build_provider
from usetai_agentic_ai.providers.heuristic import HeuristicPlannerProvider
from usetai_agentic_ai.providers.hf_inference import HFInferencePlannerProvider
from usetai_agentic_ai.providers.ollama import OllamaPlannerProvider
from usetai_agentic_ai.settings import AppSettings


def test_default_provider_is_heuristic() -> None:
    provider = build_provider(AppSettings(provider="heuristic"))
    assert isinstance(provider, HeuristicPlannerProvider)


def test_ollama_provider_selected() -> None:
    provider = build_provider(AppSettings(provider="ollama"))
    assert isinstance(provider, OllamaPlannerProvider)
    assert provider.base_url
    assert provider.model


def test_hf_provider_without_token_falls_back_to_heuristic() -> None:
    provider = build_provider(AppSettings(provider="hf_inference", hf_api_token=None))
    assert isinstance(provider, HeuristicPlannerProvider)


def test_hf_provider_with_token_selected() -> None:
    provider = build_provider(AppSettings(provider="hf_inference", hf_api_token="token"))
    assert isinstance(provider, HFInferencePlannerProvider)
