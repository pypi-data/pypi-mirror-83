import logging
from datetime import datetime
from typing import List, Optional, Sequence, Dict
from functools import reduce
from time import time

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Input, Dense, TimeDistributed, Dropout, Lambda, BatchNormalization, Activation
from tensorflow.keras import regularizers, Model
from transformers import TFDistilBertModel, DistilBertTokenizerFast
import tensorflow_probability as tfp
import uncertainty_metrics.tensorflow as um

from bavard_nlu.data_preprocessing.data_preprocessor import DataPreprocessor
from bavard_nlu.data_preprocessing.prediction_input import PredictionInput
from bavard_nlu.utils import aggregate_dicts, leave_one_out
from bavard_nlu.auto_setup import AutoSetup


logging.getLogger().setLevel(logging.DEBUG)


class NLUModel:

    # Always predict on larger batches, for efficiency's sake,
    # since it doesn't affect the model's optimization.
    batch_size_predict = 64
    embedder_name = 'distilbert-base-multilingual-cased'
    hpnames = [
        "hidden_size",
        "dropout",
        "l2_regularization",
        "hidden_activation",
        "n_hidden_layers",
        "fine_tune_embedder",
        "learning_rate",
        "batch_size",
        "epochs",
    ]

    def __init__(
        self,
        agent_data: dict,
        max_seq_len: int,
        saved_model_dir: Optional[str] = None,
        load_model: bool = False,
        verbose: bool = False,
        *,
        hidden_size: int = 256,
        dropout: float = 0.1,
        l2_regularization: float = 0.0,
        hidden_activation: str = "relu",
        n_hidden_layers: int = 0,
        fine_tune_embedder: bool = True,
        learning_rate: float = 5e-5,
        batch_size: int = 4,
        epochs: int = 30,
    ):
        self.agent_data = agent_data
        intents = self.agent_data['nluData']['intents']
        tag_types = self.agent_data['nluData']['tagTypes']

        self.intents = sorted(intents)
        self.tag_types = sorted(tag_types)
        self.max_seq_len = max_seq_len
        self.save_model_dir = saved_model_dir
        self.verbose = verbose

        # intents encoder
        self.intents_encoder = LabelEncoder()
        self.intents_encoder.fit(self.intents)

        # tags encoder
        tag_set = {'[CLS]', '[SEP]', 'O'}
        for tag_type in tag_types:
            tag_set.add(f'B-{tag_type}')
            tag_set.add(f'I-{tag_type}')
        self.tag_encoder = LabelEncoder()
        self.tag_encoder.fit(list(tag_set))

        # tag and intent sizes
        self.n_tags = len(tag_set)
        self.n_intents = len(intents)

        self.model = None
        
        # Set hyperparameters
        self.hidden_size = hidden_size
        self.dropout = dropout
        self.l2_regularization = l2_regularization
        self.hidden_activation = hidden_activation
        self.n_hidden_layers = n_hidden_layers
        self.fine_tune_embedder = fine_tune_embedder
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs

        if load_model:
            self.model = tf.keras.models.load_model(saved_model_dir)
            self._compile_model()

    @staticmethod
    def get_embedder(*, trainable: bool = False) -> tf.keras.Model:
        # TODO: Shouldn't have to access the underlying `.distilbert` layer once
        # https://github.com/huggingface/transformers/issues/3627 is resolved.
        embedder = TFDistilBertModel.from_pretrained(NLUModel.embedder_name).distilbert
        embedder.trainable = trainable
        return embedder

    @staticmethod
    def get_tokenizer() -> DistilBertTokenizerFast:
        return DistilBertTokenizerFast.from_pretrained(NLUModel.embedder_name)
    
    def get_params(self) -> dict:
        """
        Get a copy of the model's hyperparameters as a dictionary.
        """
        return {name: getattr(self, name) for name in self.hpnames}
    
    def set_params(self, **params) -> None:
        """
        Sets the hyperparameters found in `**params`.
        """
        for name, value in params.items():
            if name in self.hpnames:
                setattr(self, name, value)
            else:
                raise ValueError(f"{name} is not a known hyperparameter")
    
    @property
    def tokenizer(self) -> DistilBertTokenizerFast:
        # Lazy load the tokenizer
        if not hasattr(self, "_tokenizer"):
            self._tokenizer = self.get_tokenizer()
        return self._tokenizer

    def build_and_compile_model(self):
        embedder = self.get_embedder(trainable=self.fine_tune_embedder)

        in_id = Input(shape=(self.max_seq_len,), name='input_ids', dtype=tf.int32)
        in_mask = Input(shape=(self.max_seq_len,), name='input_mask', dtype=tf.int32)
        word_start_mask = Input(shape=(self.max_seq_len,), name='word_start_mask', dtype=tf.float32)
        embedder_inputs = [in_id, in_mask]
        all_inputs = [in_id, in_mask, word_start_mask]

        # The output of the pretrained base model.
        token_embeddings = embedder(embedder_inputs)[0]
        pooled_embedding = token_embeddings[:, 0]

        # A network for intent classification.
        
        intent_out = pooled_embedding
        for _ in range(self.n_hidden_layers):
            intent_out = Dropout(rate=self.dropout)(intent_out)
            intent_out = Dense(
                self.hidden_size,
                activation=None,
                kernel_regularizer=regularizers.l2(self.l2_regularization),
            )(intent_out)
            intent_out = BatchNormalization()(intent_out)
            intent_out = Activation(self.hidden_activation)(intent_out)

        intent_out = Dense(self.n_intents, activation='sigmoid', name='intent')(intent_out)

        # Another network for NER.

        tags_out = token_embeddings
        for _ in range(self.n_hidden_layers):
            tags_out = Dropout(rate=self.dropout)(tags_out)
            tags_out = TimeDistributed(Dense(
                self.hidden_size,
                activation=None,
                kernel_regularizer=regularizers.l2(self.l2_regularization),
            ))(tags_out)
            tags_out = BatchNormalization()(tags_out)
            tags_out = Activation(self.hidden_activation)(tags_out)

        tags_out = TimeDistributed(Dense(self.n_tags, activation='sigmoid'))(tags_out)
        tags_out = Lambda(lambda x: x, name='tags')(tags_out)
        # tags_out = Multiply(name='tagger')([tags_out, word_start_mask])

        self.model = Model(inputs=all_inputs, outputs=[intent_out, tags_out])
        self._compile_model()

    def _compile_model(self):
        optimizer = tf.keras.optimizers.Adam(self.learning_rate)
        losses = {
            'tags': 'binary_crossentropy',
            'intent': 'binary_crossentropy'
        }
        loss_weights = {'tags': 3.0, 'intent': 1.0}
        metrics = {'intent': 'acc', 'tags': 'acc'}
        self.model.compile(optimizer=optimizer, loss=losses, loss_weights=loss_weights, metrics=metrics)
        if self.verbose:
            self.model.summary()

    def get_tags_output_mask(self, word_start_mask):
        word_start_mask = np.expand_dims(word_start_mask, axis=2)  # n x seq_len x 1
        tags_output_mask = np.tile(word_start_mask, (1, 1, self.n_tags))  # n x seq_len x n_tags
        return tags_output_mask

    def train(self, batch_size: int = None, epochs: int = None, auto: bool = False):
        """
        Processes the agent data into training data, and trains the model.
        If `auto==True`, hyperparameters are determined automatically.
        """
        if not auto:
            if batch_size is not None:
                self.batch_size = batch_size
            if epochs is not None:
                self.epochs = epochs

        dataset = DataPreprocessor.preprocess(self.agent_data, self.tokenizer).to_dataset(self.max_seq_len)
        train_data, val_data, hparams, callbacks = AutoSetup.get_training_setup(auto, dataset, self.get_params())
        self.set_params(**hparams)

        self._fit(train_data, val_data, callbacks)
        
        if self.save_model_dir is not None:
            # Save the model's state, so it can be deployed and used.
            self.model.save(self.save_model_dir, save_format="tf")
    
    def _fit(
        self,
        train_data: tf.data.Dataset,
        val_data: tf.data.Dataset = None,
        callbacks: list = None,
        tensorboard: bool = True
    ) -> float:
        """
        Fits the model on `train_data`, using optional `val_data` for validation.
        `train_data` and `val_data` should be passed in unbatched.
        """
        if self.verbose:
            print("Fitting model using hyperparameters:")
            print(self.get_params())

        start = time()
        if callbacks is None:
            callbacks = []

        if val_data:
            val_data = val_data.batch(self.batch_size)

        if tensorboard:
            logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
            callbacks.append(tf.keras.callbacks.TensorBoard(log_dir=logdir))

        n_train = sum(1 for _ in train_data)

        self.model.fit(
            train_data.batch(self.batch_size),
            epochs=self.epochs,
            steps_per_epoch=AutoSetup.get_steps_per_epoch(n_train, self.batch_size),
            validation_data=val_data,
            use_multiprocessing=True,
            callbacks=callbacks
        )
        train_time = time() - start
        if self.verbose:
            print(f"Total train time: {train_time:.6f} seconds.")
        
        return train_time
    
    def evaluate(
        self,
        auto: bool = False,
        test_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0
    ) -> tuple:
        """
        Performs cross validation to evaluate the model's training set performance
        and generalizable performance on its agent's data.
        
        Parameters
        ----------
        auto : bool
            Whether to automatically determine the hyperparameter setup.
        test_ratio : float
            If provided, a basic stratified train/test split will be used.
        nfolds : int
            If provided, stratified k-fold cross validation will be conducted with `k==nfolds`.
        repeat : int
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.

        Returns
        -------
        training_performance : dict
            The metrics from evaluating the fitted model on the training set.
        test_performance : dict
            The metrics from evaluating the fitted model on the test set.
        """
        if test_ratio is not None and nfolds is not None:
            raise ValueError("please supply either test_ratio or nfolds, but not both")

        if test_ratio is not None:
            eval_fn = lambda: self._evaluate_train_test(auto, test_ratio)
        elif nfolds is not None:
            eval_fn = lambda: self._evaluate_kfold_cv(auto, nfolds)
        else:
            raise ValueError("please supply either test_ratio or nfolds")
        
        if repeat > 0:
            results = [eval_fn() for _ in range(repeat)]
            return tuple(aggregate_dicts(dicts, "mean") for dicts in zip(*results))
        else:
            return eval_fn()
    
    def _evaluate_train_test(self, auto: bool, test_ratio: float) -> tuple:
        # Evaluate the model on a basic train/test split.
        dataset, test_data = DataPreprocessor.preprocess(self.agent_data, self.tokenizer).to_dataset_split(self.max_seq_len, test_ratio)
        return self._evaluate(dataset, test_data, auto)
    
    def _evaluate_kfold_cv(self, auto: bool, nfolds: int) -> tuple:
        # Evaluate the model using k-fold cross validation.
        folds = DataPreprocessor.preprocess(self.agent_data, self.tokenizer).to_dataset_folds(self.max_seq_len, nfolds)
        results = []
        for test_fold, train_folds in leave_one_out(folds):
            train_data = reduce(lambda a, b: a.concatenate(b), train_folds)
            results.append(self._evaluate(train_data, test_fold, auto))
        
        # Now average the k performance results.
        return tuple(aggregate_dicts(dicts, "mean") for dicts in zip(*results))

    def _evaluate(self, train_data: tf.data.Dataset, test_data: tf.data.Dataset, auto: bool) -> tuple:
        self.build_and_compile_model()
        train_data, val_data, hparams, callbacks = AutoSetup.get_training_setup(auto, train_data, self.get_params())
        self.set_params(**hparams)

        train_time = self._fit(train_data, val_data, callbacks, False)

        train_performance = self.model.evaluate(train_data.batch(self.batch_size_predict), return_dict=True)
        train_performance["train_time"] = train_time

        test_performance = self.model.evaluate(test_data.batch(self.batch_size_predict), return_dict=True)

        # Get ECE
        ece_quantiles = self.bayesian_ece_for_obj(
            test_data,
            "intent",
            quantiles=[10, 50, 90],
            is_sparse=False
        )
        for quantile, value in ece_quantiles.items():
            test_performance[f"intent_test_ece_q{quantile}"] = value

        return train_performance, test_performance

    def predict(self, text: str, tokenizer: DistilBertTokenizerFast):
        text = text.lower()
        raw_input = PredictionInput(text=text, max_seq_len=self.max_seq_len, tokenizer=tokenizer)
        x = raw_input.to_model_input()
        prediction = self.model.predict(x=x)
        return prediction

    def decode_intent(self, raw_intent_prediction: np.ndarray) -> dict:
        intent_max = np.argmax(raw_intent_prediction)
        confidence = np.max(raw_intent_prediction)
        decoded_intent = self.intents_encoder.inverse_transform([intent_max])[0]
        return {"value": decoded_intent, "confidence": confidence}

    def decode_tags(self, raw_tag_predictions: np.ndarray, text: str, word_start_mask: List[int]):
        raw_tag_predictions = np.squeeze(raw_tag_predictions)
        assert raw_tag_predictions.shape[0] == len(word_start_mask)
        decoded_tags = []
        for i, e in enumerate(word_start_mask):
            if e == 1:
                predicted_tag_idx = np.argmax(raw_tag_predictions[i])
                predicted_tag = self.tag_encoder.inverse_transform([predicted_tag_idx])[0]
                decoded_tags.append(predicted_tag)

        words = text.split()

        result = []
        current_tag_words = []
        current_tag_type = None
        for i, tag in enumerate(decoded_tags):
            if tag == 'O':
                if current_tag_words and current_tag_type:
                    result.append({
                        'tag_type': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_type = None
                current_tag_words = []
                continue

            if tag.startswith('B-'):
                if current_tag_words and current_tag_type:
                    result.append({
                        'tag_type': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_words = [words[i]]
                current_tag_type = tag[2:]
            elif tag.startswith('I-'):
                current_tag_words.append(words[i])

        if current_tag_words and current_tag_type:
            result.append({
                'tag_type': current_tag_type,
                'value': ' '.join(current_tag_words),
            })

        return result

    def bayesian_ece_for_obj(
        self,
        data: tf.data.Dataset,
        obj: str,
        *,
        quantiles: Sequence = [10, 50, 90],
        bins: int = 15,
        is_sparse: bool = True
    ) -> Dict[int, float]:
        """
        Computes the Bayesian Expected Calibration Error (ECE) for `data` (ubatched)
        with respect to a single objective of the model (denoted by `obj`). Returns
        the quantiles denoted by `quantiles` of the approximated posterier bayesian
        distribution over ECE. If the labels in `data` are sparse, `is_sparse` should be
        `True`.
        """
        y_pred = self.model.predict(data.batch(self.batch_size_predict), verbose=1)

        # Isolate the labels and predictions for the objective in question.
        y_obj = tf.stack([y[obj] for _, y in data])
        if not is_sparse:
            # The ECE equation expects sparse labels.
            y_obj = tf.argmax(y_obj, axis=-1)

        obj_i = self.model.output_names.index(obj)
        y_pred_obj = tf.convert_to_tensor(y_pred[obj_i], tf.float32)

        ece_samples = um.bayesian_expected_calibration_error(
            bins,
            probabilities=y_pred_obj,
            labels_true=tf.cast(y_obj, tf.int32)
        )
        ece_quantiles = tfp.stats.percentile(ece_samples, quantiles)
        return {quantile: float(value) for quantile, value in zip(quantiles, ece_quantiles)}
