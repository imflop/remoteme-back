import typing as t
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    Query,
)

from ...lib.factories.services import job_service_factory
from ...lib.serializers.jobs import (
    PaginatedAdvert, Advert, DetailedAdvert, Tag
)
from ...lib.services.jobs import JobService

router = APIRouter()


@router.get("/adverts", response_model=PaginatedAdvert)
async def get_adverts(
    limit: int = 10,
    offset: int = 0,
    tags: t.Optional[t.Sequence[str]] = Query(None),
    job_service: JobService = Depends(job_service_factory)
) -> PaginatedAdvert:
    if tags:
        adverts = await job_service.get_adverts_short(limit, offset, tags)
    else:
        adverts = await job_service.get_adverts_short(limit, offset)

    return PaginatedAdvert(
        limit=limit,
        offset=offset,
        count=len(adverts),
        result=[Advert.from_orm(advert) for advert in adverts]
    )


@router.get("/adverts/{advert_id}", response_model=DetailedAdvert)
async def get_advert(
    advert_id: int, job_service: JobService = Depends(job_service_factory)
) -> DetailedAdvert | Response:
    if advert := await job_service.get_advert(advert_id):
        return DetailedAdvert.from_orm(advert)

    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Not Found")


@router.get("/tags")
async def get_tags(job_service: JobService = Depends(job_service_factory)) -> t.Sequence[Tag]:
    tags = await job_service.get_tags()

    return [Tag.from_orm(tag) for tag in tags]
