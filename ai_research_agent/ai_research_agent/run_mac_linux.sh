#!/bin/bash
echo "========================================"
echo "  AI Research Agent - Setup & Launch"
echo "========================================"
echo ""

echo "[1/3] Installing Python dependencies..."
pip install -r requirements.txt
echo ""

echo "[2/3] Checking Ollama..."
ollama list
echo ""

echo "[3/3] Launching Streamlit app..."
echo "Open your browser at: http://localhost:8501"
echo ""
streamlit run app.py
