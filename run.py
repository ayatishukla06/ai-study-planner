import os
from app import create_app  # Imports your factory function

# 1. Initialize the actual server instance
server_app = create_app()

if __name__ == "__main__":
    # Render sets the PORT environment variable dynamically
    port = int(os.environ.get("PORT", 5000))
    # 2. Call .run() on 'server_app', not the folder 'app'
    server_app.run(host="0.0.0.0", port=port)