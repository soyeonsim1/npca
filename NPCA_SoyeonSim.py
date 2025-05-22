
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

def count_adj(doc):
    return [f"{tok.text} {token.text}" for token in doc if token.pos_ in ['NOUN', 'PRON'] for tok in token.lefts if tok.pos_ == 'ADJ']

def count_rc(doc):
    return [f"{token.text} {doc[i+1].text} {' '.join([t.text for t in doc[i+1].rights])}"
            for i, token in enumerate(doc[:-2])
            if token.pos_ in ['NOUN', 'PRON'] and doc[i+1].text.lower() in {'that', 'which', 'who'} and doc[i+2].pos_ in {'VERB', 'AUX'}]

def count_nm(doc):
    return [f"{tok.text} {token.text}" for token in doc if token.pos_ in ['NOUN', 'PRON'] for tok in token.lefts if tok.pos_ == 'NOUN']

def count_poss(doc):
    return [f"{tok.text} {token.text}" for token in doc if token.pos_ in ['NOUN', 'PRON'] for tok in token.lefts if tok.dep_ == 'poss']

def count_of(doc):
    return [f"{token.text} {doc[i+1].text} {' '.join([t.text for t in doc[i+1].rights])}"
            for i, token in enumerate(doc[:-1]) if token.pos_ in ['NOUN', 'PRON'] and doc[i+1].text.lower() == 'of']

def count_prep(doc):
    return [f"{token.text} {tok.text} {' '.join([t.text for t in tok.rights])}"
            for token in doc if token.pos_ in ['NOUN', 'PRON']
            for tok in token.rights if tok.dep_ == 'prep' and tok.text.lower() != 'of']

def count_nonf(doc):
    return [f"{token.text} {tok.text} {' '.join([t.text for t in tok.rights])}"
            for token in doc if token.pos_ in ['NOUN', 'PRON']
            for tok in token.rights if tok.tag_ in {'VBG', 'VBN'}]

def count_adj_nm(doc):
    results = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ in ['NOUN', 'PRON']:
                phrase = token.text
                is_noun = is_adj = False
                for tok in reversed(list(token.lefts)):
                    if tok.pos_ == 'NOUN':
                        is_noun = True
                        phrase = f"{tok.text} {phrase}"
                    elif tok.pos_ == 'ADJ':
                        is_adj = True
                        phrase = f"{tok.text} {phrase}"
                if is_noun and is_adj:
                    results.append(phrase.strip())
    return results

def count_comp(doc):
    return [f"{token.text} {doc[i+1].text} {' '.join([t.text for t in doc[i+1].rights])}"
            for i, token in enumerate(doc[:-2])
            if token.pos_ in ['NOUN', 'PRON'] and doc[i+1].text.lower() == 'that' and doc[i+1].pos_ == 'SCONJ' and doc[i+1].dep_ == 'mark']

def count_ml(doc):
    results = []
    docs = list(doc)
    for index, token in enumerate(docs):
        if token.pos_ not in ['NOUN', 'PRON']:
            continue
        phrase = token.text
        prep_count = 0
        prep_tokens = [tok for tok in token.rights if tok.dep_ == 'prep']
        while prep_tokens:
            prep_token = prep_tokens.pop()
            phrase += f" {prep_token.text}"
            for right in prep_token.rights:
                if right.dep_ == 'pobj':
                    phrase += f" {right.text}"
                    for r in right.rights:
                        if r.dep_ == 'prep':
                            prep_tokens.append(r)
                            prep_count += 1
        if prep_count > 1:
            results.append(phrase.strip())
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
            "Noun Phrase Complexity (NPC) refers to the elaboration of noun phrases in written language.\n\n"
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
            "**For detailed information about the structures, please refer to Biber et al. (2011) and Sim (2024)."
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
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Error while plotting: {e}")

    pass


# This tells the app to run. You shouldn't need to change anything below
if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec())


