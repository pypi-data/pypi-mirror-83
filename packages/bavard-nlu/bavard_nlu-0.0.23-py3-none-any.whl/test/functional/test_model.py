import json
import shutil
from unittest import TestCase
from pathlib import Path

from bavard_nlu.model import NLUModel
from bavard_nlu.data_preprocessing.prediction_input import PredictionInput


class TestModel(TestCase):
    def setUp(self):
        super().setUp()
        self.max_seq_len = 200
        self.tokenizer = NLUModel.get_tokenizer()
        self.model_save_dir = "test-model"
        self.max_model_size_in_gigabytes = 2
        # Translations of the same utterance
        self.prediction_inputs = {
            "eng": "how much is a flight from washington to boston",
            "chi": "从华盛顿飞往波士顿多少钱",
            "rus": "сколько стоит перелет из вашингтона в бостон",
            "spa": "¿Cuánto cuesta un vuelo de Washington a Boston?",
            "fre": "Combien est un vol de Washington à Boston"
        }
        with open("test_data/test-agent.json") as f:
            self.agent_data = json.load(f)
    
    def tearDown(self):
        shutil.rmtree(self.model_save_dir)
    
    def test_train_and_predict(self):
        # Check that model can build and train without failing.
        model = NLUModel(self.agent_data, self.max_seq_len, self.model_save_dir)
        model.build_and_compile_model()
        model.train(batch_size=1, epochs=1)

        # Check that the saved model is small enough
        saved_model_size = self._get_dir_size(self.model_save_dir, "GB")
        self.assertLessEqual(saved_model_size, self.max_model_size_in_gigabytes)

        # Check that model can handle multiple languages without breaking.
        self._assert_model_can_predict(model)
        
        # Check that the model can be successfully loaded
        loaded_model = NLUModel(self.agent_data, self.max_seq_len, self.model_save_dir, load_model=True)
        self._assert_model_can_predict(loaded_model)

    def _predict(self, model: NLUModel, utterance: str) -> tuple:
        """
        Wraps `NLUModel.predict` to decode the predictions as well.
        """
        raw_intent_pred, raw_tags_pred = model.predict(
            utterance,
            self.tokenizer
        )
        intent_dict = model.decode_intent(raw_intent_pred)
        pred_input = PredictionInput(utterance, self.max_seq_len, self.tokenizer)
        tags = model.decode_tags(raw_tags_pred, utterance, pred_input.word_start_mask)
        return intent_dict["value"], tags
    
    def _assert_model_can_predict(self, model: NLUModel) -> None:
        for utterance in self.prediction_inputs.values():
            intent, tags = self._predict(model, utterance)
            self.assertIn(intent, self.agent_data["nluData"]["intents"])
            for tag in tags:
                self.assertIn(tag["tag_type"], self.agent_data["nluData"]["tagTypes"])

    def _get_dir_size(self, dir: str, units: str = "GB") -> int:
        """
        Gets the size of the directory at `path`.
        Source: https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
        """
        units_map = {"KB": 1e-3, "MB": 1e-6, "GB": 1e-9}
        path = Path(dir)
        total_bytes = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
        return total_bytes * units_map[units]
