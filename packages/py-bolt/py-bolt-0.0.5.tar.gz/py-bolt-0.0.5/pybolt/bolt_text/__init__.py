from pybolt.bolt_text.bolt_text import BoltText
from pybolt.bolt_text.char_clean import CharClean

bolt_text = BoltText()
char_clean = CharClean()

bolt_text.normalize = char_clean.normalize
bolt_text.clean = char_clean.clean

__all__ = ["bolt_text"]
