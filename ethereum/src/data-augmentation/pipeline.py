import logging

import generate
import compile
from params import PipelineParams

logger = logging.getLogger(__name__)


def run(params: PipelineParams) -> None:
    logger.info("Starting pipeline")
    logger.info("Parameters:")
    logger.info("  few_shot_k   = %d", params.few_shot_k)
    logger.info("  random_seed  = %d", params.random_seed)
    logger.info("  model        = %s", params.model)
    logger.info("  temperature  = %.2f", params.temperature)
    logger.info("  top_p        = %.2f", params.top_p)
    logger.info("  top_k        = %d", params.top_k)
    logger.info("  n_samples    = %d", params.n_samples)
    logger.info("  max_tokens   = %d", params.max_tokens)

    generate.run(params)
    compile.run(params)

    logger.info("Pipeline complete")
