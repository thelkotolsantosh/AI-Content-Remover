#AI Content Remover:
A Python tool that scans your GitHub repository and removes AI-generated content patterns, converting files to natural, human-written English.

## Features
 🔍 **Detects AI Patterns**: Identifies common AI writing indicators like formal list introductions, excessive explanatory phrases, and buzzwords
  🧹 **Auto-Cleans**: Removes or simplifies AI-detected patterns automatically
 📁 **Preserves Structure**: Maintains your entire directory structure
 🚀 **Batch Processing**: Processes all relevant files in your repo
 📊 **Detailed Report**: Shows which files were modified and what patterns were found

## What It Removes
The tool detects and removes:
- Formal list introductions ("The following items:", "Here are the steps:")
- Excessive explanatory phrases ("Furthermore", "Moreover", "Additionally")
- Summary indicators ("In conclusion", "To summarize")
- Filler words ("basically", "essentially", "typically", "apparently")
- AI buzzwords ("comprehensive", "robust", "scalable", "leverage", "harness", "unlock")
- Redundant explanations and verbose passive constructions

## Installation
bash
# No external dependencies required - uses only Python standard library
git clone <your-repo>
cd <your-repo>

### Basic Usage
bash
python github_cleaner.py /path/to/your/repo
This creates a new directory called `your-repo_cleaned` with the processed files.

### Custom Output Path

bash
python github_cleaner.py /path/to/your/repo /path/to/output


## Example

bash
python github_cleaner.py ./my-cybersecurity-repo


Output:

🔍 Scanning repository: ./my-cybersecurity-repo
📁 Output will be saved to: ./my-cybersecurity-repo_cleaned

✏️  Modified: README.md (4 AI patterns found)
✅ Checked: requirements.txt (clean)
✏️  Modified: main.py (2 AI patterns found)

============================================================
📊 CLEANING REPORT
============================================================
Files processed: 15
Files modified: 6
AI patterns found: 18
Output directory: ./my-cybersecurity-repo_cleaned

✨ Cleaning complete! Your repository is ready for GitHub.
📂 Check the 'my-cybersecurity-repo_cleaned' folder for cleaned files.


## Supported File Types

The tool processes the following file types:

- **Python**: `.py`
- **Documentation**: `.md`, `.txt`
- **Configuration**: `.yml`, `.yaml`, `.json`
- **Shell**: `.sh`, `.bash`
- **Web**: `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, `.css`
- **Other Languages**: `.java`, `.cpp`, `.c`, `.go`, `.rb`, `.php`, `.swift`, `.kt`, `.rs`

## Ignored Folders

The tool skips these directories (common in GitHub repos):

- `.git`, `__pycache__`, `node_modules`
- `venv`, `.venv`, `env`
- `dist`, `build`, `migrations`
- `.idea`, `.vscode`, `.pytest_cache`, `coverage`

## How to Use With Your Cybersecurity Repo

1. **Prepare your repo** with all AI-generated content
2. **Run the cleaner**:
   bash
   python github_cleaner.py ./cybersecurity-repo
   
3. **Review the output** in the `cybersecurity-repo_cleaned` folder
4. **Copy clean files** to your actual repo or use the cleaned version directly
5. **Push to GitHub**:
   bash
   cd cybersecurity-repo_cleaned
   git add .
   git commit -m "Clean: Remove AI patterns and convert to natural English"
   git push origin main
   

## Customization

To add more AI pattern detection, edit the `AI_PATTERNS` dictionary in the script:

python
AI_PATTERNS = {
    "your_pattern_name": r"your_regex_pattern",
    # ... existing patterns
}


## What This Tool Doesn't Do
- Rewrite code logic or functionality
- Change your actual codebase (only outputs cleaned version)
- Remove comments (just cleans their language)
- Guarantee 100% AI removal (use manual review for critical content)

## Best Practices

1. **Review Manually**: Always review the cleaned files before pushing to GitHub
2. **Backup First**: Keep your original files safe
3. **Test**: Ensure your cleaned code still works correctly
4. **Selective Use**: For sensitive content, manually edit before pushing

## Requirements

- Python 3.6+
- No external dependencies

## License
Use freely for your projects. I have no issues you using this. peace :D
