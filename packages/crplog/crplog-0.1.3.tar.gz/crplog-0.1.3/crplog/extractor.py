import pandas as pd
import os
from datetime import datetime


class PersonalLogFiles:
    TODAY = datetime.today().date()

    def __init__(self, path):
        self.file_list = list(
            map(
                lambda xcl: os.path.join(path, xcl),
                filter(
                    lambda file: os.path.splitext(file)[-1].lower() in [".xlsm", ".xlsx"],
                    os.listdir(path),
                ),
            )
        )
        self.frame = pd.DataFrame()
        self.frames = []
        self.path = path
        self.permission = []
        self.badlogs = []

    def extract_data(self):
        for file in self.file_list:
            try:
                read = pd.read_excel(file, sheet_name=0, header=None).dropna(how="all")
                read = read.rename(columns=read.iloc[0]).drop(read.index[0])
                self.frames.append(read)
            except PermissionError:
                self.permission.append(os.path.split(file)[-1].split("_")[0])

    def save(self):
        extracted_path = os.path.join(self.path, "Extracted")
        if not os.path.isdir(extracted_path):
            os.mkdir(extracted_path)
        archive_path = os.path.join(extracted_path, "Archive")
        if not os.path.isdir(archive_path):
            os.mkdir(archive_path)
        try:
            out = pd.concat(self.frames)
        except ValueError:
            try:
                try:
                    self.badlogs = list(
                        max(y["Owner"])
                        for y in filter(
                            lambda x: x.columns.size != x.columns.dropna().size,
                            self.frames,
                        )
                    )
                except Exception:
                    pass
                self.frames = [
                    frames[frames.columns.dropna()] for frames in self.frames
                ]
                out = pd.concat(self.frames)
            except ValueError:
                shortest = min(x.columns.size for x in self.frames)
                try:
                    self.badlogs = list(
                        max(y["Owner"])
                        for y in filter(
                            lambda x: x.columns.size != x.columns.shortest.size,
                            self.frames,
                        )
                    )
                except Exception:
                    pass
                self.frames = [
                    frame[frame.columns[0:shortest]] for frame in self.frames
                ]
                out = pd.concat(self.frames)
        out.to_csv(os.path.join(extracted_path, f"Extracted Log Files.csv"))
        out.to_csv(os.path.join(archive_path, f"Extracted Log Files_{self.TODAY}.csv"))
