"""
VentureArchitect AI - Flask Routes
"""
import logging
from flask import Blueprint, render_template, request, jsonify, current_app
from app.agents.supervisor_agent import SupervisorAgent
from app.schemas.blueprint_schema import AgentResult, BlueprintContext
from app.services.watsonx_service import get_watsonx_service

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------------------------------
# Page Routes
# ---------------------------------------------------------------------------

@main_bp.route("/")
def index():
    """Landing page / main application page."""
    return render_template("index.html")


@main_bp.route("/blueprint")
def blueprint_page():
    """Blueprint results page."""
    return render_template("blueprint.html")


@main_bp.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "app": current_app.config.get("APP_NAME", "VentureArchitect AI")})


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@api_bp.route("/generate", methods=["POST"])
def generate_blueprint():
    """
    POST /api/generate
    Body: { "startup_idea": "..." }
    Returns: Full blueprint JSON with all agent results.
    """
    logger.info("[ROUTE] POST /api/generate received")

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("startup_idea"), str):
        logger.warning("[ROUTE] Request rejected: missing startup_idea")
        return jsonify({"success": False, "error": "startup_idea is required."}), 400

    startup_idea = data["startup_idea"].strip()
    logger.info("[ROUTE] startup_idea length=%d, preview=%.80r", len(startup_idea), startup_idea)

    if len(startup_idea) < 10:
        return jsonify({"success": False, "error": "Please provide a more detailed startup idea (at least 10 characters)."}), 400

    if len(startup_idea) > 2000:
        return jsonify({"success": False, "error": "Startup idea must be under 2000 characters."}), 400

    try:
        logger.info("[ROUTE] Creating SupervisorAgent and starting pipeline...")
        supervisor = SupervisorAgent()
        try:
            get_watsonx_service()
        except RuntimeError:
            blueprint_context = build_offline_blueprint(startup_idea, supervisor.PIPELINE)
        else:
            blueprint_context = supervisor.run(startup_idea=startup_idea)
        result = blueprint_context.to_dict()
        sections_ok = sum(1 for s in result.get("sections", []) if s.get("success"))
        logger.info("[ROUTE] Pipeline complete. sections_total=%d sections_ok=%d",
                    len(result.get("sections", [])), sections_ok)
        return jsonify({"success": True, "blueprint": result}), 200

    except RuntimeError as exc:
        error_msg = str(exc)
        logger.error("[ROUTE] RuntimeError from pipeline: %s", error_msg, exc_info=True)
        return jsonify({"success": False, "error": error_msg}), 500

    except Exception as exc:
        error_msg = str(exc)
        logger.error("[ROUTE] Unexpected exception: %s", error_msg, exc_info=True)
        return jsonify({"success": False, "error": f"Generation error: {error_msg}"}), 500


def build_offline_blueprint(startup_idea, pipeline):
    """Return a clearly labeled planning worksheet without provider credentials."""
    context = BlueprintContext(startup_idea=startup_idea)
    exercises = (
        "Write down who experiences the problem, when it happens, and how they solve it today. Interview three people and revise the problem statement from their answers.",
        "List three alternatives your customers already use. Compare their price, accessibility and main limitation. Verify each claim before using it in a pitch.",
        "Pick one customer segment and one outcome. Define the smallest useful trial, the cost to deliver it, and how you will measure repeat use.",
        "List the assumptions that would stop the project if they were false. Give each assumption a low-cost test, an owner, and a deadline.",
        "Draft a short pitch with the audience, problem, proposed solution, evidence gathered so far, and the next decision or resource you need.",
    )
    for agent_class, exercise in zip(pipeline, exercises):
        agent = agent_class()
        context.add_result(AgentResult(
            agent_name=agent.name,
            section_title=agent.section_title,
            content="Offline planning worksheet (no AI provider configured). " + exercise,
            success=True,
        ))
    return context


@api_bp.route("/agents", methods=["GET"])
def list_agents():
    """Return metadata about all available agents."""
    from app.agents import (
        IdeaAnalysisAgent, MarketResearchAgent, BusinessStrategyAgent,
        RiskAnalysisAgent, InvestorPitchAgent
    )
    agents = [
        IdeaAnalysisAgent, MarketResearchAgent, BusinessStrategyAgent,
        RiskAnalysisAgent, InvestorPitchAgent
    ]
    return jsonify({
        "agents": [
            {"name": a.name, "section_title": a.section_title, "order": i + 1}
            for i, a in enumerate(agents)
        ]
    })
