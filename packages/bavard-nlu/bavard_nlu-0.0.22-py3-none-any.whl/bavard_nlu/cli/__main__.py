from fire import Fire

from bavard_nlu.cli.evaluate import evaluate
from bavard_nlu.cli.predict import predict
from bavard_nlu.cli.train import train


if __name__ == '__main__':
    Fire({
        "evaluate": evaluate,
        "predict": predict,
        "train": train,
    })
