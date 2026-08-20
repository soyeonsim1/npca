############# Noun Phrase Complexity Analyzer (NPCA) ##############
# Ver.3, 072426; main updates: comp, rc, nonf refined/ poss -> restricted to only possessive nouns/
# Developed by Soyeon Sim & Dr. Daniel H. Dixon
# Description: The NPCA identifies and counts the 10 noun phrase structures across the hypothesized stages proposed by Biber et al. (2011)
# NPC variables:
    # Stage 2: Attribute adjectives as premodifiers (e.g. It has a nice flavor.)
    # Stage 3: Finite relative clauses with head nouns (e.g. the man that was nice to me.), Nouns as premodifiers (e.g. cable channel), Possessive nouns as premodifiers (e.g. Mary's voice), Of phrase as postmodifers (e.g. chair of committee), Simple PPs as postmodifiers (prepositions other than of) (e.g. house in the country)
    # Stage 4: Nonfinite relative clauses (e.g. studies adopting this method), More phrasal embedding in the NP (e.g. Positive propagule size effects)
    # Stage 5: Complement clauses controlled by nouns (e.g. The hypothesis that female body weight was more variable.), Extensive phrasl embedding in the NP (multiple prepositional phrases as postmodifiers, with levels of embedding) (e.g. The presence of layered structures at the borderline of cell territories)
# The tool generates the raw and normed frequencies of each structures of a text file in a single row of csv. file.
# Multiple texts in the working directory could be iterated.
# pyside6-uic NPCA.ui -o NPCA_gui.py

from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import spacy
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from NPCA_gui_updated import Ui_MainWindow


NOUNISH_POS = {"NOUN", "PROPN", "PRON"}
ADJ_POS = {"ADJ"}
RELATIVIZERS_PAPER = {"that", "who", "which", "whom", "whose"}
RELATIVIZERS_STRICT = {"that"}


def normed(count: int, word_count: int) -> float:
    return round((count / word_count) * 1000, 2) if word_count else 0.0


def sorted_phrase(tokens) -> str:
    unique = sorted({tok.i: tok for tok in tokens}.values(), key=lambda tok: tok.i)
    return " ".join(tok.text for tok in unique).strip()


def append_unique(results: list[str], phrase: str) -> None:
    if phrase and phrase not in results:
        results.append(phrase)

@dataclass
class AnalysisResult:
    file_name: str
    word_count: int
    counts: dict[str, float]


