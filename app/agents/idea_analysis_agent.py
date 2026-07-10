"""
VentureArchitect AI - Idea Analysis Agent
Analyzes the raw startup idea and produces structured problem/solution framing.
"""
from app.agents.base_agent import BaseAgent
from app.schemas.blueprint_schema import BlueprintContext


class IdeaAnalysisAgent(BaseAgent):
    """
    Agent 1: Idea Analysis
    Transforms the raw startup idea into a refined startup concept with
    problem statement, target audience, value proposition, and key features.
    """

    name = "Idea Analysis Agent"
    section_title = "Startup Idea Analysis"
    max_new_tokens = 1500
    temperature = 0.7

    # -----------------------------------------------------------------------
    # AGENT_INSTRUCTIONS — customize this section to change agent behavior
    # -----------------------------------------------------------------------
    AGENT_INSTRUCTIONS = """You are an expert startup idea analyst and product strategist with 15+ years of experience 
evaluating and refining startup concepts at top-tier venture capital firms. Your role is to take a raw startup idea 
and transform it into a clearly articulated, investor-ready concept.

You analyze ideas with the critical eye of a seasoned entrepreneur combined with the market intuition of a top VC.
You are concise, structured, and always output in clean markdown format.
You focus on clarity, differentiation, and real-world viability."""
    # -----------------------------------------------------------------------

    def build_prompt(self, context: BlueprintContext) -> str:
        return f"""{self.AGENT_INSTRUCTIONS}

## Task
Analyze the following startup idea and produce a comprehensive idea analysis.

## Startup Idea
{context.startup_idea}

## Required Output
Provide a detailed analysis in the following structure (use markdown headers):

### 🎯 Refined Startup Concept
A one-paragraph polished description of the startup idea.

### 🔥 Problem Statement
What specific problem does this startup solve? Who suffers from this problem and how acutely?

### 👥 Target Audience
Primary and secondary target audiences. Include demographics, psychographics, and behavioral traits.

### 💎 Value Proposition
The core unique value delivered. What makes this solution 10x better than alternatives?

### ⚡ Key Features
List 5-7 core product features that deliver the value proposition. Be specific.

### 🌟 Startup Name Suggestion
Suggest 3 creative startup names with a brief rationale for each.

Be specific, insightful, and actionable. Avoid generic statements."""

