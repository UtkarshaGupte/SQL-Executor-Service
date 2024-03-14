from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.problems import Problem, Testcase, TestCaseSubmission, Submission
from models.problems import ProblemBase, TestcaseSchemaBase, TestCaseSubmissionSchemaBase, SubmissionSchemaBase


def get_problem(problem_id, db: Session):
    return db.query(Problem).filter(Problem.id == problem_id).first()

def post_problem(problem, db: Session):
    db_problem = Problem(
        title = problem.title,
        description=problem.description,
        difficulty=problem.difficulty
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

def del_problem(problem_id, db: Session):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    db.delete(problem)
    db.commit()

def upd_problem(problem_id, problem_data, db: Session):

    problem = get_problem(problem_id, db)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    
    problem.title = problem_data.title
    problem.description = problem_data.description
    problem.difficulty = problem_data.difficulty
    
    db.commit()
    return problem


