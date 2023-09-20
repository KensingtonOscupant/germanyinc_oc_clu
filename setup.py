import cx_Freeze
import os

executables = [cx_Freeze.Executable("script.py")]

cx_Freeze.setup(
    name="germanyinc_shareholders_utility",
    options={"build_exe": {"packages":["csv","sys","msvcrt","os"], "include_files":[(os.path.abspath('df_cleaned.csv'), 'df_cleaned.csv')]}},
    version="1.0",
    description="This app allows us to distinguish between natural and legal persons and in the latter case match companies to their OpenCorporates Profile. Press 'a' if notifying_party is a natural person, 'd' if it is a legal person and then enter the OpenCorporates URL by pasting it into the field and pressing Enter. If none can be found, just leave blank and press enter. Press 'b' to go back to the previous question and 'q' to quit the utility.",
    executables=executables
)