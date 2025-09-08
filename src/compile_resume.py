
import subprocess
import os
import shutil
import sys
from pathlib import Path

def check_latex_installation():
    """
    Check if LaTeX is installed and available.
    
    Returns:
        bool: True if LaTeX is available, False otherwise
    """
    try:
        result = subprocess.run(["xelatex", "--version"], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def compile_latex(tex_file, output_dir):
    """
    Compile a LaTeX file and save the output PDF to the specified directory.
    
    Args:
        tex_file (str): Path to the LaTeX file
        output_dir (str): Directory to save the output PDF
    """
    # Check if LaTeX is installed
    if not check_latex_installation():
        print("Error: LaTeX is not installed or not available in PATH.")
        print("\nTo install LaTeX on macOS, run one of these commands:")
        print("  brew install --cask basictex    # Lighter installation (~100MB)")
        print("  brew install --cask mactex       # Full installation (~4GB)")
        print("\nAfter installation, restart your terminal or run:")
        print("  eval \"$(/usr/libexec/path_helper)\"")
        print("\nIf you installed BasicTeX (lighter version), you'll need to install additional packages:")
        print("  sudo tlmgr update --self")
        print("  sudo tlmgr install enumitem titlesec hyperref xcolor fontspec")
        return False
    
    # Get the directory containing the tex file
    tex_dir = os.path.dirname(tex_file)
    tex_filename = os.path.basename(tex_file)
    tex_name_without_ext = os.path.splitext(tex_filename)[0]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Change to the directory containing the tex file
        original_dir = os.getcwd()
        os.chdir(tex_dir)
        
        # Run xelatex twice for references and formatting (better font support)
        print(f"Compiling {tex_filename}...")
        subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename], 
                      check=True, capture_output=True, text=True)
        subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename], 
                      check=True, capture_output=True, text=True)
        
        # Move the generated PDF to the output directory
        pdf_source = f"{tex_name_without_ext}.pdf"
        pdf_destination = os.path.join(output_dir, f"{tex_name_without_ext}.pdf")
        
        if os.path.exists(pdf_source):
            shutil.move(pdf_source, pdf_destination)
            print(f"PDF successfully generated: {pdf_destination}")
        else:
            print("Error: PDF was not generated")
            return False
            
        # Clean up auxiliary files
        auxiliary_extensions = ['.aux', '.log', '.out', '.toc', '.fls', '.fdb_latexmk']
        for ext in auxiliary_extensions:
            aux_file = f"{tex_name_without_ext}{ext}"
            if os.path.exists(aux_file):
                os.remove(aux_file)
                print(f"Cleaned up: {aux_file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error compiling LaTeX: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def list_available_templates():
    """List all available templates in the templates directory."""
    project_root = Path(__file__).parent.parent
    templates_dir = project_root / "templates"
    
    if not templates_dir.exists():
        print("Error: Templates directory not found!")
        return []
    
    templates = []
    for file in templates_dir.glob("*.tex"):
        templates.append(file.stem)
    
    return sorted(templates)

def main():
    # Define paths
    project_root = Path(__file__).parent.parent
    templates_dir = project_root / "templates"
    output_dir = project_root / "output"
    
    # Check command line arguments
    if len(sys.argv) > 1:
        template_name = sys.argv[1]
        # Add .tex extension if not provided
        if not template_name.endswith('.tex'):
            template_name += '.tex'
        tex_file = templates_dir / template_name
    else:
        # Show available templates and ask user to choose
        templates = list_available_templates()
        if not templates:
            print("Error: No templates found in templates/ directory!")
            return
        
        print("Available templates:")
        for i, template in enumerate(templates, 1):
            print(f"  {i}. {template}")
        
        try:
            choice = int(input("\nEnter the number of the template to compile (or 0 to exit): "))
            if choice == 0:
                return
            if 1 <= choice <= len(templates):
                template_name = templates[choice - 1] + '.tex'
                tex_file = templates_dir / template_name
            else:
                print("Invalid choice!")
                return
        except (ValueError, KeyboardInterrupt):
            print("\nExiting...")
            return
    
    # Check if the tex file exists
    if not tex_file.exists():
        print(f"Error: Template file not found at {tex_file}")
        print(f"Available templates: {', '.join(list_available_templates())}")
        return
    
    # Compile the resume
    success = compile_latex(str(tex_file), str(output_dir))
    
    if success:
        print("Resume compilation completed successfully!")
    else:
        print("Resume compilation failed!")

if __name__ == "__main__":
    main()
