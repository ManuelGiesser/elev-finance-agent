from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.match_repository import MatchRepository
from app.schemas.match import MatchResponse

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.get(
    "",
    response_model=list[MatchResponse],
)
def list_matches(
    db: Session = Depends(get_db),
):
    return MatchRepository(db).list()