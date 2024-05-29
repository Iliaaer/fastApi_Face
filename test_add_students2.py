from sqlalchemy import select, insert, desc
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from src.database import get_async_session
import src.models as models
import src.schema as schema
from src.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session



'''
Казаков Даниил Сергеевич
Ковшечников Эдуард Евгеньевич
Курмакаев Рушан Ринатович
Нарлы Николай Иванович
Силяков Дмитрий Владимирович
Сысолятина Юлия Николаевна
Тран Ван Киен
Чугунов Сергей Максимович
Шекуров Вячеслав Юрьевич
Чека Полина Александровна
Сливин Виктор Дмитриевич
Чурсин Алексей Юрьевич
Турсунов Самандар Хаиталиевич
Смыков Станислав Александрович
Сапаев Асрорбек Азамат угли
Парфенов Артур Борисович
Ноговицын Андрей Юрьевич
Михайлов Артем Дмитриевич
Лыу Фан Куок Кыонг
Лузина Светлана Антоновна
Леонов Егор Дмитриевич
Додшоева Камила Султоншоевна
Денисов Никита Денисович
Гомзов Кирилл Викторович
Айвазян Айк Арменович
'''

students_str = """
1 1 1
"""

students = [i for i in students_str.split('\n') if i]

loop = asyncio.get_event_loop()


async def post_addstudent(student: schema.Student):
    query = insert(models.Student).values(**student.dict())
    async with get_async_session() as s:
        await s.execute(query)
        await s.commit()



# for student in students[:2]:
#     last, name, midle = student.split(maxsplit=2)
#     print(last, name, midle)
#     schem_student = schema.Student(last_name=last, name=name, middle_name=midle, group_id=3)
#
#     loop.run_until_complete(post_addstudent(student=schem_student))
