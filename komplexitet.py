def choose_file():
    """Chooses a valid file

    Returns:
        string: The chosen file name
    """
    valid_choice = False
    while not valid_choice:
        print(f"Välj vilken korpus-fil som ska analyseras...\n")
        print(
            "För \'729G49-8S.conllx\', skriv \'1\'\n    (8 sidor)\n"
        )
        print(
            "För \'729G49-GP.conllx\', skriv \'2\'\n    (Göteborgsposten)\n"
        )
        file_choice = input(f"Val: ")
        if file_choice == "1":
            valid_choice = True
            return "729G49-8S.conllx"
        elif file_choice == "2":
            valid_choice = True
            return "729G49-GP.conllx"
        else:
            print(
                f"\'{file_choice}\' är inte en giltig input. "
                f"Var god välj antingen \'1\' eller \'2\'!\n"
            )


def sentence_generator(source):
    """Split a source into sentences .

    Args:
        source (conllx-file): Corpus-file

    Yields:
        generator-object: Containing a sentence from the corpus
    """
    sentence_list = []
    for word in source:
        if word != "\n":
            sentence_list.append(word.split())
        else:
            yield sentence_list
            sentence_list = []


def nominal_ratio(corpus):
    """Calculates the nominal ratio of the corpus .

    Args:
        corpus (conllx-file): Corpus-file

    Returns:
        float: Nominal ratio of the corpus
    """
    NOMINAL_TAGS = ["NN", "PP", "PC"]
    VERBAL_TAGS = ["VB", "PN", "AB"]
    nominal_count = 0
    verbal_count = 0
    for sentence in sentence_generator(corpus):
        for word in sentence:
            word_type = word[3]
            if any(x in word_type for x in NOMINAL_TAGS):
                nominal_count += 1
            elif any(x in word_type for x in VERBAL_TAGS):
                verbal_count += 1
    return round(nominal_count/verbal_count, 3)


def average_dependence_length(corpus):
    """Calculates the average length of dependence between words in a corpus .

    Args:
        corpus (conllx-file): Corpus-file

    Returns:
        float: Average length of dependence
    """
    PUNCT_TAGS = ["MAD", "MID", "PAD"]
    dependency_counter = 0
    total_dependence_length = 0
    DEPENDENCE_NUMBER_INDEX = 6
    ROOT_INDEX = 7
    for sentence in sentence_generator(corpus):
        for word in sentence:
            word_type = word[3]
            if word[ROOT_INDEX] != "ROOT" and word_type not in PUNCT_TAGS:
                word_root = int(word[DEPENDENCE_NUMBER_INDEX])
                if word_root != 0:
                    dependency_counter += 1
                    word_index = int(word[0])
                    total_dependence_length += abs(word_index - word_root)
    return round(total_dependence_length / dependency_counter, 3)


def print_nominal_ratio_and_dependence_length():
    """Prints the nominal ratio and dependence length .
    """
    chosen_corpus = choose_file()
    with open(chosen_corpus, encoding="UTF-8") as corpus:
        print(f"\nNominalkvot: {nominal_ratio(corpus)}")

    with open(chosen_corpus, encoding="UTF-8") as corpus:
        print(
            f"Genomsnittlig dependenslängd: "
            f"{average_dependence_length(corpus)}\n"
        )


print_nominal_ratio_and_dependence_length()
