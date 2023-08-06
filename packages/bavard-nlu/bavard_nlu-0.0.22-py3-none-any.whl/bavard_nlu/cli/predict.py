import json

from bavard_nlu.data_preprocessing.prediction_input import PredictionInput

from bavard_nlu.model import NLUModel


def predict_one(model: NLUModel, text: str) -> dict:
    tokenizer = model.get_tokenizer()
    raw_prediction = model.predict(text=text, tokenizer=tokenizer)
    raw_intent_pred = raw_prediction[0]
    raw_tags_pred = raw_prediction[1]
    pred_input = PredictionInput(text, 200, tokenizer)
    intent = model.decode_intent(raw_intent_pred)
    tags = model.decode_tags(raw_tags_pred, text, pred_input.word_start_mask)
    return {"intent": intent, "tags": tags}


def predict(
    *,
    agent_data_file: str,
    model_dir: str,
    batch_file: str = None,
    interactive: bool = False
):
    """
    Parameters
    ----------
    agent_data_file : str
        Path to the agent data file the model was trained on.
    model_dir : str
        Path to the saved model that will be loaded.
    batch_file : str, optional
        Pass this file path to predict on a file of text; one prediction per line.
    interactive : bool, optional
        If supplied, interact with the model, providing inputs for prediction via CLI.
    """
    with open(agent_data_file) as f:
        agent_data = json.load(f)

    model = NLUModel(
        agent_data=agent_data,
        max_seq_len=200,
        saved_model_dir=model_dir,
        load_model=True
    )
    if batch_file:
        with open(batch_file) as f:
            for utterance in f:
                utterance = utterance.replace("\n", "")
                print(utterance)
                print(predict_one(model, utterance))
    
    if interactive:
        quits = {"q", "quit", "exit"}
        utterance = ""
        while True:
            utterance = input("\nEnter your utterance ('q' to quit) >>> ")
            if utterance in quits:
                break
            print(predict_one(model, utterance))
