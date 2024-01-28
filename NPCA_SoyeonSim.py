
############# NPC Analyzer ##############
# Developed by Soyeon Sim
# Description: The NPC (noun phrase complexity) analyzer identifies and counts the 10 noun phrase structures across the hypothesized stages proposed by Biber et al. (2011)
# NPC variables:
    # Stage 2: Attribute adjectives as premodifiers (e.g. It has a nice flavor.)
    # Stage 3: That relative clauses with animate head nouns (e.g. the man that was nice to me.), Nouns as premodifiers (e.g. cable channel), Possessive nouns as premodifiers (e.g. Mary's voice), Of phrase as postmodifers (e.g. chair of committee), Simple PPs as postmodifiers (prepositions other than of) (e.g. house in the country)
    # Stage 4: Nonfinite relative clauses (e.g. studies adopting this method), More phrasal embedding in the NP (e.g. Positive propagule size effects)
    # Stage 5: Complement clauses controlled by nouns (e.g. The hypothesis that female body weight was more variable.), Extensive phrasl embedding in the NP (multiple prepositional phrases as postmodifiers, with levels of embedding) (e.g. The presence of layered structures at the borderline of cell territories)
# The tool generates the raw and normed frequencies of each structures of a text file in a single row of csv. file.
# Multiple texts in the working directory could be iterated.
# pyside6-uic NPCA.ui -o NPCA_gui.py


# After converting the .ui to .py, use an import statement to import the gui into this script
from NPCA_gui import *
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QMessageBox, QMainWindow, QLabel, QApplication
from PySide6.QtCore import Qt
import glob
import re
import statistics
import sys
import spacy

nlp = spacy.load('en_core_web_sm')


