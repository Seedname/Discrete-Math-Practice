import os
import re


def parse_corpus_from_directory(input_dir, output_file):
    combined_text = ""

    # Step 1: Read and concatenate all .txt files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                combined_text += file.read() + "\n"  # Add a newline between files

    # Step 2: Remove <p> symbols
    combined_text = re.sub(r"<p>", "", combined_text)

    # Step 3: Replace all closing punctuation marks (., ?, !) with newlines
    combined_text = re.sub(r"[.!?]", "\n", combined_text)

    # Step 4: Replace all symbols with spaces, except for the single quote, which is removed later
    combined_text = re.sub(r"[^\w\s']", " ", combined_text)  # Keep letters, numbers, spaces, and single quotes

    # Step 5: Fix contractions (e.g., "do n't" -> "don't")
    contraction_patterns = [
        (r"\b([a-zA-Z]+) '([a-zA-Z]+)\b", r"\1'\2"),  # General contractions like "do n't" -> "don't"
    ]
    for pattern, replacement in contraction_patterns:
        combined_text = re.sub(pattern, replacement, combined_text)

    # Step 6: Remove single quotes not part of contractions
    combined_text = combined_text.replace("'", "")

    # Step 7: Convert everything to lowercase
    combined_text = combined_text.lower()

    # Step 8: Remove words containing letters directly next to numbers
    combined_text = re.sub(r"\b\w*\d\w*\b", "", combined_text)

    # Step 9: Collapse multiple spaces into a single space, preserving newlines
    combined_text = re.sub(r"[ \t]+", " ", combined_text)  # Replace multiple spaces with a single space
    combined_text = re.sub(r"\n\s+", "\n", combined_text)  # Ensure newlines are preserved with no trailing spaces

    # Step 10: Write the cleaned text to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_text)


# Input directory and output file paths
input_directory = "coca-samples-text"
output_file_path = "coca-text.txt"

# Run the parser
parse_corpus_from_directory(input_directory, output_file_path)

print("Parsing complete. Output written to", output_file_path)
