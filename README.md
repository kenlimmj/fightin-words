<!--
@Author: Lim Mingjie, Kenneth <Astrianna>
@Date:   2016-05-22T20:53:55-04:00
@Email:  me@kenlimmj.com
@Last modified time: 2016-05-30T17:38:26-04:00
@License: MIT
-->

A scikit-learn compliant implementation of Monroe et al.'s Fightin' Words analysis method.

Features
========

- Computes a `(word, z-score)` result for a pair of text corpora.
- Works with scikit-learn estimators and pipelines.

Installation
============

Distributed via PyPI:
```shell
pip install fightin-words
```

Usage
=====

`fightin-words` implements `FWExtractor`, which inherits from the scikit-learn `BaseEstimator` and `TransformerMixin`.

Example:
```python
import fightin-words as fw
import sklearn.feature_extraction.text as sk_text

# Strings/text corpora to be compared
l1 = 'The quick brown fox jumps over the lazy pig'
l2 = 'The lazy purple pig jumps over the lazier donkey'

# Extractor configuration parameters
prior = 0.05
cv = sk_text.CountVectorizer(max_features=15000)

fw.FWExtractor(prior, cv).fit_transform([l1, l2])
```

Note that to maintain parity with scikit-learn conventions, `fit_transform` takes in _one_ variable (the canonical `X` for samples/features). Therefore the two strings to be compared should be marshaled into a single sequence-type (list or tuple) variable.

`prior` and `cv` do not need to be specified. `prior` defaults to 0.01, and `cv` defaults to a naively initialized scikit-learn `CountVectorizer`. If a list of precomputed priors is specified, it is expected that the user also passes in a vectorizer that is responsible for producing a vocabulary whose dimensionality matches the precomputed priors---we do not check for that.

Credits
=======

The [original implementation](https://github.com/jmhessel/FightingWords) by Jack Hessel at the Department of Computer Science, Cornell University. This version heavily borrows from it for the core computation. A more eloquent description of the algorithm is available there as well.

Monroe, B. L., Colaresi, M. P., & Quinn, K. M. (2008). Fightin'words: Lexical feature selection and evaluation for identifying the content of political conflict. _Political Analysis_, 16(4), 372--403.

```tex
@article{monroe2008fightin,
  title={Fightin' words: Lexical feature selection and evaluation for identifying the content of political conflict},
  author={Monroe, Burt L and Colaresi, Michael P and Quinn, Kevin M},
  journal={Political Analysis},
  volume={16},
  number={4},
  pages={372--403},
  year={2008},
  publisher={SPM-PMSAPSA}
}
```

LICENSE
=======

The MIT License (MIT)
Copyright (c) 2016 Kenneth Lim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
