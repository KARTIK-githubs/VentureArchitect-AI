"""
VentureArchitect AI - Agent Schemas / Data Structures
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentResult:
    """Standardized output from every agent."""
    agent_name: str
    section_title: str
    content: str
    success: bool = True
    error: Optional[str] = None


@dataclass
class BlueprintContext:
    """
    Shared context object passed between agents.
    Each agent reads prior results and appends its own.
    """
    startup_idea: str
    results: list = field(default_factory=list)

    def get_summary(self) -> str:
        """Return a condensed summary of all prior agent outputs for context injection."""
        if not self.results:
            return ""
        parts = []
        for result in self.results:
            if result.success:
                parts.append(f"## {result.section_title}\n{result.content}")
        return "\n\n".join(parts)

    def add_result(self, result: AgentResult):
        self.results.append(result)

    def to_dict(self) -> dict:
        return {
            "startup_idea": self.startup_idea,
            "sections": [
                {
                    "agent": r.agent_name,
                    "title": r.section_title,
                    "content": r.content,
                    "success": r.success,
                    "error": r.error,
                }
                for r in self.results
            ],
        }
