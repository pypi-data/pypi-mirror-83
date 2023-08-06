"""
A package to run any machine learning model in production
"""

# flake8: noqa

from .model_template import ModelTemplate
from .model_template import ModelPieces
from .model_template import ModelThemes
from .pieces_utils.tfidf_vectorizer import (TfidfTransformer2,
                                            TfidfVectorizer_Gpam)

__version__ = "0.0.13"
