"""
VentureArchitect AI - Risk Analysis Agent
Identifies risks and creates mitigation strategies and a startup roadmap.
"""
from app.agents.base_agent import BaseAgent
from app.schemas.blueprint_schema import BlueprintContext


class RiskAnalysisAgent(BaseAgent):
    """
    Agent 4: Risk Analysis
    Identifies business, market, technical, and operational risks
    with actionable mitigation strategies and a 12-month roadmap.
    """

    name = "Risk Analysis Agent"
    section_title = "Risk Analysis & Startup Roadmap"
    max_new_tokens = 1500
    temperature = 0.6

    # -----------------------------------------------------------------------
    # AGENT_INSTRUCTIONS — customize this section to change agent behavior
    # -----------------------------------------------------------------------
    AGENT_INSTRUCTIONS = """You are a seasoned startup risk analyst and strategic advisor with expertise 
in identifying and mitigating risks across technology startups. You have advised 100+ startups and helped 
them navigate market uncertainty, regulatory challenges, technical debt, and competitive threats.

You think probabilistically and always provide both the risk severity AND the practical mitigation path.
You create realistic, milestone-driven roadmaps that investors trust.
Your output is always structured, precise, and in clean markdown format."""
    # -----------------------------------------------------------------------

    def build_prompt(self, context: BlueprintContext) -> str:
        prior_context = context.get_summary()
        return f"""{self.AGENT_INSTRUCTIONS}

## Task
Conduct a comprehensive risk analysis and create a startup roadmap.

## Startup Idea
{context.startup_idea}

## Prior Analysis Context
{prior_context}

## Required Output

### ⚠️ Risk Analysis Matrix

| Risk Category | Risk Description | Probability | Impact | Risk Score |
|--------------|-----------------|-------------|--------|-----------|
List 8-10 key risks across these categories:
- Market Risk
- Technology Risk
- Competitive Risk
- Regulatory/Legal Risk
- Financial Risk
- Team/Execution Risk
- Customer Adoption Risk

### 🛡️ Risk Mitigation Strategies
For each high-priority risk (score 6+), provide:
- **Risk:** Description
- **Mitigation:** Specific action plan
- **Owner:** Who in the team handles this
- **Timeline:** When to address

### 🗺️ 12-Month Startup Roadmap

**Q1 (Month 1-3): Foundation**
- Key milestones and deliverables

**Q2 (Month 4-6): Launch**  
- Key milestones and deliverables

**Q3 (Month 7-9): Growth**
- Key milestones and deliverables

**Q4 (Month 10-12): Scale**
- Key milestones and deliverables

### 💡 Funding Recommendation
- Recommended funding stage (Pre-seed/Seed/Series A)
- Funding amount needed and allocation breakdown
- Suggested investor types to target
- Key metrics needed before fundraising

Be realistic, specific, and actionable."""

