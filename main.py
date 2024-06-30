import streamlit as st


def compute_levenshtein(char1, char2):
    len_char1, len_char2 = len(char1), len(char2)

    # If one of the tokens is empty
    if len_char1 == 0:
        return len_char2
    if len_char2 == 0:
        return len_char1

    # Initialize previous and current row
    prev_row = list(range(len_char2 + 1))
    curr_row = [0] * (len_char2 + 1)

    for i in range(1, len_char1 + 1):
        curr_row[0] = i
        for j in range(1, len_char2 + 1):
            insertion = curr_row[j - 1] + 1
            deletion = prev_row[j] + 1
            substitution = prev_row[j - 1] + (char1[i - 1] != char2[j - 1])
            curr_row[j] = min(insertion, deletion, substitution)
        # Swap rows
        prev_row, curr_row = curr_row, prev_row

    return prev_row[len_char2]


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return sorted(set([line.strip().lower() for line in lines]))


vocabs = load_vocab(file_path='./vocab.txt')


def get_correct_word(word, vocabs):
    distances = {vocab: compute_levenshtein(word, vocab) for vocab in vocabs}
    sorted_distances = sorted(distances.items(), key=lambda item: item[1])
    return sorted_distances[0][0], sorted_distances


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute") & bool(word):
        correct_word, sorted_distances = get_correct_word(word, vocabs)
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distances)


if __name__ == "__main__":
    main()
