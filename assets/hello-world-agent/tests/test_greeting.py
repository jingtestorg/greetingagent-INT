"""Unit tests for the greeting logic — name extraction and LLM call."""
import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# app/ is added to sys.path by conftest.py fixture
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from agent import SampleAgent


class TestNameExtraction:
    def setup_method(self):
        with patch("agent.create_checkpointer"):
            self.agent = SampleAgent.__new__(SampleAgent)

    def test_extracts_name_from_my_name_is(self):
        name = self.agent._extract_name("Hello, my name is Alice")
        assert name == "Alice"

    def test_extracts_name_from_i_am(self):
        name = self.agent._extract_name("I am Bob")
        assert name == "Bob"

    def test_extracts_name_from_im(self):
        name = self.agent._extract_name("I'm Charlie")
        assert name == "Charlie"

    def test_extracts_name_from_call_me(self):
        name = self.agent._extract_name("Call me Diana")
        assert name == "Diana"

    def test_extracts_name_case_insensitive(self):
        name = self.agent._extract_name("MY NAME IS Eve")
        assert name == "Eve"

    def test_returns_empty_when_no_name(self):
        name = self.agent._extract_name("Just say hello")
        assert name == ""

    def test_returns_empty_for_empty_string(self):
        name = self.agent._extract_name("")
        assert name == ""
