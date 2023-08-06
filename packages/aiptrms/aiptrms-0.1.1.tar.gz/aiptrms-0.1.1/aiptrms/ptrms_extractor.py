import os
import pandas as pd
from pandas.errors import EmptyDataError


class Ptrms:
    def __init__(self, file, ref_start, ref_end, sample_start, sample_end):
        self.file = file
        self.ref_start = ref_start
        self.ref_end = ref_end
        self.sample_start = sample_start
        self.sample_end = sample_end
        self.frame = pd.DataFrame

    def run(self):
        self.load()
        self.extract_windows()

    def load(self):
        try:
            self.frame = pd.read_csv(self.file, sep="\t")
        except pd.errors.EmptyDataError:
            self.file.seek(0)
            self.load()
        self.frame.index = self.frame["Cycle"].apply(lambda x: int(x))
        self.frame.drop(columns=["AbsTime", "RelTime"], errors="ignore", inplace=True)

    def extract_windows(self):
        ref_window = self.frame.loc[int(self.ref_start) - 1 : int(self.ref_end)]
        ref_window_stats = ref_window.drop(
            columns=["Cycle"], errors="ignore"
        ).describe()
        sample_window = self.frame.loc[
            int(self.sample_start) - 1 : int(self.sample_end)
        ]
        sample_window_stats = sample_window.drop(
            columns=["Cycle"], errors="ignore"
        ).describe()
        ref_window_frame = (
            pd.DataFrame(ref_window.max(axis=0))
            .transpose()
            .drop(columns=["Cycle"], errors="ignore")
        )
        sample_window_frame = (
            pd.DataFrame(sample_window.max(axis=0))
            .transpose()
            .drop(columns=["Cycle"], errors="ignore")
        )
        dif_frame = sample_window_frame.sub(ref_window_frame)
        sample_window_frame.index = ["Sample Window (Max)"]
        ref_window_frame.index = ["Reference Window (Max)"]
        dif_frame.index = ["Difference (Max)"]
        dif_frame = dif_frame.transpose()
        dif_stats = sample_window_stats.transpose().sub(ref_window_stats.transpose())
        sample_window_frame = sample_window_frame.transpose()
        ref_window_frame = ref_window_frame.transpose()
        out = pd.concat(
            [dif_frame, dif_stats, ref_window_frame, sample_window_frame], axis=1
        )
        out_path = os.path.join(
            os.path.dirname(self.file.name), "extracted_window.xlsx"
        )
        out.to_excel(out_path)
