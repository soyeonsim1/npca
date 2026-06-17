
############# NPC Analyzer ##############
# Developed by Soyeon Sim & Dr. Daniel H. Dixon
# Description: The NPC (noun phrase complexity) analyzer identifies and counts the 10 noun phrase structures across the hypothesized stages proposed by Biber et al. (2011)
# NPC variables:
    # Stage 2: Attribute adjectives as premodifiers (e.g. It has a nice flavor.)
    # Stage 3: Finite relative clauses with head nouns (e.g. the man that was nice to me.), Nouns as premodifiers (e.g. cable channel), Possessive nouns as premodifiers (e.g. Mary's voice), Of phrase as postmodifers (e.g. chair of committee), Simple PPs as postmodifiers (prepositions other than of) (e.g. house in the country)
    # Stage 4: Nonfinite relative clauses (e.g. studies adopting this method), More phrasal embedding in the NP (e.g. Positive propagule size effects)
    # Stage 5: Complement clauses controlled by nouns (e.g. The hypothesis that female body weight was more variable.), Extensive phrasl embedding in the NP (multiple prepositional phrases as postmodifiers, with levels of embedding) (e.g. The presence of layered structures at the borderline of cell territories)
# The tool generates the raw and normed frequencies of each structures of a text file in a single row of csv. file.
# Multiple texts in the working directory could be iterated.
# pyside6-uic NPCA.ui -o NPCA_gui.py


# After converting the .ui to .py, use an import statement to import the gui into this script
from NPCA_gui_updated import *
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QMessageBox, QMainWindow, QLabel, QApplication, QDialog, QPushButton
from PySide6.QtCore import Qt
import glob
import os
import re
import statistics
import sys
import spacy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

nlp = spacy.load('en_core_web_sm')

def normed(count, word_count):
    return round(count / word_count * 1000, 2) if word_count else 0

def sorted_text(tokens):
    return " ".join(tok.text for tok in sorted(set(tokens), key=lambda x: x.i))

def count_adj(doc):
    """
    Attributive adjectives as premodifiers.
    e.g.,
        a nice flavor
        the red car

    Excludes predicative adjectives:
        e.g., the car is nice
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.lefts:
            # adjectival modifier directly attached to noun
            if child.dep_ == "amod" and child.pos_ == "ADJ":
                results.append(f"{child.text} {head.text}")

    return results

def count_rc(doc):
    """
    Count finite relative clauses modifying nouns/pronouns.
    e.g.,
        the man who was nice to me
        the book that I bought
        the person who lives next door

    """
    results = []
    relativizers = {"who", "which", "that", "whom", "whose"}

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        # Search descendants / nearby right dependents for a relativizer
        # that introduces a finite clause attached to this noun.
        for child in head.rights:
            # Case 1: relativizer directly attached near the noun
            if child.text.lower() in relativizers:
                # Look for a finite verb / auxiliary associated with the clause
                clause_tokens = [child] + list(child.subtree)
                has_finite_verb = any(
                    tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VBG", "VBN", "VB"}
                    for tok in clause_tokens
                )
                if has_finite_verb:
                    phrase = " ".join(tok.text for tok in sorted(set(clause_tokens), key=lambda x: x.i))
                    results.append(f"{head.text} {phrase}".strip())

            # Case 2: clause attached as acl/relcl to the noun
            elif child.dep_ in {"acl", "relcl"}:
                subtree = list(child.subtree)

                has_relativizer = any(tok.text.lower() in relativizers for tok in subtree)
                has_finite_verb = any(
                    tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VBG", "VBN", "VB"}
                    for tok in subtree
                )

                if has_relativizer and has_finite_verb:
                    phrase = " ".join(tok.text for tok in subtree)
                    results.append(f"{head.text} {phrase}".strip())

    return results

def count_nm(doc):
    """
    Nouns as premodifiers.

    e.g.,
        cable channel
        school teacher
        government report
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.lefts:
            if child.pos_ == "NOUN" and child.dep_ == "compound":
                results.append(f"{child.text} {head.text}")

    return results

def count_poss(doc):
    """
    Possessive nouns as premodifiers.

    e.g.,
        Mary's voice
        the student's book
        John's car
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.lefts:
            if child.dep_ == "poss":
                results.append(f"{child.text} {head.text}")

    return results

def count_of(doc):
    """
    Of-phrases as noun postmodifiers.
    Examples:
        chair of the committee
        the end of the road
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.children:
            # prepositional dependent headed by "of"
            if child.dep_ == "prep" and child.text.lower() == "of":
                phrase = sorted_text(child.subtree)
                results.append(f"{head.text} {phrase}")
    return results


