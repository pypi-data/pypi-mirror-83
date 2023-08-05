#!/usr/bin/env python3

import sys
from pieoffice_gui.docs import *
from pieoffice.pie import alpha_to_pie
from PySide2 import QtWidgets, QtCore, QtGui

supLanguages = ["PIE", "Polytonic Greek", "Linear B", "Cypriot Syllabary", "Armenian",
                "Old Persian", "Avestan (Script)", "Avestan (Transliteration)",
                "Vedic/Sanskrit HK > Devanagari", "Vedic/Sanskrit HK > IAST",
                "Hieroglyphic Luwian", "Lycian", "Lydian", "Carian", "Gothic",
                "Oscan", "Ogham"]

class About(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.monofontmini = QtGui.QFont("Noto Mono", 10)

        self.text = QtWidgets.QLabel("""PIE Office\n\n\nConverter application for (Proto-)Indo-European languages' scripts.\n\n\nv. 0.0.3 (beta)\n\n\n2020 Caio Geraldes (@silenus32)\n\nLicense: MIT""")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setFont(self.monofontmini)

        self.button = QtWidgets.QPushButton("Close")
        self.button.clicked.connect(self.closer)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def closer(self):
        self.close()


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.about = About()

        self.converter = alpha_to_pie
        self.doc = doc_pie

        self.monofont = QtGui.QFont("Noto Mono", 14)
        self.monofontmini = QtGui.QFont("Noto Mono", 10)
        self.sansfont = QtGui.QFont("Noto Sans", 14)

        self.toolbar = QtWidgets.QMenuBar()
        self.toolbar.addAction("About", self.abouted)
        self.toolbar.setFont(self.monofontmini)

        self.button = QtWidgets.QPushButton("Rules")
        self.title = QtWidgets.QLabel("PIE Office")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(self.monofont)

        self.langSelector = QtWidgets.QComboBox(placeholderText="PIE")
        self.langSelector.insertItems(0, supLanguages)

        self.entry = QtWidgets.QTextEdit()
        self.entry.setAcceptRichText(True)
        self.entry.setFont(self.monofont)
        self.entry.setFontPointSize(14)
        self.entry.setPlaceholderText("Text to convert")
        self.out = QtWidgets.QTextEdit()
        self.out.setFont(self.sansfont)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.langSelector)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.out)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.rules)

        self.langSelector.activated.connect(self.selectLanguage)

        self.entry.textChanged.connect(self.convert)

    def rules(self):
        self.out.setText(self.doc)

    def selectLanguage(self):
        if self.langSelector.currentText() == "Polytonic Greek":
            # self.entry.setPlaceholderText("Polytonic Greek text to convert")
            from pieoffice.greek import alpha_to_greek
            self.converter = alpha_to_greek
            self.doc = doc_polygreek

        elif self.langSelector.currentText() == "Linear B":
            from pieoffice.linearb import alpha_to_linearb
            self.converter = alpha_to_linearb
            self.doc = doc_linarb

        elif self.langSelector.currentText() == "Cypriot Syllabary":
            from pieoffice.cypriot import alpha_to_cypriot
            self.converter = alpha_to_cypriot
            self.doc = doc_cypriot

        elif self.langSelector.currentText() == "Oscan":
            # self.entry.setPlaceholderText("Oscan text to convert")
            from pieoffice.oscan import alpha_to_oscan
            self.converter = alpha_to_oscan
            self.doc = doc_oscan

        elif self.langSelector.currentText() == "Hieroglyphic Luwian":
            from pieoffice.luwian import alpha_to_luwian
            self.converter = alpha_to_luwian
            self.doc = doc_luwian

        elif self.langSelector.currentText() == "Lycian":
            from pieoffice.lycian import alpha_to_lycian
            self.converter = alpha_to_lycian
            self.doc = doc_lycian

        elif self.langSelector.currentText() == "Lydian":
            from pieoffice.lydian import alpha_to_lydian
            self.converter = alpha_to_lydian
            self.doc = doc_lydian

        elif self.langSelector.currentText() == "Carian":
            from pieoffice.carian import alpha_to_carian
            self.converter = alpha_to_carian
            self.doc = doc_carian

        elif self.langSelector.currentText() == "Armenian":
            from pieoffice.armenian import alpha_to_armenian
            self.converter = alpha_to_armenian
            self.doc = doc_armenian

        elif self.langSelector.currentText() == "Gothic":
            from pieoffice.gothic import alpha_to_gothic
            self.converter = alpha_to_gothic
            self.doc = doc_gothic

        elif self.langSelector.currentText() == "Avestan (Script)":
            from pieoffice.avestan import alpha_to_avestan
            self.converter = alpha_to_avestan
            self.doc = doc_avestan

        elif self.langSelector.currentText() == "Avestan (Transliteration)":
            from pieoffice.avestan import alpha_to_avestan_trans
            self.converter = alpha_to_avestan_trans
            self.doc = doc_avestan

        elif self.langSelector.currentText() == "Old Persian":
            from pieoffice.oldpersian import alpha_to_oldpersian
            self.converter = alpha_to_oldpersian
            self.doc = doc_oldpersian

        elif self.langSelector.currentText() == "Vedic/Sanskrit HK > Devanagari":
            from pieoffice.vedic import hk_to_deva
            self.converter = hk_to_deva
            self.doc = doc_ved

        elif self.langSelector.currentText() == "Vedic/Sanskrit HK > IAST":
            from pieoffice.vedic import hk_to_iast
            self.converter = hk_to_iast
            self.doc = doc_ved

        elif self.langSelector.currentText() == "Ogham":
            from pieoffice.ogham import alpha_to_ogham
            self.converter = alpha_to_ogham
            self.doc = doc_ogham

        elif self.langSelector.currentText() == "PIE":
            from pieoffice.pie import alpha_to_pie
            self.converter = alpha_to_pie
            self.doc = doc_pie

        self.out.setFontPointSize(14)
        self.entry.setFontPointSize(14)

        # if self.langSelector.currentText() == "<++>":
            # from pieoffice.<++> import alpha_to_<++>
            # self.converter = alpha_to_<++>

    def convert(self):
        self.out.setText(self.converter(self.entry.toPlainText()))
        self.out.setFontPointSize(14)
        self.entry.setFontPointSize(14)

    def abouted(self):
        self.about.show()

def main():
    app = QtWidgets.QApplication([])

    widget = Main()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

