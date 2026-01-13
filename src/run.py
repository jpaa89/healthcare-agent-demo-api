import os
from pathlib import Path

import dotenv
import uvicorn

if __name__ == "__main__":

    dotenv.load_dotenv()

    src_dir = str(Path(__file__).resolve().parent)

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", default="localhost"),
        port=int(os.getenv("PORT", default=8000)),
        reload=True,
        reload_dirs=[src_dir],
        app_dir=src_dir,
    )
