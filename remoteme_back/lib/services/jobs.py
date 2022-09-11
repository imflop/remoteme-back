import logging
import typing as t
import dataclasses as dc

from loguru._logger import Logger

from ..dal.jobs import JobRepository
from ..dal.models.jobs import AdvertModel, AdvertShort, TagModel

logger = logging.getLogger(__name__)


@dc.dataclass(repr=False)
class JobService:
    job_repository: JobRepository
    logger: Logger = dc.field(default=logger)

    async def get_adverts_short(self, limit: int, offset: int, tags: t.Sequence[str] = None) -> t.Sequence[AdvertShort]:
        adverts = await self.get_adverts(limit, offset, tags)

        return [AdvertShort.build(advert) for advert in adverts]

    async def get_adverts(self, limit: int, offset: int, tags: t.Sequence[str] = None) -> t.Sequence[AdvertModel]:
        return await self.job_repository.get_adverts(limit, offset, tags)

    async def get_advert(self, advert_id: int) -> AdvertModel | None:
        self.logger.info(f"Get advert: {advert_id}")
        return await self.job_repository.get_advert_or_none(advert_id)

    async def get_tags(self) -> t.Sequence[TagModel]:
        return await self.job_repository.get_tags()
