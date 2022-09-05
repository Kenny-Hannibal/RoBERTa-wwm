from segment.model.crf.crfpp_predictor import CRFPPPredictor
from segment.sequence_tokenizer.sequence_pos_tokenizer import SequencePosTokenizer


class PosOnlyTokenizer(SequencePosTokenizer):

    def __init__(self, model_path):
        super(PosOnlyTokenizer, self).__init__()
        self._tagger = CRFPPPredictor(model_path, prev_tags=None, end_tags=None)

    def _tag(self, words):
        pairs = [(word,) for word in words]
        for idx, tag in enumerate(self._tagger.predict([pairs])[0]):
            yield pairs[idx][0], tag
