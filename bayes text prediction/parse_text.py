import tomli_w
from tqdm import tqdm
import pickle


def main() -> None:
    with open("coca-text.txt") as f:
        lines = f.readlines()

    lines = [' '.join(line.strip() for line in lines)]
    k = 10

    before_encodings = {}
    after_encodings = {}
    distribution = {}

    total = 0

    replacements = {
        "gon na": "gonna",
        "do nt": "dont",
        "did nt": "didnt",
        "wan na": "wanna",
        "i ve": "ive",
        "is nt": "isnt",
        "got ta": "gotta",
        "wo nt": "wont",
        "ca nt": "cant"
    }

    for line in lines:
        line = line.strip()

        for replacement in replacements:
            line = line.replace(replacement, replacements[replacement])

        line = line.split(" ")

        for i in tqdm(range(len(line))):
            word = line[i]
            total += 1

            if word not in after_encodings:
                after_encodings[word] = [{} for _ in range(k)]

            if word not in before_encodings:
                before_encodings[word] = [{} for _ in range(k)]

            if word not in distribution:
                distribution[word] = 1
            else:
                distribution[word] += 1

            for j in range(0, k):
                if i + j + 1 >= len(line): break
                bin = after_encodings[word][j]
                kth_word = line[i + j + 1]

                if kth_word == word:
                    continue

                if kth_word in bin:
                    bin[kth_word] += 1
                else:
                    bin[kth_word] = 1

            for j in range(0, k):
                if i - (j + 1) < 0: break
                bin = before_encodings[word][j]
                kth_word = line[i - (j + 1)]

                if kth_word == word:
                    continue

                if kth_word in bin:
                    bin[kth_word] += 1
                else:
                    bin[kth_word] = 1

    for word_encoding in after_encodings:
        for bin in after_encodings[word_encoding]:
            occurences = sum(bin.values())
            for word in bin:
                bin[word] /= occurences

    for word_encoding in before_encodings:
        for bin in before_encodings[word_encoding]:
            occurences = sum(bin.values())
            for word in bin:
                bin[word] /= occurences

    for word in distribution:
        distribution[word] /= total

    output = {
                "after_encodings": after_encodings,
                "before_encodings": before_encodings,
                "num_words": total,
                "distribution": distribution
            }

    print("Writing encodings to file...")
    with open("encodings", 'wb') as f:
        pickle.dump(output, f, pickle.HIGHEST_PROTOCOL)

    # with open('encodings.toml', 'wb') as f:
    #     tomli_w.dump(output, f)


if __name__ == "__main__":
    main()
