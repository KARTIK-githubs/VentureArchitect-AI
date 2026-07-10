"""
VentureArchitect AI - Business Strategy Agent
Creates the full business model canvas, revenue strategy, pricing, and GTM plan.
"""
from app.agents.base_agent import BaseAgent
from app.schemas.blueprint_schema import BlueprintContext


class BusinessStrategyAgent(BaseAgent):
    """
    Agent 3: Business Strategy
    Designs business model canvas, revenue streams, pricing strategy,
    and go-to-market plan.
    """

    name = "Business Strategy Agent"
    section_title = "Business Strategy & Model"
    max_new_tokens = 1800
    temperature = 0.65

    # -----------------------------------------------------------------------
    # AGENT_INSTRUCTIONS — customize this section to change agent behavior
    # -----------------------------------------------------------------------
    AGENT_INSTRUCTIONS = """You are a senior business strategist and growth consultant who has helped 
50+ startups from ideation to Series B funding. You have deep expertise in business model design, 
SaaS economics, marketplace dynamics, and go-to-market strategy.

You think like a McKinsey partner but write like a founder — practical, direct, and actionable.
You always build strategies that are executable within limited startup resources.
Your output is always in clean, professional markdown format with concrete numbers and timelines."""
    # -----------------------------------------------------------------------

    def build_prompt(self, context: BlueprintContext) -> str:
        prior_context = context.get_summary()
        return f"""{self.AGENT_INSTRUCTIONS}

## Task
Design a comprehensive business strategy for this startup.

## Startup Idea
{context.startup_idea}

## Prior Analysis Context
{prior_context}

## Required Output

### 🏗️ Business Model Canvas
Cover all 9 building blocks:
1. **Customer Segments** - Who are you serving?
2. **Value Propositions** - What value do you deliver?
3. **Channels** - How do you reach customers?
4. **Customer Relationships** - How do you acquire and retain?
5. **Revenue Streams** - How do you make money?
6. **Key Resources** - What do you need?
7. **Key Activities** - What must you do?
8. **Key Partnerships** - Who helps you?
9. **Cost Structure** - What are the major costs?

### 💰 Revenue Strategy
Primary and secondary revenue streams with realistic Year 1, Year 2, Year 3 projections.

### 💵 Pricing Strategy
Recommended pricing model (subscription/freemium/usage-based/etc.) with specific price points.
Include a pricing tier table.

### 🚀 Go-To-Market Strategy
**Phase 1 (Month 1-3):** Early adopter acquisition tactics
**Phase 2 (Month 4-6):** Growth acceleration tactics  
**Phase 3 (Month 7-12):** Scale and expansion tactics

### 📊 Unit Economics
Key metrics: CAC, LTV, LTV:CAC ratio, Payback period, Gross Margin targets.

### 🤝 Partnership Strategy
3 strategic partnerships to accelerate growth.

Be specific with tactics, channels, and projected numbers."""

