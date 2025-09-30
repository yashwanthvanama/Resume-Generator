# Resume Generator

A Python script to compile LaTeX files into PDF format.

## Prerequisites

### Python Virtual Environment

This project uses a Python virtual environment to manage dependencies. To set it up:

**Quick activation script:**
```bash
# Method 1: Source the activation script (recommended)
source activate_env.sh

# Method 2: Use the dot notation
. activate_env.sh

# Method 3: Get instructions
./activate.sh
```

### LaTeX Installation

This project requires LaTeX to be installed on your system. On macOS, you can install it using Homebrew:

```bash
# For a lighter installation (~100MB)
brew install --cask basictex

# For a full installation (~4GB) - includes all packages
brew install --cask mactex
```

After installation, restart your terminal or run:
```bash
eval "$(/usr/libexec/path_helper)"
```

### Required LaTeX Packages

If you installed BasicTeX (lighter version), you'll need to install additional packages:

```bash
# Update the package manager first
sudo tlmgr update --self

# Install required packages
sudo tlmgr install enumitem titlesec hyperref xcolor fontspec
```

## Usage

### Setup and Activation

1. **Activate the virtual environment:**
   ```bash
   # Recommended method (using our script)
   source activate_env.sh
   
   # Alternative methods
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Verify installation:**
   ```bash
   pip list  # Should show PyPDF2, requests, and other dependencies
   ```

### Running the Resume Compiler

#### Interactive Mode
Run the script without arguments to see available files and choose one:
```bash
python src/compile_resume.py
```

#### Command Line Mode
Specify the file name as an argument:
```bash
python src/compile_resume.py your_resume_file
```

The compiled PDF will be saved in the `output/` directory with the same name as the input file.

## Firecrawl: Scrape Job Postings

You can fetch the content of a job posting page using Firecrawl's Scrape API and print it to your terminal.

### Prerequisites

1. Copy `.env.example` to `.env` and put your API key in it:

```bash
cp .env.example .env
```

Edit `.env` and set:

```
FIRECRAWL_API_KEY=your_api_key_here
```

Alternatively, you can export it in your shell:

```bash
export FIRECRAWL_API_KEY=your_api_key_here
```

### Run the scraper (prints to stdout)

```bash
python -m src.scrape_job_posting "https://example.com/jobs/12345"
```

Optional flag:

- `--only-main-content` attempt to extract just the core content

## Project Structure

```
Resume Generator/
├── src/
│   └── compile_resume.py           # Main compilation script
├── templates/                      # LaTeX template files
├── original_resume/         # Original PDF resumes
├── output/                  # Generated PDF files
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── activate_env.sh          # Virtual environment activation script
└── README.md                # This file
```

## Features

- **Automated LaTeX Compilation**: Automatically compiles LaTeX files to PDF
- **Clean Output Management**: Saves output to a dedicated directory and cleans up auxiliary files
- **Virtual Environment Support**: Isolated Python environment with all dependencies
- **Error Handling**: Comprehensive error messages and fallback options

## Live Watching (Auto-Compile on Save)

You can enable automatic recompilation whenever you save a LaTeX file in the `templates/` directory using the watcher script.

### Install Dependency (if not already installed)
`watchdog` is already listed in `requirements.txt`, so if you've installed dependencies you're set:

```bash
pip install -r requirements.txt
```

### Start the Watcher
From the project root:

```bash
python watch_templates.py
```

You'll see output like:

```
📁 Watching templates directory: /path/to/project/templates
🔧 Using compile script: /path/to/project/src/compile_resume.py
🚀 Starting file watcher... (Press Ctrl+C to stop)
💾 Will compile when you save changes to .tex files
```

Then any time you save a `.tex` file, it will automatically recompile:

```
Detected save in: example_resume.tex
Compiling example_resume.tex...
✅ Successfully compiled example_resume.tex
```

### Debounce Logic
The watcher ignores duplicate rapid events (<1s apart) for the same file and waits 0.1s after a save to ensure the editor has finished writing the file.

### Stopping the Watcher
Press `Ctrl + C` in the terminal running the watcher.

### Editing or Extending
Watcher script: `watch_templates.py`
Adjust debounce timing inside `TemplateHandler` if needed.

## Troubleshooting

If you encounter issues:

1. **LaTeX not found**: Follow the installation instructions above
2. **Compilation errors**: Check your LaTeX syntax in the file
3. **Permission errors**: Ensure you have write permissions in the output directory

## Customization

To add a new LaTeX file:

1. Create a new `.tex` file in the `templates/` directory
2. Follow standard LaTeX structure and styling
3. Run the script with your file name as an argument 