from fastapi import File, UploadFile
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from db.database import Base

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    difficulty = Column(String)


# Define Testcases table model
class Testcase(Base):
    __tablename__ = 'testcases'

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    testFile = Column(String)
    outputFile = Column(String)

    
# Define Submissions table model
class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    status = Column(String)

# Define TestCaseSubmission table model
class TestCaseSubmission(Base):
    __tablename__ = 'testcase_submissions'

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'))
    testcase_id = Column(Integer, ForeignKey('testcases.id'))
    status = Column(String)

    