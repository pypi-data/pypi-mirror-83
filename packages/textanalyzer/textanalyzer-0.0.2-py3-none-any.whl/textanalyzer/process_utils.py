# MIT License

# Copyright (c) 2020 Kim DongWook

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import unicodedata
from typing import List, Union, Tuple, Dict

from .data_utils import Doc, Token


class Tokenization:
    """Base Class for Tokenization. This can be applied line by line."""
    def __call__(self, doc: Dict) -> Doc:
        """Tokenize the data with callable format."""        
        if type(doc) == dict:
            Id, text = list(doc.items())[0]
        else:
            raise TypeError(f'The type of doc should be {dict} rather than {type(doc)}.')
        
        # if text is not None
        if text:
            tokens, pos = self.tokenize(text)
            tokens = [Token(DocId=Id, offset=i, text=tok, pos=p) 
                      for i, (tok, p) in enumerate(zip(tokens, pos))]
        
        # Return Doc
        return Doc(
            Id = Id,
            text = text,
            tokens = tokens
        )
    
    def _normalize(self, text: str) -> str:
        """[Overwrite] Normalize string of input data.(Default: NFKC)"""
        return unicodedata.normalize('NFKC', text)    
        
    def _preprocess(self, text: str) -> str:
        """[OverWrite] Preprocessing stinrgs of input text data."""
        raise NotImplementedError()
    
    def _tokenize(self, text: str) -> Tuple[List[str]]:
        """[OverWrite] Tokenize the String to List of String.
        * input : string
        * return : first list is token list and second list is pos list. 
            e.g.) (['쿠팡', '에서', '후기', '가', '좋길래', '닦토용', '으로', '샀는데', '별로에요', '....'],  ['L', 'R', 'L', 'R', 'L', 'L', 'R', 'L', 'L', 'R'])
            return token, pos
        """
        raise NotImplementedError()
    
    def _postprocess(self, doc: Tuple[List[str]]) -> Tuple[List[str]]:
        """[OverWrite] Postprocessing for tokenized data."""
        raise NotImplementedError()
        
    def tokenize(self, text: str) -> Tuple[List[str]]:
        """Tokenize the single string with pre, post processing."""
        return self._postprocess(self._tokenize(self._preprocess(self._normalize(text))))
    

        
class TokenCandidateGeneration:
    """From tokenized token candidates, filter the candidates for keyphrase extraction"""
    def __call__(self, doc: Doc) -> Doc:
        return self.get_candidate(doc)
    
    def get_candidate(self, doc: Doc) -> Doc:
        """[OverWrite] Candidates extraction from token list"""
        raise NotImplementedError()
                