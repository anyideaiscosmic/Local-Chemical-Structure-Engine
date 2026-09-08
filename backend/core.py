"""Core pipeline: chemical name -> 2D structure image.

Stage 1: name -> SMILES (OPSIN, via py2opsin)
Stage 2: SMILES -> 2D image (RDKit)
"""

from io import BytesIO

from py2opsin import py2opsin
from rdkit import Chem
from rdkit.Chem import Draw


class NameParseError(Exception):
    """Raised when OPSIN cannot parse the given name."""


class StructureRenderError(Exception):
    """Raised when RDKit cannot build/render a molecule from the SMILES."""


def name_to_smiles(name: str) -> str:
    """Stage 1: parse a chemical name into a SMILES string via OPSIN."""
    name = name.strip()
    if not name:
        raise NameParseError("Empty name provided.")

    smiles = py2opsin(name, output_format="SMILES")

    if not smiles:
        raise NameParseError(
            f"OPSIN could not parse '{name}'. "
            "It may be a trivial/trade name rather than a systematic IUPAC name."
        )
    return smiles


def smiles_to_image_bytes(smiles: str, size: tuple[int, int] = (400, 400)) -> bytes:
    """Stage 2: render a SMILES string as a PNG image, returned as raw bytes."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise StructureRenderError(f"RDKit could not parse SMILES '{smiles}'.")

    img = Draw.MolToImage(mol, size=size)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def name_to_image_bytes(name: str, size: tuple[int, int] = (400, 400)) -> bytes:
    """Full pipeline: name -> SMILES -> PNG bytes."""
    smiles = name_to_smiles(name)
    return smiles_to_image_bytes(smiles, size=size)


if __name__ == "__main__":
    # Quick manual check across systematic, trivial, and invalid names.
    test_names = [
        "4-hydroxybenzoic acid",
        "ethanol",
        "aspirin",             # expected to fail: trivial name
        "not a real chemical", # expected to fail: garbage input
    ]
    for n in test_names:
        try:
            data = name_to_image_bytes(n)
            print(f"OK   : {n!r} -> {len(data)} bytes PNG")
        except (NameParseError, StructureRenderError) as e:
            print(f"FAIL : {n!r} -> {e}")
