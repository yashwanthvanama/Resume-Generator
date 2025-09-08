#!/bin/bash
# Activation script for Resume Generator virtual environment
# 
# IMPORTANT: This script must be SOURCED, not executed directly.
# Use: source activate_env.sh
# or: . activate_env.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment 'venv' not found!"
    echo "Please run 'python -m venv venv' first."
    return 1
fi

echo "Activating Resume Generator virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Warning: Ollama is not installed or not in PATH."
    echo "   To install Ollama, visit: https://ollama.ai"
    echo "   Job analyzer functionality will not work without Ollama."
    echo ""
else
    echo "🤖 Checking Ollama status..."
    
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "🚀 Starting Ollama server..."
        # Start Ollama in the background
        ollama serve > /dev/null 2>&1 &
        OLLAMA_PID=$!
        
        # Wait a moment for Ollama to start
        sleep 3
        
        # Check if it started successfully
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            echo "✅ Ollama server started successfully (PID: $OLLAMA_PID)"
        else
            echo "❌ Failed to start Ollama server"
        fi
    else
        echo "✅ Ollama server is already running"
    fi
    
    # Check if LLaMA 3.1 is available
    if curl -s http://localhost:11434/api/tags | grep -q "llama3.1"; then
        echo "✅ LLaMA 3.1 model is available"
    else
        echo "📥 LLaMA 3.1 model not found. Pulling it now..."
        ollama pull llama3.1
        if [ $? -eq 0 ]; then
            echo "✅ LLaMA 3.1 model downloaded successfully"
        else
            echo "❌ Failed to download LLaMA 3.1 model"
        fi
    fi
    echo ""
fi

echo "To deactivate, run: deactivate"
echo "To install dependencies: pip install -r requirements.txt"
echo "To run the resume compiler: python src/compile_resume.py"
echo "To analyze a job and compile resume: python src/job_analyzer.py <job_url>" 