# import language_models
from szyfrow.support.utilities import sanitise

american = set(open('/usr/share/dict/american-english', 'r').readlines())
british = set(open('/usr/share/dict/british-english', 'r').readlines())
cracklib = set(open('/usr/share/dict/cracklib-small', 'r').readlines())

words = american | british | cracklib

# sanitised_words = set()

# for w in words:
    # sanitised_words.add(language_models.sanitise(w))
    
sanitised_words = set(sanitise(w) for w in words)

sanitised_words.discard('')

with open('words.txt', 'w') as f:
    f.write('\n'.join(sorted(sanitised_words, key=lambda w: (len(w), w))))
