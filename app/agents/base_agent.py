"""
VentureArchitect AI - Base Agent
All agents inherit from this class.
"""
import logging
from abc import ABC, abstractmethod
from app.services.watsonx_service import get_watsonx_service
from app.schemas.blueprint_schema import AgentResult, BlueprintContext

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all VentureArchitect AI agents.

    Subclasses must define:
        - name (str): Human-readable agent name
        - section_title (str): Title shown in the blueprint
        - AGENT_INSTRUCTIONS (str): The system-level instructions / persona prompt
        - build_prompt(context) -> str: Constructs the full prompt
    """

    name: str = "BaseAgent"
    section_title: str = "Section"
    model_id: str = "meta-llama/llama-3-3-70b-instruct"
    max_new_tokens: int = 1500
    temperature: float = 0.7

    AGENT_INSTRUCTIONS: str = "You are a helpful AI assistant."

    @abstractmethod
    def build_prompt(self, context: BlueprintContext) -> str:
        """Build the full prompt to send to the LLM."""

    def run(self, context: BlueprintContext) -> AgentResult:
        """
        Execute the agent: build the prompt, call the LLM, return an AgentResult.
        """
        logger.info("[AGENT:%s] Starting", self.name)
        try:
            logger.info("[AGENT:%s] Building prompt...", self.name)
            prompt = self.build_prompt(context)
            logger.info("[AGENT:%s] Prompt built. length=%d chars", self.name, len(prompt))

            logger.info("[AGENT:%s] Getting WatsonXService...", self.name)
            service = get_watsonx_service()

            logger.info("[AGENT:%s] Calling service.generate() model=%s max_tokens=%d",
                        self.name, self.model_id, self.max_new_tokens)
            content = service.generate(
                prompt=prompt,
                model_id=self.model_id,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
            )
            logger.info("[AGENT:%s] service.generate() returned. response_length=%d chars",
                        self.name, len(content) if content else 0)

            result = AgentResult(
                agent_name=self.name,
                section_title=self.section_title,
                content=content,
                success=True,
            )
            logger.info("[AGENT:%s] Completed successfully.", self.name)
            return result

        except Exception as exc:
            logger.error("[AGENT:%s] FAILED: %s", self.name, exc, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                section_title=self.section_title,
                content="",
                success=False,
                error=str(exc),
            )
