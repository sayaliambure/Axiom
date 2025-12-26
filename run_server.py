#!/usr/bin/env python3
"""
Convenience script to run the AXIOM API server.

Usage:
    python run_server.py
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

