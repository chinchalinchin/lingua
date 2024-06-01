class Word:

    def __init__(self, content):
        self.content = content
        self.contexts = []
        return
    
    def __str__(self):
        return self.content
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __lt__(self, other):
        return self.frequency() < other.frequency()
    
    def __iter__(self):
        for k, v in self.as_dict().items():
            yield (k, v)

    def as_dict(self):
        return {
            'frequency': self.frequency(),
            'contexts': [
                (
                    str(context[0]), 
                    str(context[1]))
                for context in self.contexts
            ]
        }
    
    def add_context(self, start, end):
        return self.contexts.append(  
            (start, end)
        )
    
    def frequency(self):
        return len(self.contexts)
        
class Sentence:

    def __init__(self, words):
        self.words = words
        return
    
    def __iter__(self):
        for w in self.words:
            yield str(w)
    
    def __str__(self):
        stringified = ''

        for w in self.words:
            stringified += str(w) + " "
        
        return stringified[0:-1]
    
    def __contains__(self, item):
        return item in self.words