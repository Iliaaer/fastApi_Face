from sqlalchemy import select, insert, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
import src.models as models
import src.schema as schema

students_str = """
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
"""

students = [i for i in students_str.split('\n') if i]


async def post_addstudent(student: schema.Student, session: AsyncSession = get_async_session):
    query = insert(models.Student).values(**student.dict())
    print(1)
    await session.execute(query)
    print(2)
    await session.commit()
    print(3)

# for student in students[:2]:
#     last, name, midle = student.split(maxsplit=2)
#     print(last, name, midle)
#     schem_student = schema.Student(last_name=last, name=name, middle_name=midle, group_id=3)
# last, name, midle = students[0].split(maxsplit=2)
# print(last, name, midle)
# schem_student = schema.Student(last_name=last, name=name, middle_name=midle, group_id=3)
# post_addstudent(schem_student)
