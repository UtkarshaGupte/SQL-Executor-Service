from fastapi import HTTPException, Depends, APIRouter
import fastapi
from models.problems import ProblemBase, TestcaseSchemaBase, TestCaseSubmissionSchemaBase, SubmissionSchemaBase
from typing import List, Annotated
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas.problems import Problem, Testcase, TestCaseSubmission, Submission
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
    res = db.query(Problem).filter(Problem.id == problem_id).first()
    if not res:
        raise HTTPException(status_code=404, detail='Problem is not Found')
    return res

# Add new problem
@router.post("/problems")
async def create_problems(problem:ProblemBase, db: db_dependency):
    db_problem = Problem(
        title = problem.title,
        description=problem.description,
        difficulty=problem.difficulty
    )
    db.add(db_problem)
    db.commit()

    return db_problem

# Delete an existing problem
@router.delete("/problems/{problem_id}")
async def delete_problem(problem_id: int, db: db_dependency):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    
    db.delete(problem)
    db.commit()
    return {"message": "Problem deleted successfully"}


# Update a problem
@router.put("/problems/{problem_id}")
async def update_problem(problem_id: int, problem_data: ProblemBase, db: db_dependency):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    
    problem.ProblemTitle = problem_data.ProblemTitle
    problem.ProblemDescription = problem_data.ProblemDescription
    problem.ProblemDifficulty = problem_data.ProblemDifficulty
    
    db.commit()
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