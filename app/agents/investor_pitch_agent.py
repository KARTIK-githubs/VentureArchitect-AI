"""
VentureArchitect AI - Investor Pitch Agent
Creates the elevator pitch and complete investor summary.
"""
from app.agents.base_agent import BaseAgent
from app.schemas.blueprint_schema import BlueprintContext


class InvestorPitchAgent(BaseAgent):
    """
    Agent 5: Investor Pitch
    Synthesizes all prior analysis into a compelling elevator pitch
    and investor-ready summary document.
    """

    name = "Investor Pitch Agent"
    section_title = "Investor Pitch & Summary"
    max_new_tokens = 1800
    temperature = 0.75

    # -----------------------------------------------------------------------
    # AGENT_INSTRUCTIONS — customize this section to change agent behavior
    # -----------------------------------------------------------------------
    AGENT_INSTRUCTIONS = """You are an elite pitch coach and startup storyteller who has helped founders 
raise over $500M in venture capital. You have sat on both sides of the table — as a founder who raised 
from Sequoia and a16z, and as a VC partner at top-tier funds.

You craft pitches that make investors lean forward in their seats. You know exactly what VCs want to hear,
what questions they will ask, and how to pre-emptively address objections.
You combine data with narrative to create compelling, memorable pitches.
Your output is always polished, concise, and investor-ready markdown."""
    # -----------------------------------------------------------------------

    def build_prompt(self, context: BlueprintContext) -> str:
        prior_context = context.get_summary()
        return f"""{self.AGENT_INSTRUCTIONS}

## Task
Create a compelling investor pitch and complete startup summary.

## Startup Idea
{context.startup_idea}

## Complete Prior Analysis
{prior_context}

## Required Output

### 🎤 60-Second Elevator Pitch
A polished, compelling 60-second verbal pitch (approximately 150-180 words).
Format it like a founder would actually deliver it to an investor.

### 📋 One-Page Investor Summary

**Company Overview**
Name, tagline, one-liner description.

**The Problem**
The problem being solved and its magnitude.

**The Solution**
How this startup solves it uniquely.

**Market Opportunity**
TAM/SAM/SOM with the market growth rate.

**Business Model**
How the company makes money.

**Traction & Milestones**
Key milestones achieved or planned.

**Competitive Advantage**
The unique moat.

**Team Requirements**
Ideal founding team composition.

**Financial Ask**
Funding amount, use of funds, and key milestones to hit.

### ❓ Investor FAQ — Pre-empting Hard Questions
List the top 5 tough questions investors will ask with strong, honest answers.

### 🏆 Why This Will Win
A 3-paragraph closing argument for why this startup will succeed and why now is the perfect time.

### 💼 Complete Startup Blueprint Summary
Synthesize everything into a 5-bullet executive summary that captures the entire opportunity.

Make this compelling, memorable, and investor-ready."""

