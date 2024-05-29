from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

import src.models as models
import src.schema as schema
from src.database import get_async_session

app = FastAPI(
    title="Verification"
)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "src/static"),
    name="static",
)

templates = Jinja2Templates(
    directory=Path(__file__).parent.parent.absolute() / "src/templates",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request},
    )


@app.get("/creategroup")
async def get_creategroup(request: Request):
    return templates.TemplateResponse(
        "creategroup.html",
        {"request": request},
    )


@app.get("/addstudent")
async def get_add_student(request: Request):
    return templates.TemplateResponse(
        "addstudent.html",
        {"request": request},
    )


@app.get("/showgroup")
async def get_showgroup(request: Request):
    return templates.TemplateResponse(
        "showgroup.html",
        {"request": request},
    )


@app.get("/showattendance")
async def get_showattendance(request: Request):
    return templates.TemplateResponse(
        "showattendance.html",
        {"request": request},
    )


@app.get("/showvideo")
async def get_showvideo(request: Request):
    return templates.TemplateResponse(
        "showvideo.html",
        {"request": request},
    )


@app.get("/addaudience")
async def get_addaudience(request: Request):
    return templates.TemplateResponse(
        "addaudience.html",
        {"request": request},
    )


@app.get("/add_activity_information")
async def get_add_activity_information(request: Request):
    return templates.TemplateResponse(
        "add_activity_information.html",
        {"request": request},
    )


@app.post("/postdata/creategroup")
async def post_creategroup(group: schema.GroupStudents, session: AsyncSession = Depends(get_async_session)):
    number_group = group.number
    print(number_group)
    group = schema.GroupStudents(number=number_group)
    stmt = insert(models.GroupStudents).values(**group.dict())
    await session.execute(stmt)
    await session.commit()
    return {"numberGroup": number_group}


@app.get("/getdata/getgroups")
async def get_groups(session: AsyncSession = Depends(get_async_session)):
    query = select(models.GroupStudents)
    result = await session.execute(query)
    groups = [r[0].number for r in result.all()]
    return groups


@app.get("/getdata/getgroupsid")
async def get_groups_id(session: AsyncSession = Depends(get_async_session)):
    query = select(models.GroupStudents)
    result = await session.execute(query)
    groups = {}
    for r in result.all():
        groups[r[0].number] = r[0].id
    return groups


@app.post("/postdata/addstudent")
async def post_addstudent(student: schema.Student, session: AsyncSession = Depends(get_async_session)):
    query = insert(models.Student).values(**student.dict())
    await session.execute(query)
    await session.commit()
    print(student)
    return {"student": student}


@app.get("/getdata/students/{groupid}")
async def get_students(groupid: int, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Student).where(models.Student.group_id == groupid).order_by(models.Student.last_name)
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    students = [[r[0].last_name, r[0].name, r[0].middle_name] for r in result_all]
    return students


@app.get("/getdata/discipline/{groupid}")
async def get_discipline(groupid: int, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Discipline.name).where(models.Discipline.group_id == groupid).order_by(
        models.Discipline.name).distinct(models.Discipline.name)
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    disciplines = [r[0] for r in result_all]
    print(f"group {groupid} = {disciplines}")
    return disciplines


@app.get("/getdata/discipline/{groupid}/{discipline}")
async def get_discipline_info(groupid: int, discipline: str, session: AsyncSession = Depends(get_async_session)):
    print(discipline)
    query = select(models.Discipline).where(models.Discipline.group_id == groupid).where(
        models.Discipline.name == discipline)
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    info = [[r[0].id, r[0].data, r[0].time] for r in result_all]
    print(info)
    return info


@app.get("/getdata/students/{last_name}/{first_name}/{middle_name}")
async def get_student_id(last_name: str, first_name: str, middle_name: str,
                         session: AsyncSession = Depends(get_async_session)) -> int:
    query = (select(models.Student.id).
             where(models.Student.last_name == last_name).
             where(models.Student.name == first_name).
             where(models.Student.middle_name == middle_name))
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    result = result_all[0][0]
    print(last_name, first_name, middle_name, result)
    return result


@app.get("/getdata/attendance/{studentid}/{disciplineid}")
async def get_attendance(studentid: int, disciplineid: int, session: AsyncSession = Depends(get_async_session)):
    query_discipline = select(models.Discipline.time).where(models.Discipline.id == disciplineid)
    result_discipline = await session.execute(query_discipline)
    result_discipline = result_discipline.all()
    if len(result_discipline) == 0:
        return []
    result_discipline = result_discipline[0][0]

    query_attendance = select(models.Attendance.time).where(models.Attendance.discipline_id == disciplineid).where(
        models.Attendance.student_id == studentid)
    result_attendance = await session.execute(query_attendance)
    result_attendance = result_attendance.all()
    if len(result_attendance) == 0:
        return []
    result_attendance = result_attendance[0][0]

    time_discipline = result_discipline.second + (result_discipline.minute + result_discipline.hour * 60) * 60
    time_attendance = result_attendance.second + (result_attendance.minute + result_attendance.hour * 60) * 60

    time_diff = max(0, time_attendance - time_discipline)

    return [time_diff]


@app.get("/getdata/frame")
async def get_frame(session: AsyncSession = Depends(get_async_session)):
    query = select(models.Frame)
    result = await session.execute(query)
    frames = [r[0].name for r in result.all()]
    return frames


@app.get("/getdata/frame/{frame}")
async def get_frame_id(frame: str, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Frame.id).where(models.Frame.name == frame)
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    frame_id = result_all[0][0]
    print(frame, frame_id)
    return frame_id


@app.get("/getdata/audience/{frame_id}")
async def get_audience(frame_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Audience).where(models.Audience.frame_id == frame_id)
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    audiences = [r[0].audience for r in result_all]
    print(frame_id, audiences)
    return audiences


@app.post("/postdata/audience")
async def post_addaudience(audience: schema.Audience, session: AsyncSession = Depends(get_async_session)):
    query = insert(models.Audience).values(**audience.dict())
    await session.execute(query)
    await session.commit()
    print(audience)
    return {"audience": audience}


@app.get("/getdata/audience/{frame_id}/{audience}")
async def get_audience_id(frame_id: int, audience: int, session: AsyncSession = Depends(get_async_session)):
    query = select(models.Audience.id).where(models.Audience.frame_id == frame_id).where(
        models.Audience.audience == audience)
    result = await session.execute(query)
    result_all = result.all()
    if len(result_all) == 0:
        return []
    audience_id = result_all[0][0]
    return audience_id


@app.post("/postdata/discipline")
async def post_discipline(discipline: schema.Discipline, session: AsyncSession = Depends(get_async_session)):
    query = insert(models.Discipline).values(**discipline.dict())
    await session.execute(query)
    await session.commit()
    print(discipline)
    return {"discipline": discipline}
