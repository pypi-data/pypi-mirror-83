
from os.path import expanduser
from itertools import islice as head

from tqdm.notebook import tqdm as log_progress

from corus import load_lenta
from navec import Navec

from slovnet.const import PAD, PER, LOC, ORG
from slovnet.io import (
    load_lines,
    dump_lines
)
from slovnet.sent import sentenize
from slovnet.token import tokenize
from slovnet.shape import SHAPES
from slovnet.vocab import Vocab, BIOTagsVocab

from slovnet.model.emb import (
    Embedding,
    NavecEmbedding
)
from slovnet.model.tag import (
    TagEmbedding,
    TagEncoder,
    NERHead,
    NER,
    MorphHead,
    Morph
)

# from slovnet.exec.encoders import TagEncoder


NAVEC = expanduser('~/proj/navec/data/navec_news_v1_1B_250K_300d_100q.tar')
LENTA = expanduser('~/proj/corus-data/lenta-ru-news.csv.gz')

TAGS_VOCAB = 'data/tags_vocab.txt'
ENCODER = 'data/encoder.pt'
MORPH = 'data/morph.pt'
NER_ = 'data/ner.pt'
SHAPE = 'data/shape.pt'

SHAPE_DIM = 30
LAYER_DIMS = [256, 128, 64]
KERNEL_SIZE = 3

ONNX = 'data/model.onnx'
PACK = 'data/slovnet_ner_news_v1.tar'


def sentok(texts):
    for text in texts:
        for sent in sentenize(text):
            yield [_.text for _ in tokenize(sent.text)]
