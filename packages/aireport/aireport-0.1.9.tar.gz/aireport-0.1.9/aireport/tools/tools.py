import glob
import os
from datetime import datetime
import re
import pandas as pd


class Lims:
    TODAY = datetime.today().date()

    def __init__(self, root):
        self.root = root
        self.directories = [
            os.path.join(root, directory)
            for directory in (
                filter(lambda x: os.path.isdir(os.path.join(root, x)), os.listdir(root))
            )
        ]
        self.lims_out = None
        self.ftir_out = None
        self.eds = pd.DataFrame()
        self.techniques = {"Name", "FTIR", "SEM", "EDS", "OptDigMicr", "mFTIR", "TG"}
        self.frame = self.base_frame()

    def compile(self):
        self.lims()
        self.reshape_spectral_csv()
        self.write_ftir()
        self.write_lims()
        self.write_eds()

    def write_ftir(self):
        ftir_out = self.frame.Name.apply(
            lambda x: f"{self.TODAY.strftime('%Y%m%d')}_{x}"
        )
        ftir_out.to_csv(self.root + "\\ftir.csv", sep=",", header=False, index=False)

    def write_lims(self):
        f = self.frame.copy()
        f.Name = f.Name.apply(lambda x: x.replace("_", " "))
        f.to_csv(self.root + "\\lims.csv", sep=",")

    def write_eds(self):
        self.eds.to_csv(self.root + "\\cleaned_eds.csv", sep=",")

    def base_frame(self):
        return pd.DataFrame(columns=self.techniques)

    def lims(self):
        for path in self.directories:
            for file in os.listdir(path):
                try:
                    date, lims, name = os.path.splitext(file)[0].split("_")
                    name = f"{lims}_{name}"
                except ValueError or IndexError as e:
                    continue
                if tech := list(
                    filter(lambda x: re.search(x, path), self.techniques - set("EDS"))
                ):
                    tech = tech[0]
                else:
                    continue
                if lims not in self.frame.index:
                    self.frame.loc[lims, "Name"] = name
                else:
                    self.frame.loc[lims].Name = [self.frame.loc[lims].Name, name][
                        len(self.frame.loc[lims].Name) < len(name)
                    ]
                self.frame.loc[lims, tech] = "x"
        self.frame.dropna(axis=1, how="all", inplace=True)
        ordered_tech = ["Name", "OptDigMicr", "FTIR", "SEM", "EDS"]
        for tech in ordered_tech:
            if tech not in self.frame:
                self.frame[tech] = ""
        self.frame = self.frame[ordered_tech]

    def reshape_spectral_csv(self):
        elemental_dictionary = {
            "Ni": "Nickel (%)",
            "Si": "Silicon (%)",
            "Mg": "Magnesium (%)",
            "Al": "Aluminum (%)",
            "K": "Potassium (%)",
            "Ca": "Calcium (%)",
            "Cu": "Copper (%)",
            "Zr": "Zirconium (%)",
            "Mo": "Molybdenum (%)",
            "Ag": "Silver (%)",
            "Au": "Gold (%)",
            "Sn": "Tin (%)",
            "W": "Tungsten (%)",
            "Cr": "Chromium (%)",
            "Fe": "Iron (%)",
            "S": "Sulfur (%)",
            "Cl": "Chlorine (%)",
            "Zn": "Zinc (%)",
            "P": "Phosphor (%)",
            "Pb": "Lead (%)",
            "Ne": "Neon (%)",
            "Ti": "Titanium(%)",
            "Mn": "Manganese (%)",
        }

        for p in self.directories:
            if re.search("SEM", p) or re.search("EDS", p):
                try:
                    spectra = glob.glob(p + "\\*.csv")
                    eds_frame = pd.read_csv(spectra[0], skiprows=2, index_col="Name")
                    eds_frame.rename(columns=elemental_dictionary, inplace=True)
                    hold = []
                    for i in eds_frame.values:
                        temp_hold = []
                        for index, value, in enumerate(i):
                            value = str(value)
                            if value not in " ":
                                temp_hold.append(
                                    "{} {}".format(value, eds_frame.columns[index])
                                )
                        hold.append(temp_hold)
                    e = eds_frame.reset_index()
                    self.eds = pd.DataFrame(
                        data=hold,
                        index=e["Name"].apply(
                            lambda x: " ".join(
                                "_".join(x.split("_")[::-1]).split("_")[:-1]
                            )
                        ),
                    )
                    for entry in list(e.Name):
                        lims = entry.split("_")[1]
                        self.frame.loc[lims, "EDS"] = "x"
                except Exception as e:
                    pass
