from fastapi.testclient import TestClient

from src.home import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_add_students():
    students_str = """
    Айвазян Айк Арменович
    """

    students = [i for i in students_str.split('\n') if i]
    for student in students:
        last, name, midle = student.split(maxsplit=2)
        json_student = {
            "name": name,
            "last_name": last,
            "middle_name": midle,
            "group_id": 3
        }
        response = client.post("postdata/addstudent",
                               headers={"Accept": "application/json", "Content-Type": "application/json"},
                               json=json_student)
        assert response.status_code == 200
