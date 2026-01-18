# run.py

#!/usr/bin/env python
import sys
import uvicorn


def run_dev():
    print("🚀 Starting SocialHub Backend - Development Mode")
    print("📍 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


def run_prod():
    print("🚀 Starting SocialHub Backend - Production Mode")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="warning"
    )


def run_tests():
    print("🧪 Running tests...")
    import pytest
    sys.exit(pytest.main(["-v", "tests/"]))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--prod":
            run_prod()
        elif arg == "--test":
            run_tests()
        else:
            print(f"Unknown: {arg}. Use: python run.py [--prod|--test]")
    else:
        run_dev()