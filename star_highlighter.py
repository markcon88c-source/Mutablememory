# star_highlighter.py
# Viewer-only module for highlighting L1 words with a star emoji 🌟
# This does NOT modify memory, pressures, STM, or any organ math.

STAR = "🌟"

def highlight_L1_words(sentence, memory_state):
    """
    Highlights any word in the sentence that appears in Level 1 memory.

    Parameters:
        sentence (str): The raw sentence emitted by SentenceOrgan.
        memory_state (dict): The full memory structure, including L1–L11.

    Returns:
        str: The sentence with L1 words marked with a star emoji.
    """

    # 1. Get L1 words (surface memory)
    L1_words = set(memory_state.get("L1", []))

    # 2. Tokenize the sentence
    tokens = sentence.split()

    # 3. Highlight tokens that appear in L1
    highlighted_tokens = []
    for token in tokens:
        # Strip punctuation for matching, but preserve original token
        stripped = token.strip(".,!?;:\"'()[]{}")
        if stripped in L1_words:
            highlighted_tokens.append(token + STAR)
        else:
            highlighted_tokens.append(token)

    # 4. Reassemble the sentence
    highlighted_sentence = " ".join(highlighted_tokens)
    return highlighted_sentence
