import requests
import re
from fastapi import FastAPI, HTTPException, RedirectResponse
from dto.github import GitHubTreeRequest
from helper.utils import Helper
from fastapi.responses import PlainTextResponse


handle = Helper()

app = FastAPI(
    title="GitHub Repository Tree Generator",
    description="An API to generate a human-readable file tree for any public GitHub repository by providing its URL.",
    version="1.0.0"
)


# --- Root Endpoint (for welcome message) ---
@app.get("/")
async def read_root():
    # return {"message": "Welcome to the GitHub Repository Tree Generator API. Navigate to /docs to see the interactive Swagger UI."}
    return RedirectResponse(url="/docs")


@app.post("/tree", summary="Generate Repository Tree (Text Output)", response_class=PlainTextResponse)
async def get_repository_text_tree(request: GitHubTreeRequest):

    # Parse the owner and repo name from the provided URL
    match = re.search(r"github\.com/([^/]+)/([^/]+)", request.repo_url)
    if not match:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub URL format. Please provide a valid URL like https://github.com/owner/repo."
        )
    
    owner, repo = match.groups()

    try:
        # Step 1: Get the latest commit SHA of the specified branch
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{request.branch}"
        response = requests.get(commit_url)
        response.raise_for_status()
        
        commit_data = response.json()
        tree_sha = commit_data['commit']['tree']['sha']

        # Step 2: Fetch the full recursive tree using the SHA
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1"
        tree_response = requests.get(tree_url)
        tree_response.raise_for_status()
        
        tree_data = tree_response.json()
        
        all_paths = [item['path'] for item in tree_data.get('tree', [])]

        # Step 3: Build the tree structure and convert to text
        tree_structure = handle.build_tree(all_paths)
        text_tree_output = handle.to_text_tree(tree_structure)
        
        return text_tree_output

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found, branch does not exist, or repository is private. Please check the URL and branch name.")
        else:
            raise HTTPException(status_code=err.response.status_code, detail=f"An error occurred with the GitHub API: {err.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8110)