from usetai_agentic_ai.providers.factory import build_provider
from usetai_agentic_ai.providers.heuristic import HeuristicPlannerProvider
from usetai_agentic_ai.settings import AppSettings


def test_default_provider_is_heuristic() -> None:
    provider = build_provider(AppSettings(provider="heuristic"))
    assert isinstance(provider, HeuristicPlannerProvider)
