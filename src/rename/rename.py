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
    if is_final_stem(stem):
        print_warning(f"Stem is already in the expected form. Skipping: {stem}")
        return None
    image = get_image_from_path(path=path)
    if image is None:
        return
    exif_date = extract_exif_date_from_image(image=image, path=path)
    if exif_date is None:
        return
    new_path = make_new_path(exif_date=exif_date, old_path=path)
    # rename(exif_date=exif_date, old_path=path, new_path=new_path)


################################################################################

# Doc de la méthode rename: https://docs.python.org/3/library/pathlib.html#pathlib.Path.rename


@typechecked
def rename(*, exif_date: str, old_path: Path, new_path: Path):
    new_path = make_new_path(exif_date=exif_date, old_path=old_path)
    if new_path.exists():
        print_warning(f"Target path already exists. Skipping: {new_path}")
        return
    print(f"{old_path} ==> {new_path}")
    old_path.rename(new_path)


@typechecked
def make_new_path(*, exif_date: str, old_path: Path) -> Path:
    new_date = make_formatted_date(exif_date=exif_date, path=old_path)
    ##
    old_stem = old_path.stem
    new_stem = f"{new_date}_{old_stem}"
    assert is_final_stem(new_stem), new_stem
    ##
    new_path = old_path.with_stem(new_stem)
    return new_path


################################################################################

# Doc du module exif: https://pypi.org/project/exif/


@typechecked
def get_image_from_path(*, path: Path) -> Optional[exif.Image]:
    stem = path.stem
    ##
    with open(path, "rb") as cin:
        try:
            image = exif.Image(cin)
        except:
            print_warning(f"EXIF could not extract image. Skipping: {path}")
            return None
    return image


@typechecked
def extract_exif_date_from_image(*, image: exif.Image, path: Path) -> Optional[str]:
    stem = path.stem
    if not image.has_exif:
        print_warning(f"No EXIF data found in stem. Skipping: {stem}")
        return None
    ##
    exif_data_list = tuple(image.list_all())
    if "datetime" not in exif_data_list:
        possible_data = tuple(s for s in exif_data_list if "date" in s)
        print_warning(
            f"This stem has EXIF data, but no date-like data. Skipping: {stem}"
        )
        if len(possible_data) > 0:
            print_warning(
                "For information, possible date-like EXIF data: {possible_data}"
            )
        return None
    date = image.datetime
    return date


################################################################################

# Utilitaires


def make_formatted_date(*, exif_date: str, path: Path) -> str:
    m = re.fullmatch(EXIF_DATE_PATTERN, exif_date)
    assert m is not None, path
    (year, month, day, hour, minute, second) = m.groups()
    formatted_date = f"{year}-{month}-{day}-{hour}-{minute}-{second}"
    return formatted_date


def is_final_stem(stem: str) -> Optional[re.Match]:
    m = re.fullmatch(FINAL_STEM_PATTERN, stem, flags=re.IGNORECASE)
    return m


def print_warning(message: str):
    print(f"\t\tWarning: {message}")


main()
