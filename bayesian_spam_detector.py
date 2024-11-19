import re
from typing import Iterable


def filter_text(text: str) -> set[str]:
    """
    :param text: text to be filtered
    :return: lowercase list of alphabetic words
    """
    text = text.lower().strip()
    text = re.sub(r'[^a-z]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return set(text.split(" "))


def read_file() -> tuple[list[set[str]], list[set[str]]]:
    """
    Reads dataset and returns the filtered and labeled spam & ham (real) messages
    :return: spam_messages, ham_messages
    """
    spam_messages = []
    ham_messages = []

    with open('spam_dataset', 'r') as f:
        lines = f.readlines()
        for line in lines:
            label, text = line.split("\t", maxsplit=1)
            if label.strip() == "spam":
                spam_messages.append(filter_text(text))
            else:
                ham_messages.append(filter_text(text))

    return spam_messages, ham_messages


def populate_distributions(spam_messages: list[set[str]], ham_messages: list[set[str]]):
    """
    Populates distributions of ham and spam messages
    :param spam_messages: list of all spam messages in dataset
    :param ham_messages: list of all ham messages in dataset
    :return: distribution of spam words, distribution of ham words, default spam distribution, default ham distribution
    """

    # set up distribution of spam & ham messages
    spam_words_distributions = {}
    ham_words_distributions = {}

    # count occurrences of each word per message
    spam_words = 0
    for message in spam_messages:
        spam_words += len(message)
        for word in message:
            if word in spam_words_distributions:
                spam_words_distributions[word] += 1
            else:
                spam_words_distributions[word] = 1

    ham_words = 0
    for message in ham_messages:
        ham_words += len(message)
        for word in message:
            if word in ham_words_distributions:
                ham_words_distributions[word] += 1
            else:
                ham_words_distributions[word] = 1

    # divide occurences by total number of messages for probability
    spam_words_distributions = {word: spam_words_distributions[word] / len(spam_messages)
                                for word in spam_words_distributions}
    ham_words_distributions = {word: ham_words_distributions[word] / len(ham_messages)
                               for word in ham_words_distributions}

    # default probabilities are just the chance of choosing a word at random from each
    # default probabilities are used when the user inputs a word that wasn't in the dataset
    return spam_words_distributions, ham_words_distributions, 1 / spam_words, 1 / ham_words


def determine_best_cutoff(spam_messages, ham_messages, spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability):
    """
    Iteratively determines the best cutoff for ham and spam messages
    Maximizes the sum of the correct identification of ham and spam messages

    :param spam_messages: list of all spam messages in dataset
    :param ham_messages: list of all ham messages in dataset
    :param spam_words_distributions: distribution of spam words
    :param ham_words_distributions: distribution of ham words
    :param default_spam_probability: probability of spam word if it doesn't appear in dataset
    :param default_ham_probability: probability of ham word if it doesn't appear in dataset
    :return: cutoff
    """

    def spam_score(spam_probs, cutoff):
        return sum(prob >= cutoff for prob in spam_probs) / len(spam_probs)

    def ham_score(ham_probs, cutoff):
        return sum(prob < cutoff for prob in ham_probs) / len(ham_probs)

    # calculate probabilities of each message being spam
    spam_probs = [determine_spam_prob(message, spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability)
                  for message in spam_messages]
    ham_probs = [determine_spam_prob(message, spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability)
                 for message in ham_messages]

    highest_cutoff = 0.5
    highest_score = spam_score(spam_probs, highest_cutoff) + ham_score(ham_probs, highest_cutoff)

    # iterate through and find cutoff that maximizes spam_score + ham_score
    precision = 100_000
    for i in range(0, precision+1):
        cutoff = i / precision
        score = spam_score(spam_probs, cutoff) + ham_score(ham_probs, cutoff)
        if score > highest_score:
            highest_score = score
            highest_cutoff = cutoff

    print(f"Spam Score: {spam_score(spam_probs, highest_cutoff)}\nHam Score: {ham_score(ham_probs, highest_cutoff)}\nCutoff: {highest_cutoff}")
    return highest_cutoff


def determine_spam_prob(message, spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability):
    """
    Determine the probability of a message being spam or not

    :param message: filtered message
    :param spam_words_distributions: distribution of spam words
    :param ham_words_distributions: distribution of ham words
    :param default_spam_probability: probability of spam word if it doesn't appear in dataset
    :param default_ham_probability: probability of ham word if it doesn't appear in dataset
    :return:
    """
    def product(__iterable: Iterable[float]) -> float:
        prod: float = 1
        for item in __iterable:
            prod *= item
        return prod

    # p(w_1) * p(w_2) * ... * p(w_n)
    spam_probs = product(spam_words_distributions[word]
                         if word in spam_words_distributions
                         else default_spam_probability
                         for word in message)

    # q(w_1) * q(w_2) * ... * q(w_n)
    ham_probs = product(ham_words_distributions[word]
                        if word in ham_words_distributions
                        else default_ham_probability
                        for word in message)

    # avoid division by 0
    if spam_probs == 0: return 0

    # Use bayes' theorem
    # assuming probabilities of words appearing in a message are independent (mutually exclusive events)
    spam_probability = spam_probs / (spam_probs + ham_probs)
    return spam_probability


def main() -> None:
    spam_messages, ham_messages = read_file()
    spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability = (
        populate_distributions(spam_messages, ham_messages))

    # cutoff = determine_best_cutoff(spam_messages, ham_messages, spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability)
    # print(cutoff)
    cutoff = 0.98688

    message = filter_text(input("Type a message: "))

    spam_probability = (
        determine_spam_prob(message, spam_words_distributions, ham_words_distributions, default_spam_probability, default_ham_probability))

    print(f"Probability of your message being spam: {100*spam_probability:.3f}%")
    print(f"Your message is {['HAM', 'SPAM'][spam_probability >= cutoff]}")


if __name__ == "__main__":
    main()
