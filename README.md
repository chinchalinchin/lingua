Notes
#####

- # observation: the cardinality of sentences must be greater than the cardinality of words
    #      reason: Every word is the answer to the question "Which word is next?".
    #     counter: The question "Which word is next?" is a meta-question.
    # observation: However, an observed vocab will always (with prob approx 1) exceed the 
    #               the cardinality of the corpus. I think. We shall see.