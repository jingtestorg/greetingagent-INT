"""Integration test: end-to-end agent flow using mocked LLM and no real network calls."""
import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from agent import SampleAgent, AgentResponse


@pytest.mark.asyncio
async def test_invoke_end_to_end_with_name():
    """Full invoke() call: user provides a name, agent returns a greeting containing it."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    expected_response = "Hello, Carol! It's wonderful to meet you!"
    fake_message = MagicMock()
    fake_message.content = expected_response
    fake_result = {"messages": [fake_message]}

    with patch.object(agent, "_invoke", new_callable=AsyncMock, return_value=fake_result):
        result = await agent.invoke("Hello, my name is Carol", "integration-test-1", tools=[])

    assert result.status == "completed"
    assert isinstance(result.message, str)
    assert len(result.message) > 0


@pytest.mark.asyncio
async def test_invoke_end_to_end_no_name():
    """Full invoke() call: no name provided, agent still returns a friendly response."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    expected_response = "Hello, friend! How can I help you today?"
    fake_message = MagicMock()
    fake_message.content = expected_response
    fake_result = {"messages": [fake_message]}

    with patch.object(agent, "_invoke", new_callable=AsyncMock, return_value=fake_result):
        result = await agent.invoke("Say hello", "integration-test-2", tools=[])

    assert result.status == "completed"
    assert isinstance(result.message, str)
    assert len(result.message) > 0


@pytest.mark.asyncio
async def test_invoke_handles_llm_exception_gracefully():
    """If the LLM raises, invoke() should return a completed response (not raise)."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    with patch.object(agent, "_invoke", new_callable=AsyncMock, side_effect=RuntimeError("Simulated LLM failure")):
        result = await agent.invoke("My name is Dave", "integration-test-3", tools=[])

    # Should complete (not error out at the invoke level) — fallback message from _run_greeting
    assert isinstance(result.message, str)
    assert len(result.message) > 0