def count_prep(doc):
    """
    Simple prepositional phrases as postmodifiers of nouns,
    excluding of-phrases

    e.g.,
        house in the country
        students with good grades
        the book on the table
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.children:
            if child.dep_ == "prep" and child.text.lower() != "of":
                phrase = " ".join(tok.text for tok in child.subtree)
                results.append(f"{head.text} {phrase}")

    return results

def count_nonf(doc):
    """
    Nonfinite relative clauses as postmodifiers.
    e.g.,
        students studying abroad
        the method used in the experiment
        a book written by Orwell

    Targets participial clause postmodifiers attached to nouns.
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.children:
            # participial clausal modifier of the noun
            if child.dep_ == "acl" and child.tag_ in {"VBG", "VBN"}:
                phrase = sorted_text(child.subtree)
                results.append(f"{head.text} {phrase}")

    return results

def count_adj_nm(doc):
    """
    Multiple premodifiers: adjective + noun + head noun
    e.g.,
        medical school teacher
        large government report

    Requires at least one adjectival premodifier and one noun premodifier attached to the same head noun.
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        adjs = []
        nouns = []

        for child in head.lefts:
            if child.dep_ == "amod" and child.pos_ == "ADJ":
                adjs.append(child)
            elif child.dep_ == "compound" and child.pos_ == "NOUN":
                nouns.append(child)

        if adjs and nouns:
            phrase_tokens = adjs + nouns + [head]
            phrase = sorted_text(phrase_tokens)
            results.append(phrase)

    return results

def count_comp(doc):
    """
    Count noun complement clauses used as postmodifiers.
    e.g.,
        the fact that he left
        the idea that we should wait
        a chance to win
        permission to leave

    - Includes both that-clause complements and to-infinitive complements.

    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for child in head.rights:
            # 1) that-clause complement:
            if child.text.lower() == "that" and child.pos_ == "SCONJ" and child.dep_ == "mark":
                clause_head = child.head

                # Make sure this clause is linked back to the noun
                if clause_head.i > head.i:
                    subtree = list(clause_head.subtree)

                    has_finite_verb = any(
                        tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VBG", "VBN", "VB"}
                        for tok in subtree
                    )
                    has_relativizer = any(
                        tok.text.lower() in {"who", "which", "whom", "whose"}
                        for tok in subtree
                    )

                    if has_finite_verb and not has_relativizer:
                        phrase = " ".join(tok.text for tok in subtree)
                        results.append(f"{head.text} {phrase}".strip())

            # 2) to-infinitive complement:
            elif child.dep_ == "acl" and child.tag_ == "VB":
                subtree = list(child.subtree)
                has_to = any(tok.text.lower() == "to" and tok.dep_ == "aux" for tok in subtree)
                if has_to:
                    phrase = " ".join(tok.text for tok in subtree)
                    results.append(f"{head.text} {phrase}".strip())

            # where spaCy labels infinitival postmodifiers differently
            elif child.dep_ == "acl" and child.pos_ == "VERB":
                subtree = list(child.subtree)
                has_to = any(tok.text.lower() == "to" for tok in subtree)
                is_nonfinite = child.tag_ == "VB"
                if has_to and is_nonfinite:
                    phrase = " ".join(tok.text for tok in subtree)
                    results.append(f"{head.text} {phrase}".strip())
    return results

def count_ml(doc):
    """
    Multiple prepositional phrase embeddings as postmodifiers.
    e.g.,
        the development of structural complexity through recursive expansion
        the presence of layered structures at the borderline of cell territories

    This function identifies noun heads followed by a PP postmodifier
    whose object contains another PP, indicating embedded PP structure.
    """
    results = []

    for head in doc:
        if head.pos_ not in {"NOUN", "PRON"}:
            continue

        for prep in head.children:
            if prep.dep_ != "prep":
                continue

            found_embedding = False
            phrase_tokens = [head] + list(prep.subtree)

            # Find object of the first PP
            for pobj in prep.children:
                if pobj.dep_ == "pobj":
                    # Check whether the object itself has another PP
                    for child in pobj.children:
                        if child.dep_ == "prep":
                            found_embedding = True
                            phrase_tokens.extend(list(child.subtree))

            if found_embedding:
                phrase = " ".join(
                    tok.text for tok in sorted(set(phrase_tokens), key=lambda x: x.i)
                )
                results.append(phrase)

    return results

class NPCInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("What is NPC?")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(
            "Noun Phrase Complexity (NPC) refers to the elaboration of noun phrases in language.\n\n"
            "This tool follows the developmental stages proposed by Biber et al. (2011):\n\n"
            "Stage 2: Attribute adjectives as premodifiers (e.g., a nice flavor)\n"
            "Stage 3: Relative clauses, noun modifiers, possessives, of-phrases, simple PPs\n"
            "Stage 4: Nonfinite relatives and more phrasal embedding\n"
            "Stage 5: Complement clauses and extensive phrasal embedding\n\n"
            "Analyzing these structures can reveal patterns in syntactic development over time.\n\n\n"
            
            "Index manual\n"
            "adj: Attribute adjective + Noun\n"
            "rc: Noun + That relative clauses\n"
            "nm: Noun + Noun\n"
            "poss: Possessive noun + Noun\n"
            "of: Noun + of phrase\n"
            "prep: Noun + simple PP (other than of)\n"
            "nonf: Noun + nonfinite relative clause\n"
            "adj_nm: Adjective + Noun + Noun\n"
            "comp: Noun + complement clause\n"
            "ml: Noun + multiple PPs as postmodifiers\n\n"
            "**For detailed information about the structures, please refer to the following source.\n"
            "Biber, D., Gray, B., & Poonpon, K. (2011). Should We Use Characteristics of Conversation to Measure Grammatical Complexity in L2 Writing Development? TESOL Quarterly, 45(1), 5–35."
        )
        layout.addWidget(self.text_edit)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

