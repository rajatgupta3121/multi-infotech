from app import create_app

# Create the Flask application instance
app = create_app()

# Expose the app for WSGI servers
if __name__ == "__main__":
    app.run()