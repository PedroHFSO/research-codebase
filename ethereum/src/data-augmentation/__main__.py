import logging
import os
import time

from form import PipelineForm
import pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
)

if __name__ == "__main__":
    params = PipelineForm().run()
    if params is not None:
        os.system("cls")
        time.sleep(1)
        pipeline.run(params)
