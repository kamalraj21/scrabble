import requests
import os
import re

def fetch_file_from_repo(repo_url, filepath, output_dir):
    api_url = f"{repo_url}/contents/{filepath}"
    response = requests.get(api_url)
    if response.status_code == 200:
        file_content = response.json()['content']
        save_file(output_dir, filepath, file_content)
    else:
        print(f"Failed to fetch {filepath} from {repo_url}")

def save_file(output_dir, filename, content):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as file:
        file.write(content)

def parse_markdown_content(content):
    reusable_content = {}
    reusable_sections = re.findall(r'\[Reusable id="(\w+)"\](.*?)\[EndReusable\]', content, re.DOTALL)
    for section_id, section_content in reusable_sections:
        reusable_content[section_id] = section_content.strip()
    return reusable_content

def main():
    # Define your repositories and file paths here
    repositories = [
        {"url": "https://api.github.com/repos/user/repo1", "files": ["file1.md", "file2.md"]},
        {"url": "https://api.github.com/repos/user/repo2", "files": ["file3.md"]}
    ]
    output_dir = "../content"

    for repo in repositories:
        for file in repo["files"]:
            fetch_file_from_repo(repo["url"], file, output_dir)

if __name__ == "__main__":
    main()
