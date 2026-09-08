"""FastAPI backend: name -> 2D structure image."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response

from core import NameParseError, StructureRenderError, name_to_image_bytes

app = FastAPI(title="Name to Structure API")


@app.get("/structure")
def get_structure(
    name: str = Query(..., min_length=1, description="Chemical name (IUPAC preferred)"),
    width: int = Query(400, ge=50, le=2000),
    height: int = Query(400, ge=50, le=2000),
):
    """Return a PNG image of the 2D structure for the given chemical name."""
    try:
        png_bytes = name_to_image_bytes(name, size=(width, height))
    except NameParseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StructureRenderError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return Response(content=png_bytes, media_type="image/png")


@app.get("/health")
def health():
    return {"status": "ok"}
