class Word:

    def __init__(self, content):
        self.content = content
        self.contexts = []
        self.distances = {}
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
            'distances': self.distances,
            'contexts': self.unique_contexts(),
        }
    
    def set_distance(self, word, dist):
        self.distances[str(word)] = dist

    def sort_distances(self):
        s_dist = sorted(
            self.distances.items(), 
            key=lambda x: x[1],
            reverse = True
        )
        self.distances = {
            pair[0]: pair[1]
            for pair in s_dist
        }

    def add_context(self, start, end):
        return self.contexts.append(  
            (start, end)
        )
    
    def frequency(self):
        return len(self.contexts)
    
    def prior_contexts(self):
        return [
            str(context[0])
            for context in self.contexts
        ]

    def post_contexts(self):
        return [
            str(context[1])
            for context in self.contexts
        ]
        
    def unique_contexts(self):
        return list(
            set([
                (
                    str(context[0]), 
                    str(context[1]))
                for context in self.contexts
            ])
        )
    
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