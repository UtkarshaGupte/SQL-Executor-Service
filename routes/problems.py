from fastapi import HTTPException, Depends, APIRouter
import fastapi
from models.problems import ProblemBase, TestcaseSchemaBase, TestCaseSubmissionSchemaBase, SubmissionSchemaBase
from typing import List, Annotated
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas.problems import Problem, Testcase, TestCaseSubmission, Submission
from controller.problems import get_problem, post_problem, del_problem, upd_problem
router = fastapi.APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Get Problem 
@router.get("/problems/{problem_id}")
async def read_problem(problem_id: int, db: db_dependency):
    res = get_problem(problem_id, db)
    if not res:
        raise HTTPException(status_code=404, detail='Problem is not Found')
    return res

# Add new problem
@router.post("/problems")
async def create_problems(problem:ProblemBase, db: db_dependency):
    db_problem = post_problem(problem, db)
    return db_problem

# Delete an existing problem
@router.delete("/problems/{problem_id}")
async def delete_problem(problem_id: int, db: db_dependency):
    problem = get_problem(problem_id, db)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')   
    del_problem(problem_id, db)
    return {"message": "Problem deleted successfully"}


# Update a problem
@router.put("/problems/{problem_id}")
async def update_problem(problem_id: int, problem_data: ProblemBase, db: db_dependency):
    problem = upd_problem(problem_id,problem_data, db)
    return problem


# Add test cases for a problem
@router.post("/problems/{problem_id}/testcases")
async def create_testcases_for_problem(problem_id: int, testcases: List[TestcaseSchemaBase], db: db_dependency):
    # Check if the problem exists
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')

    # Create test cases for the problem
    for testcase_data in testcases:
        testcase = Testcase(
            problem_id=problem_id,
            filePath=testcase_data.filePath,
            expectedOutput=testcase_data.expectedOutput
        )
        db.add(testcase)
    
    db.commit()
    return {"message": "Test cases added successfully"}