# -------------Main window class---------------
class MainWindow(QMainWindow, Ui_MainWindow):  # https://docs.python.org/3/tutorial/classes.html

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # Assigning functionality to the button that was named "pushButton_select_files" in QT Designer
        self.pushButton_2.clicked.connect(self.set_input_folder)
        self.pushButton.clicked.connect(self.run_process)
        self.pushButton_3.clicked.connect(self.show_npc_info)
        self.pushButton_4.clicked.connect(self.set_output_folder)
        self.pushButton_3.setCursor(Qt.PointingHandCursor)
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                background-color: rgb(240, 248, 255);
                border: 1px solid #8f8f91;
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: rgb(225, 240, 255);
            }
            QPushButton:pressed {
                background-color: rgb(200, 220, 240);
            }
        """)
        self.folder_label = QLabel()
        self.folder_label.setAlignment(Qt.AlignTop)
        self.scrollArea.setWidget(self.folder_label)
        self.input_folder = ""
        self.output_folder = ""

    def set_input_folder(self):
        # The folder selected will be opened
        selected_folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if selected_folder:
            self.folder_label.setText(f"{selected_folder}")
            self.input_folder = selected_folder

    def set_output_folder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        if selected_folder:
            self.output_folder = selected_folder

    def get_all_columns(self):
        return ['adj_raw', 'adj_normed', 'rc_raw', 'rc_normed', 'nm_raw', 'nm_normed', 'poss_raw', 'poss_normed',
                'of_raw', 'of_normed', 'prep_raw', 'prep_normed', 'nonf_raw', 'nonf_normed', 'adj_nm_raw',
                'adj_nm_normed', 'comp_raw', 'comp_normed', 'ml_raw', 'ml_normed']

    # Defining a function
    def run_process(self):
        if not self.input_folder:
            QMessageBox.warning(self, 'Warning', 'Please select a folder using "Find Folder" button.')
            return
        if not self.output_folder:
            QMessageBox.warning(self, 'Warning', 'Please select an output folder using "Find Folder" button.')

        selected_columns = []
        all_columns = self.get_all_columns()
        freq_raw = self.checkBox.isChecked()
        freq_normed = self.checkBox_2.isChecked()

        if self.checkBox_3.isChecked():
            if freq_raw:
                selected_columns.append('adj_raw')
            if freq_normed:
                selected_columns.append('adj_normed')
        if self.checkBox_4.isChecked():  # Stage 3
            stage3 = ['rc', 'nm', 'poss', 'of', 'prep']
            for prefix in stage3:
                if freq_raw:
                    selected_columns.append(f'{prefix}_raw')
                if freq_normed:
                    selected_columns.append(f'{prefix}_normed')

        if self.checkBox_5.isChecked():  # Stage 4
            stage4 = ['nonf', 'adj_nm']
            for prefix in stage4:
                if freq_raw:
                    selected_columns.append(f'{prefix}_raw')
                if freq_normed:
                    selected_columns.append(f'{prefix}_normed')

        if self.checkBox_6.isChecked():  # Stage 5
            stage5 = ['comp', 'ml']
            for prefix in stage5:
                if freq_raw:
                    selected_columns.append(f'{prefix}_raw')
                if freq_normed:
                    selected_columns.append(f'{prefix}_normed')

        selected_columns = sorted(set(selected_columns))
        if not selected_columns:
            QMessageBox.warning(self, 'Warning', 'Please select at least one checkbox before running the analysis.')
            return


        # Get the csv file name from the testEdit widget
        output_file_name = self.textEdit.toPlainText()
        output_file_path = os.path.join(self.output_folder, f'{output_file_name}.csv')

        self.pushButton.setText("Processing...")
        self.pushButton.setEnabled(False)
        self.progressBar.setValue(0)
        QApplication.processEvents()

        try:
            print('Before opening the output file')
            with open(output_file_path, 'w+', encoding='utf-8') as out_file:
                header = ['file', 'Number of words'] + selected_columns
                out_file.write(','.join(header) + '\n')

                file_list = glob.glob(os.path.join(self.input_folder, '*'))
                total_files = len(file_list)


                for i, file_name in enumerate(file_list):
                    # Open each file here
                    with open(file_name, encoding = 'utf-8', errors = 'ignore') as file:
                        text = file.read()
                        words = text.split()
                        word_count = len(words)
                        doc = nlp(text)

                        adj = count_adj(doc)
                        rc = count_rc(doc)
                        nm = count_nm(doc)
                        poss = count_poss(doc)
                        of = count_of(doc)
                        prep = count_prep(doc)
                        nonf = count_nonf(doc)
                        adj_nm = count_adj_nm(doc)
                        comp = count_comp(doc)
                        ml = count_ml(doc)

                        # Compute counts and normed freqs
                        results = {
                            'adj_raw': len(adj), 'adj_normed': normed(len(adj), word_count),
                            'rc_raw': len(rc), 'rc_normed': normed(len(rc), word_count),
                            'nm_raw': len(nm), 'nm_normed': normed(len(nm), word_count),
                            'poss_raw': len(poss), 'poss_normed': normed(len(poss), word_count),
                            'of_raw': len(of), 'of_normed': normed(len(of), word_count),
                            'prep_raw': len(prep), 'prep_normed': normed(len(prep), word_count),
                            'nonf_raw': len(nonf), 'nonf_normed': normed(len(nonf), word_count),
                            'adj_nm_raw': len(adj_nm), 'adj_nm_normed': normed(len(adj_nm), word_count),
                            'comp_raw': len(comp), 'comp_normed': normed(len(comp), word_count),
                            'ml_raw': len(ml), 'ml_normed': normed(len(ml), word_count)
                        }

                        row = [os.path.basename(file_name), str(word_count)]
                        for col in selected_columns:
                            row.append(str(results.get(col, 0)))
                        out_file.write(','.join(row) + '\n')

                    # Update progress bar
                    progress = int((i + 1) / total_files * 100)
                    self.progressBar.setValue(progress)
                    QApplication.processEvents()

            self.progressBar.setValue(100)
            QMessageBox.information(self, 'Success', f'CSV file "{output_file_path}" generated successfully.')

            if self.checkBox_7.isChecked():
                self.plot_bar_graph()

        except Exception as e:
            print(f'Error: {e}')
            # Inform user about the error
            QMessageBox.critical(self, 'Error', f'Error generating CSV file: {str(e)}')

        self.pushButton.setText("Start the analysis")
        self.pushButton.setEnabled(True)

    def show_npc_info(self):
        dialog = NPCInfoDialog(self)
        dialog.exec()

    def plot_bar_graph(self):
        try:
            # Only run if checkbox is checked
            if not self.checkBox_7.isChecked():
                return

            # Ensure output file exists
            output_file_name = self.textEdit.toPlainText()
            output_file_path = os.path.join(self.output_folder, f'{output_file_name}.csv')

            if not os.path.exists(output_file_path):
                QMessageBox.warning(self, 'Warning', 'Output CSV file not found. Please run the analysis first.')
                return

            # Load the data
            df = pd.read_csv(output_file_path)

            # Get selected normed columns only
            normed_cols = [col for col in self.get_all_columns() if col.endswith('_normed') and col in df.columns]

            if not normed_cols:
                QMessageBox.information(self, 'Info', 'No normalized frequency variables selected for plotting.')
                return

            # Calculate means
            mean_values = df[normed_cols].mean().sort_values(ascending=False)

            # Plot
            plt.figure(figsize=(10, 6))
            mean_values.plot(kind='bar')
            plt.ylabel('Mean Normalized Frequency per 1,000 words')
            plt.xlabel('Noun Phrase Feature')
            plt.title('Mean Normalized Frequencies of Selected NP Structures')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.grid(axis='y', linestyle='--', linewidth=0.5)

            # Save image
            plot_path = os.path.join(
                self.output_folder,
                f"{output_file_name}_NPC_plot.png"
            )

            # Save the plot
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()

            if sys.platform == "darwin":
                os.system(f'open "{plot_path}"')

            QMessageBox.information(
                self,
                'Success',
                f'Bar graph saved as:\n{plot_path}'
            )

            plt.show()
            plt.savefig(os.path.join(self.output_folder, 'NPC_plot.png'))

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Error while plotting: {e}")

    pass


# This tells the app to run. You shouldn't need to change anything below
if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec())


