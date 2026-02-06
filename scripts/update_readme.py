#!/usr/bin/env python3
"""
Auto-update README.md with dynamic content
- Updates experience duration based on start date
- Fetches and displays top 3 recent commits
- Shows top 3 starred repositories
"""

import os
import re
from datetime import datetime
from github import Github
import requests

# Configuration
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'punithvt')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
README_PATH = 'README.md'
START_DATE = datetime(2024, 9, 1)  # Your career start date (Sept 2024)

def calculate_experience():
    """Calculate years of experience from start date"""
    now = datetime.now()
    delta = now - START_DATE
    years = delta.days / 365.25

    if years < 1:
        return "0+ years"
    elif years < 2:
        return "1+ years"
    elif years < 3:
        return "2+ years"
    else:
        return f"{int(years)}+ years"

def get_recent_commits(username, token, limit=3):
    """Fetch recent commits from user's repositories"""
    try:
        g = Github(token)
        user = g.get_user(username)

        all_commits = []
        for repo in user.get_repos():
            if not repo.fork:  # Skip forked repos
                try:
                    commits = repo.get_commits(author=username)
                    for commit in list(commits)[:5]:  # Get last 5 commits from each repo
                        all_commits.append({
                            'repo': repo.name,
                            'message': commit.commit.message.split('\n')[0][:80],
                            'date': commit.commit.author.date,
                            'url': commit.html_url
                        })
                except:
                    continue

        # Sort by date and get top 3
        all_commits.sort(key=lambda x: x['date'], reverse=True)
        return all_commits[:limit]
    except Exception as e:
        print(f"Error fetching commits: {e}")
        return []

def get_top_repos(username, token, limit=3):
    """Fetch top starred repositories"""
    try:
        g = Github(token)
        user = g.get_user(username)

        repos = []
        for repo in user.get_repos():
            if not repo.fork:
                repos.append({
                    'name': repo.name,
                    'description': repo.description or 'No description',
                    'stars': repo.stargazers_count,
                    'url': repo.html_url,
                    'language': repo.language or 'Unknown'
                })

        # Sort by stars and get top 3
        repos.sort(key=lambda x: x['stars'], reverse=True)
        return repos[:limit]
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def update_readme():
    """Update README.md with dynamic content"""

    # Read current README
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update experience duration
    experience = calculate_experience()
    content = re.sub(
        r'experience: "[^"]*"',
        f'experience: "{experience} in AI/ML and Product Development"',
        content
    )

    # 2. Get recent commits
    commits = get_recent_commits(GITHUB_USERNAME, GITHUB_TOKEN)
    commits_section = "\n### 📝 Recent Activity\n\n"
    for commit in commits:
        commits_section += f"- **[{commit['repo']}]({commit['url']})**: {commit['message']}\n"

    # 3. Get top repositories
    repos = get_top_repos(GITHUB_USERNAME, GITHUB_TOKEN)
    repos_section = "\n### ⭐ Featured Projects\n\n"
    for repo in repos:
        repos_section += f"- **[{repo['name']}]({repo['url']})** - {repo['description'][:60]}... ⭐ {repo['stars']}\n"

    # 4. Insert dynamic sections before "GitHub Analytics"
    # Remove old dynamic sections if they exist
    content = re.sub(r'\n### 📝 Recent Activity\n\n.*?(?=\n##|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'\n### ⭐ Featured Projects\n\n.*?(?=\n##|\Z)', '', content, flags=re.DOTALL)

    # Insert new sections before GitHub Analytics
    insert_pos = content.find('## 📊 GitHub Analytics')
    if insert_pos != -1:
        dynamic_content = f"\n{commits_section}\n{repos_section}\n"
        content = content[:insert_pos] + dynamic_content + content[insert_pos:]

    # Write updated README
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ README updated successfully!")
    print(f"📅 Experience: {experience}")
    print(f"📝 Recent commits: {len(commits)}")
    print(f"⭐ Featured repos: {len(repos)}")

if __name__ == '__main__':
    update_readme()
