#!/usr/bin/env python3
"""
GitHub Repo AI Content Remover & Cleaner
Scans files for AI-generated content patterns and converts them to natural English.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


class GitHubRepoCleaner:
    """Tool to identify and clean AI-generated content from code and documentation files."""
    
    # Patterns commonly found in AI-generated text
    AI_PATTERNS = {
        "formal_list_start": r"\b(?:The following|These are|Here are|Below is|This includes)\s+(?:the\s+)?(?:list|items?|examples?|steps?|points?|features?)(?:\s+of)?:",
        "explanatory_phrase": r"\b(?:In other words|Furthermore|Moreover|Additionally|On the other hand|As mentioned|It is important to note that|It should be noted that)\b",
        "summary_indicators": r"\b(?:In summary|To summarize|In conclusion|In essence|Ultimately|Finally)\b",
        "redundant_bullets": r"^[\s]*[-•*]\s+\w+\s*:\s*",  # Bullet points with colons
        "generic_intro": r"^This\s+(?:guide|article|document|tool|script)\s+(?:aims to|provides|explains|covers)",
        "verbose_explanation": r"\b(?:essentially|basically|generally|typically|usually|normally|obviously|clearly)\s+",
        "ai_filler": r"\b(?:comprehensive|robust|scalable|efficient|seamless|leverage|harness|unlock|maximize)\b",
        "passive_voice_excess": r"\bcan be\s+\w+ed\b|\bis\s+\w+ed\b",
    }
    
    # File extensions to process
    PROCESSABLE_EXTENSIONS = {
        '.py', '.md', '.txt', '.yml', '.yaml', '.json', 
        '.sh', '.bash', '.js', '.ts', '.jsx', '.tsx',
        '.html', '.css', '.java', '.cpp', '.c', '.go',
        '.rb', '.php', '.swift', '.kt', '.rs'
    }
    
    # Folders to skip
    SKIP_FOLDERS = {
        '.git', '__pycache__', 'node_modules', '.env',
        'venv', 'env', '.venv', 'dist', 'build', '.pytest_cache',
        '.idea', '.vscode', 'migrations', 'coverage'
    }
    
    def __init__(self, repo_path: str, output_path: str = None):
        """
        Initialize the cleaner.
        
        Args:
            repo_path: Path to the GitHub repository
            output_path: Path to save cleaned files (default: repo_path + '_cleaned')
        """
        self.repo_path = Path(repo_path)
        self.output_path = Path(output_path) if output_path else Path(str(self.repo_path) + '_cleaned')
        self.issues_found = []
        self.files_processed = 0
        self.files_modified = 0
        
    def scan_and_clean(self) -> Dict:
        """Scan repo and clean files."""
        if not self.repo_path.exists():
            print(f"❌ Repository path not found: {self.repo_path}")
            return {}
        
        print(f"🔍 Scanning repository: {self.repo_path}")
        print(f"📁 Output will be saved to: {self.output_path}\n")
        
        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Process all files
        self._process_directory(self.repo_path, self.output_path)
        
        # Print report
        self._print_report()
        
        return {
            "files_processed": self.files_processed,
            "files_modified": self.files_modified,
            "issues_found": len(self.issues_found),
            "output_path": str(self.output_path)
        }
    
    def _process_directory(self, source_dir: Path, dest_dir: Path):
        """Recursively process directory."""
        for item in source_dir.iterdir():
            # Skip certain directories
            if item.is_dir():
                if item.name in self.SKIP_FOLDERS or item.name.startswith('.'):
                    continue
                
                # Create corresponding directory in output
                new_dest = dest_dir / item.name
                new_dest.mkdir(exist_ok=True)
                self._process_directory(item, new_dest)
            
            # Process files
            elif item.is_file():
                if item.suffix in self.PROCESSABLE_EXTENSIONS:
                    self._process_file(item, dest_dir)
                else:
                    # Copy non-processable files as-is
                    import shutil
                    shutil.copy2(item, dest_dir / item.name)
    
    def _process_file(self, file_path: Path, output_dir: Path):
        """Process a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.files_processed += 1
            
            # Detect AI patterns
            issues = self._detect_ai_patterns(content)
            
            # Clean content
            cleaned_content = self._clean_content(content, issues)
            
            # Write cleaned file
            output_file = output_dir / file_path.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            if issues:
                self.files_modified += 1
                self.issues_found.append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "issues_count": len(issues),
                    "issues": issues
                })
                print(f"✏️  Modified: {file_path.name} ({len(issues)} AI patterns found)")
            else:
                print(f"✅ Checked: {file_path.name} (clean)")
                
        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")
    
    def _detect_ai_patterns(self, content: str) -> List[Tuple[str, str]]:
        """Detect AI-generated patterns in content."""
        issues = []
        
        for pattern_name, pattern in self.AI_PATTERNS.items():
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                issues.append((pattern_name, match.group()))
        
        return issues
    
    def _clean_content(self, content: str, issues: List[Tuple[str, str]]) -> str:
        """Clean AI patterns from content."""
        cleaned = content
        
        # Remove formal list introductions
        cleaned = re.sub(
            r'\b(?:The following|These are|Here are|Below is|This includes)\s+(?:the\s+)?(?:list|items?|examples?|steps?)\s*:',
            '',
            cleaned,
            flags=re.IGNORECASE
        )
        
        # Simplify explanatory phrases
        explanatory_replacements = {
            r'\bIn other words[,:]?\s+': '',
            r'\bFurthermore[,:]?\s+': '',
            r'\bMoreover[,:]?\s+': '',
            r'\bAdditionally[,:]?\s+': '',
            r'\bOn the other hand[,:]?\s+': '',
            r'\bIt is important to note that\s+': 'Note: ',
            r'\bIt should be noted that\s+': 'Note: ',
        }
        
        for pattern, replacement in explanatory_replacements.items():
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        # Remove or simplify summary indicators
        summary_removals = {
            r'\b(?:In summary|To summarize)[,:]?\s+': '',
            r'\b(?:In conclusion|In essence)[,:]?\s+': '',
            r'\bUltimately[,:]?\s+': '',
        }
        
        for pattern, replacement in summary_removals.items():
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        # Replace verbose filler words
        filler_replacements = {
            r'\bessentially\s+': '',
            r'\bbasically\s+': '',
            r'\bgenerally\s+': '',
            r'\btypically\s+': '',
            r'\bapparently\s+': '',
            r'\bobviously\s+': '',
        }
        
        for pattern, replacement in filler_replacements.items():
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        # Replace AI-specific buzzwords with simpler alternatives
        buzzword_replacements = {
            r'\bcomprehensive\b': 'full',
            r'\brobust\b': 'strong',
            r'\bscalable\b': 'flexible',
            r'\bseamless\b': 'smooth',
            r'\bleverage\b': 'use',
            r'\bharness\b': 'use',
            r'\bunlock\b': 'enable',
            r'\bmaximize\b': 'improve',
            r'\boptimize\b': 'improve',
        }
        
        for pattern, replacement in buzzword_replacements.items():
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        # Fix multiple spaces
        cleaned = re.sub(r' {2,}', ' ', cleaned)
        
        # Clean up extra blank lines
        cleaned = re.sub(r'\n\n\n+', '\n\n', cleaned)
        
        return cleaned.strip()
    
    def _print_report(self):
        """Print cleaning report."""
        print("\n" + "="*60)
        print("📊 CLEANING REPORT")
        print("="*60)
        print(f"Files processed: {self.files_processed}")
        print(f"Files modified: {self.files_modified}")
        print(f"AI patterns found: {len(self.issues_found)}")
        print(f"Output directory: {self.output_path}")
        
        if self.issues_found:
            print("\n🔍 Files with AI patterns detected:\n")
            for file_info in self.issues_found[:10]:  # Show first 10
                print(f"  📄 {file_info['file']} ({file_info['issues_count']} patterns)")
        
        print("\n✨ Cleaning complete! Your repository is ready for GitHub.")
        print(f"📂 Check the '{self.output_path.name}' folder for cleaned files.\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python github_cleaner.py <repo_path> [output_path]")
        print("\nExample:")
        print("  python github_cleaner.py ./my-cybersecurity-repo")
        print("  python github_cleaner.py ./my-repo ./cleaned-repo")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    cleaner = GitHubRepoCleaner(repo_path, output_path)
    result = cleaner.scan_and_clean()
    
    return result


if __name__ == "__main__":
    main()
