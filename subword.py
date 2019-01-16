import collections
import itertools
import sys


def subword(args):
    if args.method in ['bpe', 'unigram']:
        assert args.vocab_size


def sents2uni(sents, split=False):
    if split:
        for word in itertools.chain.from_iterable(sents):
            yield '<w>'
            for uni in word:
                yield uni
            yield '</w>'
    else:
        for sent in sents:
            yield '<s>'
            for uni in '▁'.join(sent):
                yield uni
            yield '</s>'


def bi_count(uni_list):
    a, b = itertools.tee(uni_list)
    next(b, None)
    return collections.Counter(zip(a, b))


def merge(uni_list, vocab, bi_counter, num_ops=1):
    # import pdb
    # pdb.set_trace()
    bi_grams = set(k for k, v in bi_counter.most_common(num_ops))
    for idx in range(len(uni_list) - 1):
        t = (uni_list[idx], uni_list[idx + 1])
        t_vocab = ''.join(t)
        if t in bi_grams:

            uni_list[idx + 1] = t_vocab
            uni_list[idx] = None

            vocab.update([t_vocab])
            vocab.subtract(t)

    return [u for u in uni_list if u is not None], +vocab


def train_bpe(fname, vocab_size, split=False):
    sents = ([w for w in l.strip().split()]
             for l in open(fname, encoding='utf8'))
    uni_list = list(sents2uni(sents, split=split))
    vocab = collections.Counter(uni_list)

    keep_training = Keep_training()
    while keep_training(vocab, vocab_size):
        bi_counter = bi_count(uni_list)
        sys.stdout.write('\r' + 'num vocab: {} num bi_vocab: {} '.format(
            len(vocab), len(bi_counter)))
        uni_list, vocab = merge(uni_list, vocab, bi_counter)

    return uni_list, vocab


class Keep_training():
    def __init__(self):
        self.max_vocab = 0

    def __call__(self, vocab, vocab_size):
        if len(vocab) >= self.max_vocab:
            self.max_vocab = len(vocab)

        if self.max_vocab >= vocab_size:
            print('max vocab size {} reached.'.format(len(vocab)))
            return False
        if self.max_vocab >= len(vocab) * 1.1:
            print('vocab size retreat too many {} -> {}'.format(
                self.max_vocab, len(vocab)))
            return False
        if any(
                len(v.replace('<', '').replace('>', '').replace('/', '')) > 10
                for v in vocab):
            print('too many merges on same vocab. stop')
            return False

        return True