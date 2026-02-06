# 🤖 README Auto-Update Scripts

This directory contains automation scripts that keep your README.md updated with the latest information.

## Features

✨ **Auto-update experience** - Calculates years of experience from your start date (Sept 2024)
📝 **Recent commits** - Shows your top 3 latest commits across all repos
⭐ **Featured projects** - Displays your top 3 most starred repositories
🔄 **Auto-commit** - Automatically commits changes to your README

## How It Works

### GitHub Actions Workflow
- **Schedule**: Runs daily at 00:00 UTC
- **Triggers**: Also runs on every push to main branch
- **Manual**: Can be triggered manually from GitHub Actions tab

### Python Script
The `update_readme.py` script:
1. Calculates experience duration from your start date
2. Fetches your recent commits using GitHub API
3. Gets your top starred repositories
4. Updates the README.md file
5. GitHub Actions automatically commits the changes

## Setup Instructions

### 1. Enable GitHub Actions
The workflow file is already created at `.github/workflows/update-readme.yml`

### 2. Configure Permissions
Go to your GitHub repository:
- Settings → Actions → General
- Under "Workflow permissions", select "Read and write permissions"
- Save changes

### 3. Test the Workflow
You can manually trigger the workflow:
- Go to "Actions" tab in your repository
- Click on "Update README" workflow
- Click "Run workflow" button

## Configuration

### Update Your Start Date
Edit `scripts/update_readme.py` line 18:
```python
START_DATE = datetime(2024, 9, 1)  # Change to your actual start date
```

### Change Update Frequency
Edit `.github/workflows/update-readme.yml` line 5:
```yaml
- cron: '0 0 * * *'  # Daily at midnight
# Other options:
# - cron: '0 0 * * 0'  # Weekly (Sunday)
# - cron: '0 0 1 * *'  # Monthly (1st day)
```

## Testing Locally

To test the script locally:

```bash
# Install dependencies
cd scripts
pip install -r requirements.txt

# Set environment variables
export GITHUB_USERNAME=punithvt
export GITHUB_TOKEN=your_github_token

# Run the script
python update_readme.py
```

## Generated Sections

The script adds these sections to your README:

### 📝 Recent Activity
Shows your latest 3 commits with:
- Repository name
- Commit message
- Direct link to commit

### ⭐ Featured Projects
Displays your top 3 starred repos with:
- Repository name and link
- Description
- Star count
- Primary language

## Notes

- The script only processes non-forked repositories
- Commit messages are truncated to 80 characters
- Repository descriptions are truncated to 60 characters
- All updates are inserted before the "GitHub Analytics" section

## Troubleshooting

**Workflow not running?**
- Check repository settings → Actions are enabled
- Verify workflow permissions are set to "Read and write"

**No updates appearing?**
- Check Actions tab for error logs
- Ensure GITHUB_TOKEN has proper permissions

**Want to change what's displayed?**
- Edit `update_readme.py` to customize the output format
- Adjust the `limit` parameters in function calls

---

🤖 **Last updated**: Automatically by GitHub Actions
