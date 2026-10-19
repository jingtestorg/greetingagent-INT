"""Unit tests for the default (no-name) greeting path."""
import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from agent import SampleAgent


@pytest.mark.asyncio
async def test_run_greeting_with_name():
    """When a name is present, the greeting response is returned."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    fake_message = MagicMock()
    fake_message.content = "Hello, Alice! Great to meet you!"
    fake_result = {"messages": [fake_message]}

    with patch.object(agent, "_invoke", new_callable=AsyncMock, return_value=fake_result):
        response = await agent._run_greeting("Hello, my name is Alice", "ctx-1", [])

    assert "Alice" in response or "Hello" in response


@pytest.mark.asyncio
async def test_run_greeting_without_name_uses_default():
    """When no name is found, the agent still returns a response (using 'friend' default)."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    fake_message = MagicMock()
    fake_message.content = "Hello, friend! How can I help you today?"
    fake_result = {"messages": [fake_message]}

    with patch.object(agent, "_invoke", new_callable=AsyncMock, return_value=fake_result):
        response = await agent._run_greeting("Just say hello", "ctx-2", [])

    assert response != ""
    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_run_greeting_llm_failure_returns_fallback():
    """When the LLM call fails, a graceful fallback greeting is returned."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    with patch.object(agent, "_invoke", new_callable=AsyncMock, side_effect=RuntimeError("LLM error")):
        response = await agent._run_greeting("My name is Bob", "ctx-3", [])

    # Should return a fallback string, not raise
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_stream_yields_completed():
    """stream() should yield a final chunk with is_task_complete=True."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    with patch.object(agent, "_run_greeting", new_callable=AsyncMock, return_value="Hi Alice!"):
        chunks = []
        async for chunk in agent.stream("My name is Alice", "ctx-4", tools=[]):
            chunks.append(chunk)

    # Must have at least two chunks: "Processing..." and the final result
    assert len(chunks) >= 2
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "Alice" in final["content"] or final["content"] != ""


@pytest.mark.asyncio
async def test_stream_yields_processing_first():
    """stream() must emit a 'Processing...' status before the final result."""
    with patch("agent.create_checkpointer", return_value=None), \
         patch("agent.ChatLiteLLM"), \
         patch("agent.SummarizationMiddleware"):
        agent = SampleAgent()

    with patch.object(agent, "_run_greeting", new_callable=AsyncMock, return_value="Hello!"):
        chunks = []
        async for chunk in agent.stream("Hi", "ctx-5", tools=[]):
            chunks.append(chunk)

    first = chunks[0]
    assert first["is_task_complete"] is False
    assert first["content"] == "Processing..."
