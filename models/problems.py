from pydantic import BaseModel

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str

class TestcaseSchemaBase(BaseModel):
    id: int
    problemId: int
    filePath: str
    expectedOutput: str

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