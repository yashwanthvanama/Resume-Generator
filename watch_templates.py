#!/usr/bin/env python3
"""
File watcher script that monitors the templates folder and automatically
compiles resumes when .tex files are modified.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TemplateHandler(FileSystemEventHandler):
    def __init__(self, templates_dir, src_dir):
        self.templates_dir = Path(templates_dir)
        self.src_dir = Path(src_dir)
        self.compile_script = self.src_dir / "compile_resume.py"
        self.last_modified = {}  # Track last modification times
        self.debounce_seconds = 1.0  # Wait time to avoid duplicate events
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Only process .tex files
        if file_path.suffix == '.tex':
            # Debounce: avoid duplicate events from the same file
            current_time = time.time()
            last_time = self.last_modified.get(str(file_path), 0)
            
            if current_time - last_time < self.debounce_seconds:
                return  # Skip this event as it's too soon after the last one
            
            self.last_modified[str(file_path)] = current_time
            
            # Small delay to ensure file is fully written
            time.sleep(0.1)
            
            print(f"Detected save in: {file_path.name}")
            self.compile_resume(file_path)
    
    def compile_resume(self, tex_file):
        """Compile the resume using compile_resume.py"""
        try:
            print(f"Compiling {tex_file.name}...")
            
            # Run compile_resume.py with the modified template
            cmd = [sys.executable, str(self.compile_script), str(tex_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Successfully compiled {tex_file.name}")
                if result.stdout:
                    print(f"Output: {result.stdout}")
            else:
                print(f"❌ Error compiling {tex_file.name}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                    
        except Exception as e:
            print(f"❌ Exception while compiling {tex_file.name}: {e}")

def main():
    # Get the script directory
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    src_dir = script_dir / "src"
    
    # Verify directories exist
    if not templates_dir.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        sys.exit(1)
        
    if not src_dir.exists():
        print(f"❌ Source directory not found: {src_dir}")
        sys.exit(1)
        
    compile_script = src_dir / "compile_resume.py"
    if not compile_script.exists():
        print(f"❌ Compile script not found: {compile_script}")
        sys.exit(1)
    
    print(f"📁 Watching templates directory: {templates_dir}")
    print(f"🔧 Using compile script: {compile_script}")
    print("🚀 Starting file watcher... (Press Ctrl+C to stop)")
    print("💾 Will compile when you save changes to .tex files")
    
    # Set up the file watcher
    event_handler = TemplateHandler(templates_dir, src_dir)
    observer = Observer()
    observer.schedule(event_handler, str(templates_dir), recursive=False)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping file watcher...")
        observer.stop()
    
    observer.join()
    print("✅ File watcher stopped.")

if __name__ == "__main__":
    main()
