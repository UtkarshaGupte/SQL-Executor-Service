import os
import shutil
from fastapi import File, HTTPException, Depends, APIRouter, UploadFile
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
async def create_testcases_for_problem(problem_id: int,db: db_dependency, testFile: UploadFile = File(...) ,outputFile: UploadFile = File(...)):
    
    # Check if the problem exists
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    
    
    test_file_path = os.path.join("test_files", testFile.filename)
    with open(test_file_path, "w+b") as test_file:
        shutil.copyfileobj(testFile.file, test_file)

    expected_output_file_path = os.path.join("output_files", outputFile.filename)
    with open(expected_output_file_path, "wb") as expected_output_file:
        shutil.copyfileobj(outputFile.file, expected_output_file)

    testcase = Testcase(
        problem_id=problem_id,
        testFile=test_file_path,
        outputFile=expected_output_file_path
    )
    db.add(testcase)
    db.commit()

    return {"message": "Test cases added successfully"}