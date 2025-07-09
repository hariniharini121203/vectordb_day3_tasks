from flask import Flask, render_template, request, redirect
import chromadb
import time
import os

app = Flask(__name__)

# Measure time to connect to ChromaDB
data_path = os.path.abspath(os.path.join(os.getcwd(), "chromadb_data")).replace("\\", "/")
start_connect_time = time.time()
client = chromadb.PersistentClient(path=data_path)
# Cache collection to avoid repeated get/create calls
try:
    collection = client.get_collection("Reviews")
except:
    collection = client.create_collection("Reviews", embedding_function=None)
connect_time = time.time() - start_connect_time
print(f"Time to connect to ChromaDB: {connect_time:.4f} seconds")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_review', methods=['POST'])
def add_review():
    try:
        # Get form data
        title = request.form['title']
        review_text = request.form['review_text']
        rating = int(request.form['rating'])

        # Measure time to upload data
        start_upload_time = time.time()
        collection.add(
            documents=[review_text],
            metadatas=[{"title": title, "rating": rating}],
            ids=[f"review_{int(time.time())}"]
        )
        upload_time = time.time() - start_upload_time
        print(f"Time to upload review data: {upload_time:.4f} seconds")

        return redirect('/')
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/reviews')
def list_reviews():
    try:
        # Retrieve all reviews
        results = collection.get()
        reviews = [
            {"id": id, "title": meta["title"], "rating": meta["rating"], "review_text": doc}
            for id, meta, doc in zip(results['ids'], results['metadatas'], results['documents'])
        ]
        return render_template('reviews.html', reviews=reviews)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    try:
        app.run(debug=True, port=5000)
    finally:
        # Measure time to close connection
        start_close_time = time.time()
        client = None
        close_time = time.time() - start_close_time
        print(f"Time to close ChromaDB connection: {close_time:.4f} seconds")