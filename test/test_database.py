from sqlalchemy import select, insert, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
import src.models as models
import src.schema as schema


async def post_group(number: str, session: AsyncSession = get_async_session):
    print(1)
    group = schema.GroupStudents(number=number)
    print(2)
    stmt = insert(models.GroupStudents).values(**group.dict())
    print(3)
    await session.execute(stmt)
    print(4)
    await session.commit()
    print(5)

post_group(number="211-251")
