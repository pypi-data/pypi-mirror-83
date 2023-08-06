
from tqdm.notebook import tqdm as log_progress

from collections import defaultdict, Counter

from natasha import (
    PER,

    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    NamesExtractor,

    Doc
)

from natasha.morph.lemma import normal_word


def adapt_spans(doc, spans):
    from natasha.doc import DocSpan

    for start, stop, type, normal in spans:
        text = doc.text[start:stop]
        yield DocSpan(start, stop, type, text)


def add_spans(doc, spans):
    from natasha.span import index_spans, query_spans_index

    doc.spans = list(adapt_spans(doc, spans))

    # envelope tokens < spans < sents
    index = index_spans(doc.tokens)
    for span in doc.spans:
        span.tokens = query_spans_index(index, span)

    index = index_spans(doc.spans)
    for sent in doc.sents:
        sent.spans = query_spans_index(index, sent)
