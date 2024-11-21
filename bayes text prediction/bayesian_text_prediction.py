# m =
# P(word_1, word_2, ..., word_n given word) = P(word_1 given word) * P(word_2 given word) * ... * P(word_n given word)
# P(word given word_1, word_2, ... , word_n) =
# m * P(word) / (m * P(word) + n * (1 - P(word))
# n =
# P(word_1, word_2, ..., word_n given not word) = P(word_1 given not word) * P(word_2 given not word) * ... * P(word_n given not word)

# how to find m?
# look through our dictionary and find each word. for the last word, find the occurrences that our given word appears directly after. for the second to last, find the occurrences that it appears 2 places after, and so on
# do this for a sliding window of k words
# data structure? parse the text and store 10 lists per word of all the words that show up 1 <= k <= 10 words after our word, along with the percent that the word showed up
# for n, just do the same thing but for the all words that arent our word
# lets say our word doesn't have a kth next word? give it a default probability 1 / ((10 - k) * all_words)
# lets say or word isn't in the kth next word container? give it a default probability 1 / all_words


# this might have the problem where its actually just repeating the same lines as the source... maybe it will be better with more text

import tomli
import re
import random
from tqdm import tqdm

import math
import statistics
import pickle


def filter_text(text: str) -> list[str]:
    """
    :param text: text to be filtered
    :return: lowercase list of alphabetic words
    """
    text = text.lower().strip()
    text = re.sub(r'[^a-z]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split(" ")


def get_next_word(message, k, after_encodings, distribution, num_words, before_encodings):
    default_word_probability = 1 / num_words
    word_probs = {}

    # find probability of every word coming after this message
    for word in distribution:
        P_word = distribution[word]

        N = P_word
        M = (1 - P_word)

        for i in range(1, min(len(message), k) + 1):
            kth_word = message[-i]

            before_words = before_encodings[word][i - 1]

            if len(before_words) == 0:
                # N *= 1 / num_words
                # continue
                break

            N *= before_words.get(kth_word, default_word_probability)

        for i in range(1, min(len(message), k) + 1):
            kth_word = message[-i]

            if kth_word not in after_encodings:
                # M *= 1 / ((k + 1 - i) * num_words)
                # M *= 1 - 1 / num_words
                # continue
                break

            after_words = after_encodings[kth_word][i - 1]

            if len(after_words) == 0:
                # M *= 1 - 1 / num_words
                # continue
                break

            M *= (1 - after_words.get(word, default_word_probability))

        word_probs[word] = N / (N + M)

    # normalize data
    s = sum(word for word in word_probs.values())
    word_probs = {word: word_probs[word] / s for word in word_probs}
    next_word = random.choices(list(word_probs.keys()), weights=list(word_probs.values()))[0]
    return next_word


def main() -> None:
    print("Loading encodings into memory...")
    # with open("encodings.toml", 'rb') as f:
    #     data = tomli.load(f)

    with open("encodings", 'rb') as f:
        data = pickle.load(f)

    num_words = data["num_words"]
    after_encodings = data["after_encodings"]
    before_encodings = data["before_encodings"]
    distribution = data["distribution"]

    while True:
        message = filter_text(input("Give a message: "))

        k = 10

        for _ in tqdm(range(20), desc="Generating sentence"):
            next_word = get_next_word(message, k, after_encodings, distribution, num_words, before_encodings)
            message.append(next_word)

        print(' '.join(message))


if __name__ == '__main__':
    main()
