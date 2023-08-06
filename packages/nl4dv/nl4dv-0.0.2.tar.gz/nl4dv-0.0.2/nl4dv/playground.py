from datetime import datetime
from itertools import product
import dateparser
from dateutil.parser import parse
from gensim.models import Word2Vec, KeyedVectors
from nltk.corpus import wordnet as wn

def synonymity_score(word_x, word_y):
    # type: (str, str) -> int
    """
    Helper method to find similarity between two words

    """
    sem_1 = wn.synsets(word_x)
    sem_2 = wn.synsets(word_y)
    max_score = 0
    for i, j in list(product(*[sem_1, sem_2])):
        score = i.wup_similarity(j)
        max_score = score if (score is not None and max_score < score) else max_score

    return max_score * 100

def word2vec_stuff():
    # Use the BROWN corpus from NLTK
    # model = Word2Vec(brown.sents())
    # model.save('examples/assets/jars/brown.embedding')
    model = Word2Vec.load('examples/assets/jars/brown.embedding')
    # vocabulary = model.wv.vocab
    print(model.similarity('king', 'queen'))
    # print(model.similarity('price', 'cost'))
    # print(model.most_similar(positive=['price'], topn = 3))

    # Use Google News corpus: https://code.google.com/archive/p/word2vec/
    # model = KeyedVectors.load_word2vec_format('examples/assets/jars/GoogleNews-vectors-negative300.bin.gz', binary=True)
    # model.save('examples/assets/jars/googlenews.embedding')
    model = KeyedVectors.load('examples/assets/jars/googlenews.embedding')
    print(model.similarity('king', 'queen'))

def isdateParser(datum):
    settings = dict()
    settings['PREFER_DAY_OF_MONTH'] = 'first'
    settings['RELATIVE_BASE'] = datetime(2020, 1, 1)
    try:
        if datum == '' or str(datum).isspace():
            return False
        print('dateparser: ', dateparser.parse(datum, settings=settings), '  dateutil.parser: ', parse(datum, fuzzy=False))
    except AttributeError:
        return False
    except ValueError:
        return False
    except OverflowError:
        return False
    return True


def dateparsing():
    isdateParser("12/05/18")
    isdateParser("12-05-18")
    isdateParser("December 2018")
    isdateParser("Dec 2018")
    isdateParser("Dec 5 2018")
    isdateParser("December 5 2018")
    isdateParser("2018")
    isdateParser("5 Dec 2018")
    isdateParser("8 June")
    isdateParser("June 8")

word2vec_stuff()
# dateparsing()
# print (synonymity_score("date","year"))
