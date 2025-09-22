#!/usr/bin/env python3
"""
Start the Personal Day Planner FastAPI server
"""

import os
import sys
import uvicorn
from main import app

if __name__ == "__main__":
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in a virtual environment!")
        print("   Recommended: Activate virtual environment first:")
        print("   Windows: venv\\Scripts\\activate")
        print("   Unix: source venv/bin/activate")
        print()
    
    print("🚀 Starting Personal Day Planner API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )