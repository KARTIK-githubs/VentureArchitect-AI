"""
VentureArchitect AI - Market Research Agent
Conducts deep market research based on the refined startup idea.
"""
from app.agents.base_agent import BaseAgent
from app.schemas.blueprint_schema import BlueprintContext


class MarketResearchAgent(BaseAgent):
    """
    Agent 2: Market Research
    Analyzes market size, trends, customer segments, and competitive landscape.
    """

    name = "Market Research Agent"
    section_title = "Market Research & Competitive Analysis"
    max_new_tokens = 1500
    temperature = 0.65

    # -----------------------------------------------------------------------
    # AGENT_INSTRUCTIONS — customize this section to change agent behavior
    # -----------------------------------------------------------------------
    AGENT_INSTRUCTIONS = """You are a world-class market research analyst and competitive intelligence expert 
with deep expertise in startup ecosystems, emerging technology trends, and global market dynamics. 
You have analyzed hundreds of markets for leading VC firms and Fortune 500 companies.

You produce data-driven, structured market research that investors rely on to make decisions.
You always cite market sizing methodologies (TAM/SAM/SOM) and ground your analysis in real industry context.
Your output is always in clean, professional markdown format."""
    # -----------------------------------------------------------------------

    def build_prompt(self, context: BlueprintContext) -> str:
        prior_context = context.get_summary()
        return f"""{self.AGENT_INSTRUCTIONS}

## Task
Conduct comprehensive market research for this startup.

## Startup Idea
{context.startup_idea}

## Prior Analysis Context
{prior_context}

## Required Output
Provide detailed market research in the following structure:

### 📊 Market Size & Opportunity
- **TAM (Total Addressable Market):** Estimated size with reasoning
- **SAM (Serviceable Addressable Market):** Realistic reachable market
- **SOM (Serviceable Obtainable Market):** Year 1-3 target market

### 📈 Industry Trends
5 major trends shaping this industry in the next 3-5 years.

### 🎯 Customer Segments
3-4 distinct customer personas with needs, pain points, and willingness to pay.

### ⚔️ Competitor Analysis
| Competitor | Type | Strengths | Weaknesses | Pricing |
|-----------|------|-----------|------------|---------|
Analyze 4-5 key competitors (direct and indirect).

### 🏆 Competitive Advantage
What unique positioning creates a defensible moat for this startup?

### 🌍 Market Entry Strategy
Which geographic market to target first and why?

Be specific with market data, percentages, and actionable insights."""