class NPCAnalyzer:
    def __init__(self, model_name: str = "en_core_web_sm", rc_mode: str = "paper") -> None:
        self.model_name = model_name
        self.rc_mode = rc_mode
        self._nlp = None

    @property
    def nlp(self):
        if self._nlp is None:
            self._nlp = spacy.load(self.model_name)
        return self._nlp

    def relativizers(self) -> set[str]:
        return RELATIVIZERS_PAPER if self.rc_mode == "paper" else RELATIVIZERS_STRICT

    def count_words(self, doc) -> int:
        return sum(1 for tok in doc if not tok.is_space and not tok.is_punct)

    def is_noun_head(self, token) -> bool:
        return token.pos_ in NOUNISH_POS

    def is_such_as(self, token) -> bool:
        return (
            token.lemma_.lower() == "as"
            and any(child.lower_ == "such" for child in token.children)
        )

    def count_adj(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue
            for child in head.lefts:
                if child.dep_ == "amod" and child.pos_ in ADJ_POS:
                    results.append(sorted_phrase([child, head]))
        return results

    def count_rc(self, doc) -> list[str]:
        results = []
        relativizers = self.relativizers()

        for head in doc:
            if not self.is_noun_head(head):
                continue

            for child in head.children:
                if child.dep_ != "relcl" or child.i <= head.i:
                    continue

                subtree = list(child.subtree)
                has_relativizer = any(
                    tok.lower_ in relativizers
                    and not (tok.lower_ == "that" and tok.dep_ == "mark")
                    for tok in subtree
                )
                has_complementizer_that = any(
                    tok.lower_ == "that" and tok.dep_ == "mark"
                    for tok in subtree
                )
                has_finite_verb = any(
                    tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VB", "VBG", "VBN"}
                    for tok in subtree
                )

                if has_finite_verb and has_relativizer:
                    append_unique(results, sorted_phrase([head] + subtree))

        return results

    def count_nm(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue
            compounds = [child for child in head.lefts if child.dep_ == "compound" and child.pos_ in {"NOUN", "PROPN"}]
            for compound in compounds:
                results.append(sorted_phrase([compound, head]))
        return results

    # Function detecting contractions (e.g., Mary's the president.)
    def is_contracted_is(self, child, head):
        case_tokens = [
            token for token in child.children
            if token.dep_ == "case" and token.text in {"'s", "’s"}
        ]
        if not case_tokens:
            return False
        apostrophe_s = case_tokens[0]
        return any(
            token.pos_ == "DET"
            for token in apostrophe_s.doc[apostrophe_s.i + 1: head.i]
        )

    def count_poss(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue
            for child in head.lefts:
                if (
                    child.dep_ == "poss"
                    and child.pos_ in {"NOUN", "PROPN"}
                    and not self.is_contracted_is(child, head)
                ):
                    results.append(sorted_phrase(list(child.subtree) + [head]))
        return results

    def count_of(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue
            for child in head.children:
                if child.dep_ == "prep" and child.lemma_.lower() == "of":
                    results.append(sorted_phrase([head] + list(child.subtree)))
        return results

    def count_prep(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue
            for child in head.children:
                if (
                    child.dep_ == "prep"
                    and child.lemma_.lower() != "of"
                    and not self.is_such_as(child)
                ):
                    results.append(sorted_phrase([head] + list(child.subtree)))
        return results

    def count_nonf(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue

            # Normal reduced-relative parse: "students waiting outside".
            for clause in head.children:
                if clause.dep_ not in {"acl", "relcl"}:
                    continue
                if clause.tag_ not in {"VBG", "VBN"}:
                    continue

                subtree = list(clause.subtree)
                has_finite = any(
                    tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VB", "VBG", "VBN"}
                    for tok in subtree
                )
                if not has_finite:
                    append_unique(results, sorted_phrase([head] + subtree))

            # Recovery for occasional en_core_web_sm attachment errors:
            # students -> nsubj -> waiting -> csubj -> are
            participle = head.head
            if head.dep_ not in {"nsubj", "nsubjpass"}:
                continue
            if participle.pos_ != "VERB" or participle.tag_ not in {"VBG", "VBN"}:
                continue
            if participle.dep_ not in {"csubj", "csubjpass"}:
                continue
            if participle.i <= head.i:
                continue

            matrix_predicate = participle.head
            matrix_is_finite = (
                matrix_predicate.pos_ in {"VERB", "AUX"}
                and matrix_predicate.tag_ not in {"VB", "VBG", "VBN"}
            )
            if not matrix_is_finite:
                continue

            subtree = list(participle.subtree)
            subtree_has_finite = any(
                tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VB", "VBG", "VBN"}
                for tok in subtree
            )
            if not subtree_has_finite:
                append_unique(results, sorted_phrase(subtree))

        return results

    def count_adj_nm(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue

            premods = [child for child in head.lefts if child.dep_ in {"amod", "compound"}]
            has_adj = any(child.dep_ == "amod" and child.pos_ in ADJ_POS for child in premods)
            has_noun = any(child.dep_ == "compound" and child.pos_ in {"NOUN", "PROPN"} for child in premods)

            if has_adj and has_noun:
                results.append(sorted_phrase(premods + [head]))

        return results

    def count_comp(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue

            for child in head.children:
                if child.i <= head.i or child.dep_ not in {"acl", "ccomp", "relcl"}:
                    continue

                subtree = list(child.subtree)
                has_that_complement = any(
                    tok.lower_ == "that" and tok.dep_ == "mark" for tok in subtree
                )
                has_finite = any(
                    tok.pos_ in {"VERB", "AUX"} and tok.tag_ not in {"VB", "VBG", "VBN"}
                    for tok in subtree
                )
                has_to_infinitive = (
                    child.tag_ == "VB"
                    or "Inf" in child.morph.get("VerbForm")
                ) and any(
                    tok.lower_ == "to" and tok.dep_ in {"aux", "mark"} for tok in subtree
                )
                has_relativizer = any(tok.lower_ in RELATIVIZERS_PAPER - {"that"} for tok in subtree)

                if (
                    (has_that_complement and has_finite) or has_to_infinitive
                ) and not has_relativizer:
                    append_unique(results, sorted_phrase([head] + subtree))

        return results

    def pp_embedding_depth(self, prep_token) -> int:
        depths = [1]
        for child in prep_token.children:
            if child.dep_ == "pobj":
                nested_preps = [
                    tok
                    for tok in child.children
                    if tok.dep_ == "prep" and not self.is_such_as(tok)
                ]
                if not nested_preps:
                    continue
                for nested in nested_preps:
                    depths.append(1 + self.pp_embedding_depth(nested))
        return max(depths)

    def count_ml(self, doc) -> list[str]:
        results = []
        for head in doc:
            if not self.is_noun_head(head):
                continue

            for prep in [
                child
                for child in head.children
                if child.dep_ == "prep" and not self.is_such_as(child)
            ]:
                if self.pp_embedding_depth(prep) >= 2:
                    results.append(sorted_phrase([head] + list(prep.subtree)))
                    break

        return results

    def analyze_text(self, text: str, file_name: str) -> AnalysisResult:
        doc = self.nlp(text)
        word_count = self.count_words(doc)

        adj = self.count_adj(doc)
        rc = self.count_rc(doc)
        nm = self.count_nm(doc)
        poss = self.count_poss(doc)
        of = self.count_of(doc)
        prep = self.count_prep(doc)
        nonf = self.count_nonf(doc)
        adj_nm = self.count_adj_nm(doc)
        comp = self.count_comp(doc)
        ml = self.count_ml(doc)

        counts = {
            "adj_raw": len(adj),
            "adj_normed": normed(len(adj), word_count),
            "rc_raw": len(rc),
            "rc_normed": normed(len(rc), word_count),
            "nm_raw": len(nm),
            "nm_normed": normed(len(nm), word_count),
            "poss_raw": len(poss),
            "poss_normed": normed(len(poss), word_count),
            "of_raw": len(of),
            "of_normed": normed(len(of), word_count),
            "prep_raw": len(prep),
            "prep_normed": normed(len(prep), word_count),
            "nonf_raw": len(nonf),
            "nonf_normed": normed(len(nonf), word_count),
            "adj_nm_raw": len(adj_nm),
            "adj_nm_normed": normed(len(adj_nm), word_count),
            "comp_raw": len(comp),
            "comp_normed": normed(len(comp), word_count),
            "ml_raw": len(ml),
            "ml_normed": normed(len(ml), word_count),
        }

        return AnalysisResult(file_name=file_name, word_count=word_count, counts=counts)


class NPCInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("What is NPC?")
        self.setMinimumSize(500, 360)

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
            "Index manual\n"
            "adj: Attribute adjective + noun\n"
            "rc: Noun + finite relative clause\n"
            "nm: Noun + noun premodifier\n"
            "poss: Possessive noun + noun\n"
            "of: Noun + of phrase\n"
            "prep: Noun + simple PP (other than of)\n"
            "nonf: Noun + nonfinite relative clause\n"
            "adj_nm: Adjective + noun + noun stacking\n"
            "comp: Noun + complement clause\n"
            "ml: Noun + multiple PP embedding\n\n"
            "Paper-aligned notes used in this version:\n"
            "- Relative clauses include overt relativizers only.\n"
            "- Zero relativizers are excluded.\n"
            "- The default implementation follows the paper's broader operationalization and does not filter animate heads.\n"
        )
        layout.addWidget(self.text_edit)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.analyzer = NPCAnalyzer()
        self.input_folder = ""
        self.output_folder = ""

        self.pushButton_2.clicked.connect(self.set_input_folder)
        self.pushButton.clicked.connect(self.run_process)
        self.pushButton_3.clicked.connect(self.show_npc_info)
        self.pushButton_4.clicked.connect(self.set_output_folder)

        self.pushButton_3.setCursor(Qt.PointingHandCursor)
        self.pushButton_3.setStyleSheet(
            """
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
            """
        )

        self.folder_label = QLabel()
        self.folder_label.setAlignment(Qt.AlignTop)
        self.scrollArea.setWidget(self.folder_label)

    def set_input_folder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if selected_folder:
            self.folder_label.setText(selected_folder)
            self.input_folder = selected_folder

    def set_output_folder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if selected_folder:
            self.output_folder = selected_folder

    def get_all_columns(self) -> list[str]:
        return [
            "adj_raw",
            "adj_normed",
            "rc_raw",
            "rc_normed",
            "nm_raw",
            "nm_normed",
            "poss_raw",
            "poss_normed",
            "of_raw",
            "of_normed",
            "prep_raw",
            "prep_normed",
            "nonf_raw",
            "nonf_normed",
            "adj_nm_raw",
            "adj_nm_normed",
            "comp_raw",
            "comp_normed",
            "ml_raw",
            "ml_normed",
        ]

    def get_selected_columns(self) -> list[str]:
        selected = []
        freq_raw = self.checkBox.isChecked()
        freq_normed = self.checkBox_2.isChecked()

        if self.checkBox_3.isChecked():
            if freq_raw:
                selected.append("adj_raw")
            if freq_normed:
                selected.append("adj_normed")

        if self.checkBox_4.isChecked():
            for prefix in ["rc", "nm", "poss", "of", "prep"]:
                if freq_raw:
                    selected.append(f"{prefix}_raw")
                if freq_normed:
                    selected.append(f"{prefix}_normed")

        if self.checkBox_5.isChecked():
            for prefix in ["nonf", "adj_nm"]:
                if freq_raw:
                    selected.append(f"{prefix}_raw")
                if freq_normed:
                    selected.append(f"{prefix}_normed")

        if self.checkBox_6.isChecked():
            for prefix in ["comp", "ml"]:
                if freq_raw:
                    selected.append(f"{prefix}_raw")
                if freq_normed:
                    selected.append(f"{prefix}_normed")

        order = self.get_all_columns()
        return [column for column in order if column in set(selected)]

    def iter_text_files(self) -> list[Path]:
        input_path = Path(self.input_folder)
        return sorted(path for path in input_path.glob("*.txt") if path.is_file())

    def output_csv_path(self) -> Path:
        raw_name = self.textEdit.toPlainText().strip() or "npc_results"
        safe_name = "".join(char for char in raw_name if char not in '\\/:*?"<>|').strip() or "npc_results"
        return Path(self.output_folder) / f"{safe_name}.csv"

    def run_process(self):
        if not self.input_folder:
            QMessageBox.warning(self, "Warning", 'Please select an input folder using the "Find Folder" button.')
            return

        if not self.output_folder:
            QMessageBox.warning(self, "Warning", 'Please select an output folder using the "Find Folder" button.')
            return

        selected_columns = self.get_selected_columns()
        if not selected_columns:
            QMessageBox.warning(self, "Warning", "Please select at least one feature and one frequency type.")
            return

        file_list = self.iter_text_files()
        if not file_list:
            QMessageBox.warning(self, "Warning", "No .txt files were found in the selected input folder.")
            return

        try:
            _ = self.analyzer.nlp
        except OSError as exc:
            QMessageBox.critical(
                self,
                "spaCy Model Error",
                "The spaCy English model 'en_core_web_sm' is not installed.\n\n"
                "Install it with:\npython -m spacy download en_core_web_sm\n\n"
                f"Details: {exc}",
            )
            return

        output_file_path = self.output_csv_path()

        self.pushButton.setText("Processing...")
        self.pushButton.setEnabled(False)
        self.progressBar.setValue(0)
        QApplication.processEvents()

        try:
            with output_file_path.open("w", newline="", encoding="utf-8") as out_file:
                writer = csv.writer(out_file)
                writer.writerow(["file", "Number of words", *selected_columns])

                total_files = len(file_list)
                for index, file_path in enumerate(file_list, start=1):
                    text = file_path.read_text(encoding="utf-8", errors="ignore")
                    result = self.analyzer.analyze_text(text, file_path.name)

                    row = [result.file_name, result.word_count]
                    row.extend(result.counts.get(column, 0) for column in selected_columns)
                    writer.writerow(row)

                    progress = int(index / total_files * 100)
                    self.progressBar.setValue(progress)
                    QApplication.processEvents()

            self.progressBar.setValue(100)
            QMessageBox.information(self, "Success", f'CSV file "{output_file_path}" generated successfully.')

            if self.checkBox_7.isChecked():
                self.plot_bar_graph(output_file_path, selected_columns)

        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Error generating CSV file:\n{exc}")

        self.pushButton.setText("Start the analysis")
        self.pushButton.setEnabled(True)

    def show_npc_info(self):
        dialog = NPCInfoDialog(self)
        dialog.exec()

    def plot_bar_graph(
            self,
            csv_path: Path,
            selected_columns: list[str]
    ):
        try:
            csv_path = Path(csv_path).resolve()

            if not csv_path.exists():
                QMessageBox.warning(
                    self,
                    "Warning",
                    f"Output CSV file not found:\n{csv_path}"
                )
                return

            df = pd.read_csv(csv_path)

            normed_cols = [
                column
                for column in selected_columns
                if column.endswith("_normed")
                   and column in df.columns
            ]

            if not normed_cols:
                QMessageBox.information(
                    self,
                    "Info",
                    "The graph requires normalized frequencies. "
                    "Select normalized frequency and run again."
                )
                return

            mean_values = (
                df[normed_cols]
                .apply(pd.to_numeric, errors="coerce")
                .mean()
                .dropna()
                .sort_values(ascending=False)
            )

            if mean_values.empty:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "No numeric normalized-frequency data were found."
                )
                return

            figure, axis = plt.subplots(figsize=(10, 6))

            mean_values.plot(
                kind="bar",
                ax=axis,
                color="#52789c",
                edgecolor="#263849"
            )

            axis.set_ylabel(
                "Mean Normalized Frequency per 1,000 words"
            )
            axis.set_xlabel("Noun Phrase Feature")
            axis.set_title(
                "Mean Normalized Frequencies of "
                "Selected NP Structures"
            )
            axis.grid(
                axis="y",
                linestyle="--",
                linewidth=0.5,
                alpha=0.7
            )

            axis.tick_params(axis="x", labelrotation=45)

            for label in axis.get_xticklabels():
                label.set_horizontalalignment("right")

            figure.tight_layout()

            # Derive the PNG path directly from the actual CSV path.

            plot_path = csv_path.with_name(
                f"{csv_path.stem}_NPC_plot.png"
            )

            figure.savefig(
                plot_path,
                dpi=300,
                format="png",
                bbox_inches="tight"
            )

            plt.close(figure)

            if not plot_path.exists():
                raise RuntimeError(
                    f"The PNG could not be created at:\n{plot_path}"
                )

            QMessageBox.information(
                self,
                "Success",
                "Analysis and graph completed.\n\n"
                f"CSV:\n{csv_path}\n\n"
                f"PNG:\n{plot_path}"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Plot Error",
                f"Error while generating the PNG:\n{error}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
