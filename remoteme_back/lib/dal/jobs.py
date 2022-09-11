import dataclasses as dc
import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, contains_eager, selectinload
from sqlalchemy.sql.expression import null, not_, true, and_

from .models.jobs import AdvertModel, TagModel, TagToAdvertModel


@dc.dataclass(repr=False)
class JobRepository:
    db: AsyncSession

    async def get_adverts(self, limit: int, offset: int = 0, tags: t.Sequence[str] = None) -> t.Sequence[AdvertModel]:
        # TODO: add filters (!!!)
        q = (
            select(AdvertModel)
            # .join(TagToAdvertModel)
            # .join(TagModel)
            .options(joinedload(AdvertModel.tags))
            .options(joinedload(AdvertModel.user))
            .where(AdvertModel.is_moderate == true())
            .limit(limit)
            .offset(offset)
            .order_by(AdvertModel.created_at)
        )

        if tags:
            q.where(TagModel.slug_name.in_(tags))

        result = await self.db.execute(q)
        rows = result.unique()

        return [row[AdvertModel] for row in rows]

    async def get_advert_or_none(self, advert_id: int) -> t.Optional[AdvertModel]:
        q = (
            select(AdvertModel)
            .options(joinedload(AdvertModel.tags))
            .options(joinedload(AdvertModel.user))
            .where(AdvertModel.id == advert_id)
        )
        result = await self.db.execute(q)
        row = result.first()

        return row[AdvertModel] if row else None

    async def get_tags(self) -> t.Sequence[TagModel]:
        result = await self.db.execute(
            select(TagModel)
        )
        rows = result.all()

        return [row[TagModel] for row in rows]
