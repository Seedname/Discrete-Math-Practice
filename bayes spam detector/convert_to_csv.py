
import re
def filter_text(text: str) -> str:
    """
    :param text: text to be filtered
    :return: lowercase list of alphabetic words
    """
    text = text.lower().strip()
    text = re.sub(r'[^a-z]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


with open('spam_dataset', 'r') as f:
    lines = f.readlines()
    with open('spam_dataset.csv', 'w') as g:
        g.write("label,text\n")
        for line in lines:
            label, text = line.split("\t", maxsplit=1)
            if label.strip() == "spam":
                g.write(f'spam,{filter_text(text)}\n')
            else:
                g.write(f'ham,{filter_text(text)}\n')