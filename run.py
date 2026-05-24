from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True is a lifesaver: it restarts the server every time you save a file
    app.run(debug=True)
    