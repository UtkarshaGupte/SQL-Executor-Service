from typing import Annotated
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from models.problems import ProblemBase
from main import app
from typing import List, Annotated
from db.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.orm  import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from httpx import AsyncClient

from routes.problems import get_db

from unittest.mock import patch, Mock


URL_DATABASE = 'postgresql://utkarshagupte:@localhost:5432/SQLExecutorTest'
engine = create_engine(URL_DATABASE)

@pytest.fixture(scope='session')
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(test_db):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_problem():
    return ProblemBase(
        title="xyz-cl",
        description="xyz-cl",
        difficulty="xyz"
    )

def test_create_problem(client, test_problem: ProblemBase):
    response = client.post("/problems", json=test_problem.dict())

    assert response.status_code == 200

@pytest.mark.anyio
async def test_read_problem(client):

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        # Create an item
        test_problem_data = {"title": "Test Problem", "description": "This is a test problem", "difficulty": "Easy"}
        response = await ac.post("/problems", json=test_problem_data)
        
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        item_id = data["id"]

        response = client.get(f"/problems/{item_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Test Problem"
        assert data["description"] == "This is a test problem"
        assert data["difficulty"] == "Easy"


@pytest.mark.asyncio
@patch('routes.problems.get_problem')
async def test_read_problem_found(mock_get_problem, client, db_session):
    mock_problem = {"id":"1", "title":"Test Problem", "description":"This is a test problem", "difficulty":"Easy"}
    mock_get_problem.return_value = mock_problem

    problemDataResponse =client.get("/problems/1")
    assert problemDataResponse.status_code == 200

    mock_get_problem.assert_called_with(1, db_session)

    problemData = problemDataResponse.json()
    assert problemData["id"] == mock_problem["id"]
    assert problemData["title"] == mock_problem["title"]
    assert problemData["description"] == mock_problem["description"]
    assert problemData["difficulty"] == mock_problem["difficulty"]
