from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.routes.auth import get_current_user  # Correct import here
from app.models.user import User
import pandas as pd
import io

router = APIRouter(prefix="/upload", tags=["uploads"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV or Excel files are allowed"
        )

    contents = await file.read()
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse file: {e}"
        )

    from app.models.upload import Upload  # your Upload model

    new_upload = Upload(user_id=current_user.id, filename=file.filename)
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)

    return {
        "filename": file.filename,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "preview": df.head(5).to_dict(orient="records"),
        "upload_id": new_upload.id
    }
