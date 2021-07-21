from textblob import TextBlob


def anlaysis(text):
    total = 0
    blob = TextBlob(text)
    blob.tags  # [('The', 'DT'), ('titular', 'JJ'),
    #  ('threat', 'NN'), ('of', 'IN'), ...]
    # print('@', blob.tags)
    blob.noun_phrases  # WordList(['titular threat', 'blob',
    #            'ultimate movie monster',
    #            'amoeba-like mass', ...])
    # print('#', blob.noun_phrases)
    for sentence in blob.sentences:
        # print(sentence.sentiment.polarity)
        total += sentence.sentiment.polarity
    return blob.noun_phrases, total


# if __name__ == "__main__":
#     anlaysis('The fox and the wolf give you New Year greetings, so terrible')
