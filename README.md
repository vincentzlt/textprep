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
