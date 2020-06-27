
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget, QApplication
from pandas import DataFrame as pddf
from pandas import read_csv
from matplotlib.pyplot import subplots
from glob import glob
import re
from os import chdir

import sys

from rex_ui import Ui_Form  # pyuic5 generated code

# sys.setrecursionlimit(20000)


class MainWindows(QWidget, Ui_Form):
    """
    a class of my main window
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.btn_browse.clicked.connect(self.select_folder)
        self.btn_clear.clicked.connect(self.clear_txt)
        self.btn_run.clicked.connect(self.run)
        self.btn_exit.clicked.connect(sys.exit)
        self.show()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory()
        self.lineEdit.setText(folder)

    def clear_txt(self):
        self.lineEdit.setText("")

    def run(self):
        folder = self.lineEdit.text()
        df = pddf(columns=["residue_number", "residue", "Rex"])
        i = 0
        try:
            chdir(folder)

            file_list = glob("*.cpmg")   # get a list of *.cpmg files
            for file in file_list:
                with open(file):
                    name = file[0]
                    # grab unumber from file name as residue no.
                    residue_no = int(re.findall(r"\d+", file)[0])
                    # columns separated by one or more spaces
                    data = read_csv(file, header=0, sep=r"\s+")
                    max_index = data["#nu_cpmg(Hz)"].idxmax()  # index of maximum frequency
                    min_index = data["#nu_cpmg(Hz)"].idxmin()
                    R2_max_f = data.loc[max_index]["R2(1/s)"]  # R2 of maximum frequency
                    R2_min_f = data.loc[min_index]["R2(1/s)"]
                    Rex = R2_min_f - R2_max_f
                    df.loc[i] = [residue_no, name, Rex]
                    i += 1

            df = df.sort_values("residue_number")
            filt = (df["residue_number"] < 1000)

            fig, ax = subplots()
            df.loc[filt].plot(x="residue_number", y="Rex", legend=False, ax=ax)
            ax.set_xlabel("residue number")
            ax.set_ylabel("Rex")
            fig.tight_layout()
            fig.show()
            # how to show plot in label?
            # plt.savefig("Rex.png")
        except OSError:
            self.lineEdit.setText("Please input correct path")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindows()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
