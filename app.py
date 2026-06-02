from flask import Flask
app=Flask(__name__)
@app.route('/')
def home(): return 'Cincinnati Lodge AI'
if __name__ == "__main__":
    app.run(debug=True)