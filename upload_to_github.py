#!/usr/bin/env python3
"""Upload entire Jekyll site to GitHub via API (no git push needed)."""

import subprocess
import json
import os
import base64
import sys

REPO = "QuanshuYang05/quanshuyang05.github.io"
BRANCH = "main"
SITE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE = {'.git', '.gitignore', 'Gemfile', 'Gemfile.lock', 'CLAUDE.md', 'upload_to_github.py'}


def gh_api(endpoint, method="GET", data=None):
    """Call GitHub API via gh CLI."""
    cmd = ["gh", "api", endpoint, "--method", method]
    if data:
        for k, v in data.items():
            cmd.extend(["-f", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"API error: {result.stderr}")
        return None
    return json.loads(result.stdout) if result.stdout else {}


def get_current_commit():
    ref = gh_api(f"repos/{REPO}/git/refs/heads/{BRANCH}")
    if not ref:
        return None, None
    sha = ref["object"]["sha"]
    commit = gh_api(f"repos/{REPO}/git/commits/{sha}")
    return sha, commit["tree"]["sha"] if commit else None


def create_blob(filepath):
    with open(filepath, "rb") as f:
        content = f.read()
    try:
        text = content.decode("utf-8")
        encoding = "utf-8"
        data = {"content": text, "encoding": encoding}
    except UnicodeDecodeError:
        b64 = base64.b64encode(content).decode("ascii")
        encoding = "base64"
        data = {"content": b64, "encoding": encoding}
    result = gh_api(f"repos/{REPO}/git/blobs", method="POST", data=data)
    return result["sha"] if result else None


def collect_files():
    files = []
    for root, dirs, filenames in os.walk(SITE_DIR):
        rel_root = os.path.relpath(root, SITE_DIR)
        if rel_root == '.':
            rel_root = ''
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for fname in filenames:
            if fname in EXCLUDE:
                continue
            rel_path = os.path.join(rel_root, fname).replace('\\', '/')
            abs_path = os.path.join(root, fname)
            files.append((rel_path, abs_path))
    return files


def main():
    print("Collecting files...")
    files = collect_files()
    print(f"Found {len(files)} files to upload")

    print("Getting current commit...")
    commit_sha, tree_sha = get_current_commit()
    if not commit_sha:
        print("Failed to get current commit")
        sys.exit(1)
    print(f"Current commit: {commit_sha[:12]}, tree: {tree_sha[:12]}")

    print("Creating blobs...")
    tree_entries = []
    for i, (rel_path, abs_path) in enumerate(files):
        blob_sha = create_blob(abs_path)
        if not blob_sha:
            print(f"  FAILED: {rel_path}")
            continue
        ext = os.path.splitext(rel_path)[1].lower()
        # Images and binaries should use 100644 blob type
        tree_entries.append({
            "path": rel_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob_sha
        })
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(files)} blobs created...")

    print(f"Created {len(tree_entries)} blobs")

    print("Creating tree...")
    tree_data = {"tree": tree_entries, "base_tree": tree_sha}
    # gh api doesn't support JSON body easily, so use raw curl
    tree_json = json.dumps(tree_data)
    tree_file = os.path.join(SITE_DIR, ".tree.json")
    with open(tree_file, "w") as f:
        f.write(tree_json)

    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/trees", "--method", "POST",
         "--input", tree_file],
        capture_output=True, text=True, timeout=60
    )
    os.remove(tree_file)

    if result.returncode != 0:
        print(f"Tree creation failed: {result.stderr}")
        sys.exit(1)
    new_tree = json.loads(result.stdout)
    new_tree_sha = new_tree["sha"]
    print(f"New tree: {new_tree_sha[:12]}")

    print("Creating commit...")
    commit_data = {
        "message": "Deploy Jekyll site: 杨荃舒 AI+网络安全个人主页",
        "tree": new_tree_sha,
        "parents": commit_sha
    }
    commit_json = json.dumps(commit_data)
    commit_file = os.path.join(SITE_DIR, ".commit.json")
    with open(commit_file, "w") as f:
        f.write(commit_json)

    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/commits", "--method", "POST",
         "--input", commit_file],
        capture_output=True, text=True, timeout=30
    )
    os.remove(commit_file)

    if result.returncode != 0:
        print(f"Commit creation failed: {result.stderr}")
        sys.exit(1)
    new_commit = json.loads(result.stdout)
    new_commit_sha = new_commit["sha"]
    print(f"New commit: {new_commit_sha[:12]}")

    print("Updating branch ref...")
    ref_data = {"sha": new_commit_sha, "force": True}
    ref_json = json.dumps(ref_data)
    ref_file = os.path.join(SITE_DIR, ".ref.json")
    with open(ref_file, "w") as f:
        f.write(ref_json)

    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/refs/heads/{BRANCH}", "--method", "PATCH",
         "--input", ref_file],
        capture_output=True, text=True, timeout=30
    )
    os.remove(ref_file)

    if result.returncode != 0:
        print(f"Ref update failed: {result.stderr}")
        sys.exit(1)

    print(f"\nDone! Site deployed to https://quanshuyang05.github.io/")
    print(f"Commit: {new_commit_sha[:12]}")


if __name__ == "__main__":
    main()
