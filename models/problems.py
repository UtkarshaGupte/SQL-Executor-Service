from pydantic import BaseModel

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str

class TestcaseSchemaBase(BaseModel):
    problem_id: int
    testFile: str
    outputFile: str

class SubmissionSchemaBase(BaseModel):
    id: int
    userId: int
    problemId: int
    status: str

class TestCaseSubmissionSchemaBase(BaseModel):
    id: int
    submissionId: int
    testcaseId: int
    status: str