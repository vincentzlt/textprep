# textprep
text pre-processing toolkit for character-based languages: dict-based
tokenization (Jieba, Mecab, Kytea), subword tokenization (Sentencepiece
unigram/bpe), vocab generalization, text normalization, reverse tokenization,
character decomposition (based on cjkvi-ids project and manual data), etc.

## required softwares
- [Jieba](https://github.com/fxsjy/jieba)
<br/>
“结巴”中文分词：做最好的 Python 中文分词组件
<br/>
"Jieba" (Chinese for "to stutter") Chinese text segmentation: built to be the best Python Chinese word segmentation module.
- [Mecab](http://taku910.github.io/mecab/)
<br/>
Yet Another Part-of-Speech and Morphological Analyzer (doc in Japanese)
- [Kytea](http://www.phontron.com/kytea/) ([japanese](http://www.phontron.com/kytea/index-ja.html))
<br/>
A general toolkit developed for analyzing text, with a focus on Japanese, Chinese and other languages requiring word or morpheme segmentation.
<br/>
Extra models for specific languages can be found at [here](http://www.phontron.com/kytea/model.html#japanese). 
- [Moses](https://github.com/moses-smt/mosesdecoder)
<br/>
Moses, the machine translation system. Mainly the preprocessing script is used. (should pay attention to script path when use it)
- [SentencePiece](https://github.com/google/sentencepiece)<br/>
Unsupervised text tokenizer for Neural Network-based text generation.
- [tqdm](https://github.com/tqdm/tqdm)<br/>
  handle progress bars

## usage

There are four sub-commands: tok, vocab, decomp, reverse. Use

    python3 textprep.py -h

to get detailed usage information for each sub-commands.

### examples
- use 'jieba' to tokenize chinese text. if you choose spm/bpe, relevant subword models will be trained by `Sentencepiece` first.
  
      python3 textprep.py tok -m jieba -i input.cn -o output.cn

- generate vocab of a maximum vocab size

      python3 textprep.py vocab -m mecab -i input.jp -m 30000

- decomposition chinese text into ideograph sequences. the ids file `ids.txt` can be found in `cjkvi-ids` sub-module. the circle/single char files can be found in `data` folder.

      python3 textprep.py decomp -d ./cjkvi-ids/ids.txt -c ./data/circle_char.txt -s ./data/single_char.txt -i tok/input.cn

- reverse transform decomposed/tokenized files back to original text. if reverse transform decomposed data, the decomp file (decomp dict) should be specified

      python3 textprep.py reverse -i ./tok/input.cn -m bpe


## plan

- pipeline the sub-commands
