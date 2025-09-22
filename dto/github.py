from pydantic import BaseModel, Field
from typing import Optional

class GitHubTreeRequest(BaseModel):
    """
    Model for the request body to specify the repository URL and an optional branch.
    """
    repo_url: str = Field(..., description="The full HTTPS URL of the public GitHub repository (e.g., https://github.com/owner/repo).")
    branch: Optional[str] = Field("main", description="The repository branch name (e.g., main, dev, feature-branch). Defaults to 'main'.")