# Double check that the second argument (Ui_MainWindow) exactly matches the name of the class in your gui.py file
class MainWindow(QMainWindow, Ui_MainWindow):  # https://docs.python.org/3/tutorial/classes.html

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # Assigning functionality to the button that was named "pushButton_select_files" in QT Designer
        self.pushButton_2.clicked.connect(self.set_input_folder)
        self.pushButton.clicked.connect(self.run_process)
        self.folder_label = QLabel()
        self.folder_label.setAlignment(Qt.AlignTop)
        self.scrollArea.setWidget(self.folder_label)
        self.input_folder = ""

    def set_input_folder(self):
        # The folder selected will be opened
        selected_folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if selected_folder:
            self.folder_label.setText(f"{selected_folder}")
            self.input_folder = selected_folder

    # Defining a function
    def run_process(self):
        if not self.input_folder:
            QMessageBox.warning(self, 'Warning', 'Please select a folder using "Find Folder" button.')
            return

        # The folder selected will be opened
        selected_folder = QFileDialog.getExistingDirectory(self, 'pushButton')
        # if selected_folder:
        #     self.folder_label.setText(f"{selected_folder}")

        # Get the csv file name from the testEdit widget
        output_file_name = self.textEdit.toPlainText()
        output_file_path = os.path.join(selected_folder, f'{output_file_name}.csv')

        try:
            print('Before opening the output file')
            with open(output_file_path, 'w+') as out_file:
                # Write the output file
                out_file.write('file, Number of words, adj_raw, adj_normed, rc_raw, rc_normed, nm_raw, nm_normed, poss_raw, poss_normed, of_raw, of_normed, prep_raw, prep_normed, nonf_raw, nonf_normed, adj_nm_raw, adj_nm_normed, comp_raw, comp_normed, ml_raw, ml_normed')

                # TO READ IN THE TEXT OF EACH FILE
                for file_name in glob.glob(os.path.join(selected_folder, '*')):
                    print(f'Processing file: {file_name}')
                    # Open each file here
                    with open(file_name, encoding = 'utf-8', errors = 'ignore') as file:

                        # Initialize word_count and set its value to 0
                        word_count = 0

                        # Initialize the npc counters for each text file and set its value to 0
                        adj_count = 0
                        rc_count = 0
                        nm_count = 0
                        poss_count = 0
                        of_count = 0
                        prep_count = 0
                        nonf_count = 0
                        adj_nm_count = 0
                        comp_count = 0
                        ml_count = 0

                        # Create a list of the 10 features
                        adj = []
                        rc = []
                        nm = []
                        poss = []
                        of = []
                        prep = []
                        nonf = []
                        adj_nm = []
                        comp = []
                        ml = []

                        text = file.read()
                        words = text.split()

                        doc = nlp(text)
                        print('FILE NAME: ', file_name)
                        #### STAGE 2: Attribute adjectives as premodifiers (adj)
                        for token in doc:
                            # print(f"word: {token.text}, POS: {token.pos_}, Tag: {token.tag_}, Tag explanation: {spacy.explain(token.tag_)} Dependency: {token.dep_}, Dependency explanation: {spacy.explain(token.dep_)}")
                            # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Initialize a variable to store the current phrase
                                current_phrase = ""

                                # Iterate over left-hand heads
                                for tok in token.lefts:
                                    if tok.pos_ == 'ADJ':
                                        current_phrase = ' '.join(
                                            [t.text for t in tok.lefts]) + ' ' + tok.text + ' ' + token.text
                                        break

                                # If there is an adjective, append the phrase to the list
                                if current_phrase:
                                    adj.append(current_phrase)

                        print('adj: ', adj)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        adj_count = len(adj)
                        word_count = len(words)
                        adj_normed_freq = round(adj_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 3: That relative caluses with animate head nouns (rc)

                        # Iterate through each token in the processed document
                        for i, token in enumerate(doc[:-2]):  # Avoid checking the last two tokens
                            # Check if the token is a noun or pronoun
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Get the next token
                                next_token = doc[i + 1]
                                next2_token = doc[i + 2]
                                # Check if the lowercase text of the next token is in the set of relative pronouns
                                if next_token.text.lower() in {'that', 'which', 'who'}:
                                    # Check if the next token is a verb
                                    if next2_token.pos_ == 'VERB' or 'AUX':
                                        # Construct the relative clause phrase
                                        current_phrase = f"{token.text} {next_token.text} {' '.join([t.text for t in next_token.rights])}"
                                        rc.append(current_phrase)
                        print('rc: ', rc)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        rc_count = len(rc)
                        word_count = len(words)
                        rc_normed_freq = round(rc_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 3: Nouns as premodifiers (nm)

                        for token in doc:
                            # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Initialize a variable to store the current phrase
                                current_phrase = ""

                                # Iterate over left-hand heads
                                for tok in token.lefts:
                                    if tok.pos_ == 'NOUN':
                                        current_phrase = ' '.join(
                                            [t.text for t in tok.lefts]) + ' ' + tok.text + ' ' + token.text
                                        break

                                # Append the current phrase to the total list of nm
                                if current_phrase:
                                    nm.append(current_phrase)

                        print('nm: ', nm)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        nm_count = len(nm)
                        word_count = len(words)
                        nm_normed_freq = round(nm_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 3: Possessive nouns as premodifiers (poss)

                        for token in doc:
                            # print(f"word: {token.text}, POS: {token.pos_}, Tag: {token.tag_}, Dependency: {token.dep_}, Dependency explanation: {spacy.explain(token.dep_)}")
                            # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Initialize a variable to store the current phrase
                                current_phrase = ""

                                # Iterate over left-hand heads
                                for tok in token.lefts:
                                    if tok.dep_ == 'poss':
                                        print(f">>>>>>>{tok.text} {tok.pos_} {tok.dep_}")
                                        current_phrase = ' '.join(
                                            [t.text for t in tok.lefts]) + ' ' + tok.text + ' ' + token.text
                                        break

                                # If there is an adjective, append the phrase to the list
                                if current_phrase:
                                    poss.append(current_phrase)

                        print('poss: ', poss)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        poss_count = len(poss)
                        word_count = len(words)
                        poss_normed_freq = round(poss_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 3: Of phrase as postmodifiers (of)

                        # Iterate through each token in the processed document
                        for i, token in enumerate(
                                doc[:-1]):  # Avoid checking the last token since there's no "next" token for it
                            # Check if the token is a noun or pronoun
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Get the next token
                                next_token = doc[i + 1]
                                # Check if the lowercase text of the next token is the preposition 'of'
                                if next_token.text.lower() == 'of':
                                    # Construct the relative clause phrase
                                    current_phrase = f"{token.text} {next_token.text} {' '.join([t.text for t in next_token.rights])}"
                                    of.append(current_phrase)
                        print('of: ', of)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        of_count = len(of)
                        word_count = len(words)
                        of_normed_freq = round(of_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 3: Simple PPs as postmodifiers (prepositions other than of) (prep)

                        for token in doc:
                            # print(f"word: {token.text}, POS: {token.pos_}, Tag: {token.tag_}, Dependency: {token.dep_}, Dependency explanation: {spacy.explain(token.dep_)}")
                            # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Initialize a variable to store the current phrase
                                current_phrase = ""

                                # Iterate over right-hand heads
                                for tok in token.rights:
                                    if tok.dep_ == 'prep' and tok.text.lower() != 'of':
                                        current_phrase = f"{token.text} {tok.text} {' '.join([t.text for t in tok.rights])}"
                                        break

                                # Add the current phrase to the list if it's not empty
                                if current_phrase:
                                    prep.append(current_phrase)

                        print('prep: ', prep)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        prep_count = len(prep)
                        word_count = len(words)
                        prep_normed_freq = round(prep_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 4: Nonfinite relative clauses (nonf)

                        for token in doc:
                            # print(f"word: {token.text}, POS: {token.pos_}, POS explain: {spacy.explain(token.pos_)}Tag: {token.tag_}, Dependency: {token.dep_}, Dependency explanation: {spacy.explain(token.dep_)}")
                            # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Initialize a variable to store the current phrase
                                current_phrase = ""

                                # Iterate over right-hand heads
                                for tok in token.rights:
                                    if tok.tag_ == 'VBG' or tok.tag_ == 'VBN':
                                        current_phrase = f"{token.text} {tok.text} {' '.join([t.text for t in tok.rights])}"
                                        break

                                # Add the current phrase to the list if it's not empty
                                if current_phrase:
                                    nonf.append(current_phrase)
                        print('nonf: ', nonf)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        nonf_count = len(nonf)
                        word_count = len(words)
                        nonf_normed_freq = round(nonf_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 4: More phrasal embedding in the NP (attributive adjectives, nouns as premodifiers) (adj_nm)
                        for sent in doc.sents:
                            for token in sent:
                                is_noun_found = False
                                is_adj_found = False

                                # print(f"word: {token.text}, POS: {token.pos_}, Tag: {token.tag_}, Dependency: {token.dep_}, Dependency explanation: {spacy.explain(token.dep_)}")
                                # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                                if token.pos_ in ['NOUN', 'PRON']:
                                    # print(f"F>>>>>>>{token.text} {token.pos_} {token.dep_}")
                                    # Initialize a variable to store the current phrase
                                    current_phrase = token.text
                                    for tok in reversed(list(token.lefts)):
                                        if tok.pos_ == 'NOUN':
                                            is_noun_found = True
                                            current_phrase = f"{tok.text} {current_phrase}"
                                        elif tok.pos_ == 'ADJ':
                                            is_adj_found = True
                                            current_phrase = f"{tok.text} {current_phrase}"

                                    # Add the current phrase to the list if it matches the pattern
                                    if current_phrase and is_noun_found and is_adj_found:
                                        adj_nm.append(current_phrase)

                        print('adj_nm: ', adj_nm)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        adj_nm_count = len(adj_nm)
                        word_count = len(words)
                        adj_nm_normed_freq = round(adj_nm_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 5: Complement clauses controlled by nouns (comp)

                        # Iterate through each token in the processed document
                        for i, token in enumerate(doc[:-2]):  # Avoid checking the last two tokens
                            # Check if the token is a noun or pronoun
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Get the next token
                                next_token = doc[i + 1]

                                # Check if the lowercase text of the next token is in the set of relative pronouns
                                if next_token.text.lower() == 'that' and next_token.pos_ == 'SCONJ' and next_token.dep_ == 'mark':
                                    # Construct the relative clause phrase
                                    current_phrase = f"{token.text} {next_token.text} {' '.join([t.text for t in next_token.rights])}"
                                    comp.append(current_phrase)
                        print('comp: ', comp)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        comp_count = len(comp)
                        word_count = len(words)
                        comp_normed_freq = round(comp_count / word_count * 1000, 2) if word_count != 0 else 0

                        #### STAGE 5: Extensive phrasal embedding in the NP (ml)
                        # convert the doc to a list for easier indexing
                        docs = list(doc)
                        token = None

                        for index, _ in enumerate(docs):
                            # if this token has been processed, we want to skip
                            if token is not None and token.i >= index:
                                continue
                            token = docs[index]
                            # If the POS of the token is noun or pronoun, start a while loop that iterates over left-hand heads
                            if token.pos_ in ['NOUN', 'PRON']:
                                # print(f">>>>>>>{token.text} {token.pos_} {token.dep_}")
                                # Initialize a variable to store the current phrase
                                current_phrase = token.text
                                next_right_token_found = False
                                prep_count = 0
                                prep_tokens = []
                                for tok in token.rights:
                                    if tok.dep_ == 'prep':
                                        prep_tokens.append(tok)
                                        prep_count += 1
                                while len(prep_tokens) != 0:
                                    prep_token = prep_tokens.pop()
                                    current_phrase = f"{current_phrase} {prep_token.text}"
                                    for right in prep_token.rights:
                                        if right.dep_ == 'pobj':
                                            current_phrase = f"{current_phrase} {right.text}"
                                            if token.i < right.i:
                                                token = right
                                            for r in right.rights:
                                                if r.dep_ == 'prep':
                                                    prep_tokens.append(r)
                                                    prep_count += 1
                                # Add the current phrase to the list if it's not empty and proposition count is more than 1
                                if current_phrase and prep_count > 1:
                                    ml.append(current_phrase)

                        print('ml: ', ml)

                        # Once the program reaches the end of the file, calculate the raw frequency and normed frequency per 1000 words
                        ml_count = len(ml)
                        word_count = len(words)
                        ml_normed_freq = round(ml_count / word_count * 1000, 2) if word_count != 0 else 0

                        # Write out the results to the out_file
                        out_file.write(f"{file_name},{word_count},{adj_count},{adj_normed_freq},{rc_count},{rc_normed_freq},{nm_count},{nm_normed_freq},{poss_count},{poss_normed_freq},{of_count},{of_normed_freq},{prep_count},{prep_normed_freq},{nonf_count},{nonf_normed_freq},{adj_nm_count},{adj_nm_normed_freq},{comp_count},{comp_normed_freq},{ml_count},{ml_normed_freq}\n")
                        print('After writing to the output file')
            QMessageBox.information(self, 'Success', f'CSV file "{output_file_path}" generated successfully.')
        except Exception as e:
            print(f'Error: {e}')
            # Inform user about the error
            QMessageBox.critical(self, 'Error', f'Error generating CSV file: {str(e)}')
    pass


# This tells the app to run. You shouldn't need to change anything below
if __name__ == "__main__":
    import os
    import sys
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    # app.setStyle('Fusion')
    sys.exit(app.exec())


