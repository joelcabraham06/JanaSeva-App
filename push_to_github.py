import os
import base64
import httpx
import sys

GITHUB_REPO = "joelcabraham06/JanaSeva-App"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

IGNORE_DIRS = {
    ".git", "__pycache__", "node_modules", ".pytest_cache", 
    "dist", "build", ".venv", "venv", "env"
}

IGNORE_FILES = {
    "janaseva.db", "test_janaseva_app.db", ".DS_Store"
}

def is_ignored(path):
    rel_path = os.path.relpath(path, PROJECT_DIR)
    parts = rel_path.split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS or part in IGNORE_FILES:
            return True
        if part.endswith(".pyc") or part.endswith(".db"):
            return True
    return False

def get_all_files():
    files_to_upload = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            full_path = os.path.join(root, f)
            if not is_ignored(full_path):
                rel_path = os.path.relpath(full_path, PROJECT_DIR).replace("\\", "/")
                files_to_upload.append((full_path, rel_path))
    return files_to_upload

def upload_to_github(pat_token):
    headers = {
        "Authorization": f"Bearer {pat_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    files = get_all_files()
    print(f"Found {len(files)} files to upload to https://github.com/{GITHUB_REPO}...")
    
    success_count = 0
    fail_count = 0
    
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        # Check repo access
        repo_res = client.get(f"https://api.github.com/repos/{GITHUB_REPO}", headers=headers)
        if repo_res.status_code != 200:
            print(f"Error accessing repo {GITHUB_REPO}: {repo_res.status_code} - {repo_res.text}")
            return False
            
        real_repo = repo_res.json().get("full_name", GITHUB_REPO)
        print(f"Connected to repo {real_repo} successfully!")
        
        for full_path, rel_path in files:
            try:
                with open(full_path, "rb") as fp:
                    content_bytes = fp.read()
                content_b64 = base64.b64encode(content_bytes).decode("utf-8")
                
                url = f"https://api.github.com/repos/{real_repo}/contents/{rel_path}"
                
                # Check if file exists to get SHA
                get_res = client.get(url, headers=headers)
                sha = None
                if get_res.status_code == 200:
                    sha = get_res.json().get("sha")
                    
                payload = {
                    "message": f"Add/Update {rel_path} via Janaseva Build Deployer",
                    "content": content_b64,
                    "branch": "main"
                }
                if sha:
                    payload["sha"] = sha
                    
                put_res = client.put(url, headers=headers, json=payload)
                if put_res.status_code in (200, 201):
                    print(f"[OK] Uploaded: {rel_path}")
                    success_count += 1
                else:
                    print(f"[FAIL] Failed: {rel_path} ({put_res.status_code}: {put_res.text})")
                    fail_count += 1
            except Exception as e:
                print(f"[FAIL] Error uploading {rel_path}: {e}")
                fail_count += 1
                
    print(f"\n==========================================")
    print(f"Upload Complete! {success_count} succeeded, {fail_count} failed.")
    print(f"Repository: https://github.com/{real_repo}")
    print(f"==========================================\n")
    return fail_count == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python push_to_github.py <GITHUB_PAT_TOKEN>")
        sys.exit(1)
    token = sys.argv[1]
    upload_to_github(token)
