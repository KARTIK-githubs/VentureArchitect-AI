"""
VentureArchitect AI - Supervisor Agent
Orchestrates all five agents in sequence, passing context between them.
"""
import logging
from typing import Callable, Optional
from app.agents.idea_analysis_agent import IdeaAnalysisAgent
from app.agents.market_research_agent import MarketResearchAgent
from app.agents.business_strategy_agent import BusinessStrategyAgent
from app.agents.risk_analysis_agent import RiskAnalysisAgent
from app.agents.investor_pitch_agent import InvestorPitchAgent
from app.schemas.blueprint_schema import BlueprintContext, AgentResult

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Supervisor Agent — Orchestrates the complete VentureArchitect AI pipeline.

    Execution order:
        1. IdeaAnalysisAgent
        2. MarketResearchAgent
        3. BusinessStrategyAgent
        4. RiskAnalysisAgent
        5. InvestorPitchAgent

    Context flows from each agent into the next, building an ever-richer
    blueprint that later agents can reference.

    The progress_callback, if provided, receives (agent_index, agent_name, status)
    after each agent completes.
    """

    PIPELINE = [
        IdeaAnalysisAgent,
        MarketResearchAgent,
        BusinessStrategyAgent,
        RiskAnalysisAgent,
        InvestorPitchAgent,
    ]

    def run(
        self,
        startup_idea: str,
        progress_callback: Optional[Callable[[int, str, str], None]] = None,
    ) -> BlueprintContext:
        """
        Execute the full agent pipeline for the given startup idea.

        Args:
            startup_idea: The raw startup idea provided by the user.
            progress_callback: Optional callable(index, agent_name, status)
                               called after each agent. status is 'running',
                               'done', or 'error'.

        Returns:
            BlueprintContext containing all agent results.
        """
        logger.info("[SUPERVISOR] Pipeline starting. idea_length=%d preview=%.80r",
                    len(startup_idea), startup_idea)
        context = BlueprintContext(startup_idea=startup_idea)

        for i, AgentClass in enumerate(self.PIPELINE):
            agent = AgentClass()
            logger.info("[SUPERVISOR] Dispatching agent %d/%d: %s", i + 1, len(self.PIPELINE), agent.name)

            if progress_callback:
                progress_callback(i, agent.name, "running")

            result: AgentResult = agent.run(context)
            context.add_result(result)

            status = "done" if result.success else "error"
            logger.info("[SUPERVISOR] Agent %s finished. status=%s content_length=%d",
                        agent.name, status, len(result.content) if result.content else 0)

            if progress_callback:
                progress_callback(i, agent.name, status)

            if not result.success:
                logger.warning("[SUPERVISOR] Agent %s reported error (pipeline continues): %s",
                               agent.name, result.error)

        logger.info("[SUPERVISOR] Pipeline complete. total_sections=%d", len(context.results))
        return context
