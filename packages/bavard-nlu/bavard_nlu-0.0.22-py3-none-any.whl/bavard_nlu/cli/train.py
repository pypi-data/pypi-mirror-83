import json

from bavard_nlu.model import NLUModel


def train(
    *,
    agent_data_file: str,
    saved_model_dir: str = None,
    auto: bool = False,
    **nlu_model_args
):
    """
    Parameters
    ----------
    agent_data_file : str
        Path to the agent data file to train on.
    saved_model_dir : str, optional
        If passed, the trained model will be saved at this path.
    auto : bool, optional
        Whether to have hyperparameters be automatically determined.
    **nlu_model_args : optional
        Any other arguments or hyperparameters to pass to NLUModel
        constructor. If `auto==True`, some of these values may be
        overridden.
    """
    with open(agent_data_file) as f:
        agent_data = json.load(f)

    model = NLUModel(
        agent_data=agent_data,
        max_seq_len=200,
        saved_model_dir=saved_model_dir,
        **nlu_model_args
    )
    model.build_and_compile_model()
    model.train(auto=auto)
