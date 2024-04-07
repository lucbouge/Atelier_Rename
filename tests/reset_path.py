from pathlib import Path, PurePath
import re
from typing import Optional

# Pour l'importation des modules, voir https://docs.python.org/3/installing/index.html

import exif
from typeguard import typechecked

ROOT = Path(
    "/",
    "Users",
    "bouge",
    "share",
    "Projets",
    "Atelier_numerique_Cleunay",
    "Rename",
    "Sources",
    "Test",
)

ROOT = Path(
    "/",
    "Users",
    "bouge",
    "share",
    "Personnel",
    "Personnes",
    "Mado",
    "Photos",
    "2024-04-06_Juliette",
)
# À remplacer par le chemin de la racine de tes dossiers photos

FINAL_STEM_PATTERN = r"(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})_([\w-]+)"
EXIF_DATE_PATTERN = r"(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})"

################################################################################


# Doc de la méthode walk: https:", "/docs.python.org/3/library/pathlib.html#pathlib.Path.walk


def main():
    assert ROOT.exists(), ROOT
    print(f"{ROOT = }")
    for dirpath, dirnames, filenames in ROOT.walk():
        for filename in filenames:
            path = dirpath / filename
            suffix = path.suffix.lower()
            if suffix not in (".jpeg", ".jpg"):
                continue
            process_path(path=path)


################################################################################


@typechecked
def process_path(*, path: Path):
    stem = path.stem
    if m := re.fullmatch(FINAL_STEM_PATTERN, stem, flags=re.IGNORECASE):
        new_stem = m.groups()[-1]
        new_path = path.with_stem(new_stem)
        print(f"Moving {path.stem} => {new_path.stem}")
        assert not new_path.exists(), new_path
        path.rename(new_path)


main()
