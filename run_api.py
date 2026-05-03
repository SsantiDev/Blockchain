import uvicorn
import os
import sys

# Ensure the root directory is in sys.path for internal imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting NotaryChain Commercial Server...")
    print("Architecture: Clean Architecture (SOLID)")
    print("Environment: Development")
    
    uvicorn.run(
        "src.api.server:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=True
    )
