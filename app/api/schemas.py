from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    keyword : str = Field(..., min_length=1, description='Search keyword')

class AnalyzeResponse(BaseModel):
    keyword: str
    found: bool
    transcript_excerpt: str | None = None
    sentiment: str | None = None
    summary: str | None = None
    message: str | None = None