"""
VentureArchitect AI - IBM watsonx.ai LLM Service
Reusable client that all agents use to communicate with IBM watsonx.ai.
"""
import logging
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextGenParameters

logger = logging.getLogger(__name__)


class WatsonXService:
    """
    Singleton-style LLM service wrapping IBM watsonx.ai.
    All agents call generate() through this shared client.

    Key design: one APIClient is created at init time (one IAM token fetch).
    ModelInference is built once per unique model_id and reused across all
    agent calls — avoids 5 separate IAM token requests during the pipeline.
    """

    def __init__(self, api_key: str, project_id: str, url: str):
        if not api_key or not project_id:
            raise ValueError("IBM_API_KEY and IBM_PROJECT_ID must be set in environment variables.")
        # Strip whitespace that causes 404 "Cannot set Project or Space"
        self.project_id = project_id.strip()
        clean_url = url.rstrip("/")
        logger.info("[WATSONX] Initializing. project_id=%s url=%s",
                    self.project_id[:8] + "...", clean_url)

        logger.info("[WATSONX] Creating Credentials object...")
        credentials = Credentials(api_key=api_key, url=clean_url)
        logger.info("[WATSONX] Credentials created.")

        # SDK 1.5.14: pass project_id directly to APIClient so it becomes the
        # default project on the client. ModelInference then receives only
        # api_client= (no project_id=), avoiding a second set.default_project()
        # mutation and a redundant network validation call.
        logger.info("[WATSONX] Building APIClient with project_id (IAM token fetch happens here)...")
        self._api_client = APIClient(credentials=credentials, project_id=self.project_id)
        logger.info("[WATSONX] APIClient ready. default_project_id=%s",
                    getattr(self._api_client, 'default_project_id', 'unknown'))

        # Cache of model_id -> ModelInference so agents share the same instance
        self._model_cache: dict[str, ModelInference] = {}
        logger.info("[WATSONX] WatsonXService initialized successfully.")

    def _get_model(self, model_id: str) -> ModelInference:
        """Return a cached ModelInference for model_id, building it if needed."""
        if model_id not in self._model_cache:
            logger.info("[WATSONX] Building ModelInference for model_id=%s", model_id)
            # SDK 1.5.14:
            # - Pass api_client= only (project_id already set on APIClient above).
            # - Do NOT pass project_id= here: that would call set.default_project()
            #   again on the shared client, triggering another network validation.
            # - validate=False: skips the blocking model-existence check at
            #   construction time. Any bad model_id surfaces as a clear error on
            #   the actual generate_text() call instead of hanging silently here.
            logger.info("[WATSONX] Calling ModelInference() constructor (validate=False, no network call)...")
            self._model_cache[model_id] = ModelInference(
                model_id=model_id,
                api_client=self._api_client,
                validate=False,
            )
            logger.info("[WATSONX] ModelInference built and cached for model_id=%s", model_id)
        else:
            logger.info("[WATSONX] Reusing cached ModelInference for model_id=%s", model_id)
        return self._model_cache[model_id]

    def generate(
        self,
        prompt: str,
        model_id: str = "meta-llama/llama-3-3-70b-instruct",
        max_new_tokens: int = 1500,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        repetition_penalty: float = 1.1,
    ) -> str:
        """
        Send a prompt to IBM watsonx.ai and return the generated text.

        Args:
            prompt: The input prompt string.
            model_id: IBM Granite model identifier.
            max_new_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling probability.
            top_k: Top-k sampling.
            repetition_penalty: Penalty for repeated tokens.

        Returns:
            Generated text string.
        """
        logger.info("[WATSONX] generate() called. model_id=%s max_new_tokens=%d prompt_length=%d",
                    model_id, max_new_tokens, len(prompt))
        try:
            # SDK 1.5.x: use typed TextGenParameters instead of a raw GenParams dict.
            # Field names match the resolved GenParams string values exactly.
            params = TextGenParameters(
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
            )
            logger.info("[WATSONX] TextGenParameters: max_new_tokens=%d temperature=%s top_p=%s top_k=%s repetition_penalty=%s",
                        max_new_tokens, temperature, top_p, top_k, repetition_penalty)

            model = self._get_model(model_id)

            logger.info("[WATSONX] Calling model.generate_text()... (blocking until IBM responds)")
            # validate_prompt_variables=False: prevents the SDK raising
            # InvalidPromptVariables if the prompt contains {{ }} patterns
            # (common in JSON examples inside agent prompts).
            response = model.generate_text(
                prompt=prompt,
                params=params,
                guardrails=False,
            )
            logger.info("[WATSONX] model.generate_text() returned. response_type=%s response_length=%d",
                        type(response).__name__, len(response) if response else 0)

            result = response.strip() if response else ""
            logger.info("[WATSONX] generate() complete. returning %d chars", len(result))
            return result

        except Exception as exc:
            logger.error("[WATSONX] generate() EXCEPTION: %s", exc, exc_info=True)
            raise RuntimeError(f"LLM generation failed: {exc}") from exc


# Module-level singleton — initialized lazily in create_app()
_service_instance: WatsonXService | None = None


def init_watsonx_service(api_key: str, project_id: str, url: str) -> WatsonXService:
    """Create and cache the singleton WatsonXService instance."""
    global _service_instance
    _service_instance = WatsonXService(api_key=api_key, project_id=project_id, url=url)
    return _service_instance


def get_watsonx_service() -> WatsonXService:
    """Retrieve the cached WatsonXService instance."""
    if _service_instance is None:
        raise RuntimeError("WatsonXService has not been initialized. Call init_watsonx_service() first.")
    return _service_instance
