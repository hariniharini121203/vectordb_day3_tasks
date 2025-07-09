# Movie Review App with ChromaDB

## What is this project?
This is a simple web application built with Flask and ChromaDB to collect and store movie reviews. You can:
- Submit movie reviews (title, review text, rating) through a web form.
- Store reviews in a ChromaDB database running in a Docker container.
- View stored reviews in the browser.
- Measure and display three timings in the terminal:
  - Time to connect to ChromaDB.
  - Time to upload review data.
  - Time to disconnect from ChromaDB.

The app is designed to be as simple as a previous Weaviate project, with minimal setup and clear output.

## Folder Structure
```
movie_review_app/
├── templates/
│   ├── index.html       # Form to submit movie reviews
│   └── reviews.html     # Page to display stored reviews
├── flask_chromadb_app.py # Flask app code
├── docker-compose.yml    # Docker configuration for ChromaDB
└── chromadb_data/       # Folder for storing ChromaDB data (created by Docker)
```

## What does each file do?
- **flask_chromadb_app.py**: The main Flask app. It:
  - Connects to ChromaDB and prints the connection time.
  - Provides a form to submit reviews (`/`) and stores them in the "Reviews" collection, printing the upload time.
  - Displays all reviews in a table (`/reviews`).
  - Prints the disconnection time when the app stops.
- **index.html**: The web form where you enter a movie title, review text, and rating (1-5).
- **reviews.html**: A page showing all stored reviews in a table (ID, title, review text, rating).
- **docker-compose.yml**: Runs ChromaDB in a Docker container with a persistent storage folder (`chromadb_data`).

## How to set up the project
1. **Ensure you have the tools**:
   - **Python 3.10**: Install from the Python website or Microsoft Store.
   - **Docker Desktop**: Install and ensure it’s running.
   - A code editor (e.g., VS Code).

2. **Create the project folder**:
   - Make a folder called `movie_review_app`.
   - Place the `flask_chromadb_app.py`, `docker-compose.yml`, and `templates/` folder (with `index.html` and `reviews.html`) inside it.

3. **Install Python packages**:
   - Open a terminal (PowerShell) in `movie_review_app`.
   - Install Flask and ChromaDB:
     ```bash
     pip install flask chromadb
     ```
   - Update ChromaDB to avoid issues:
     ```bash
     pip install --upgrade chromadb
     ```
   - Clear ChromaDB cache (optional, if you see model download messages):
     ```bash
     rmdir /s /q "C:\Users\YourUsername\.cache\chroma"
     ```

4. **Start ChromaDB**:
   - In the `movie_review_app` folder, run:
     ```bash
     docker-compose up -d
     ```
   - Check if the ChromaDB container is running:
     ```bash
     docker ps
     ```
   - If it fails, view logs:
     ```bash
     docker logs movie_review_app_chromadb_1
     ```

## How to run the app
1. **Run the Flask app**:
   - In the `movie_review_app` folder, run:
     ```bash
     python flask_chromadb_app.py
     ```
   - The terminal will show:
     ```
     Time to connect to ChromaDB: X.XXXX seconds
     ```

2. **Use the web form**:
   - Open a browser and go to `http://localhost:5000`.
   - Enter a movie title (e.g., "Inception"), review text (e.g., "Mind-bending!"), and rating (1-5).
   - Click "Submit Review".
   - The terminal will show:
     ```
     Time to upload review data: X.XXXX seconds
     ```

3. **View stored reviews**:
   - Go to `http://localhost:5000/reviews` to see all reviews in a table.
   - Each row shows the review’s ID, title, review text, and rating.
   - Click "Back to Add Review" to return to the form.

4. **Stop the app**:
   - Press `Ctrl+C` in the terminal.
   - The terminal will show:
     ```
     Time to close ChromaDB connection: X.XXXX seconds
     ```

## How to check stored data manually
If you want to see reviews in the terminal (instead of the browser):
1. Create a file called `query_chromadb.py` in `movie_review_app`:
   ```python
   import chromadb
   import os

   client = chromadb.PersistentClient(path=os.path.abspath(os.path.join(os.getcwd(), "chromadb_data")).replace("\\", "/"))
   collection = client.get_collection("Reviews")
   results = collection.get()
   for id, meta, doc in zip(results['ids'], results['metadatas'], results['documents']):
       print(f"ID: {id}, Title: {meta['title']}, Rating: {meta['rating']}, Review: {doc}")
   ```
2. Run it:
   ```bash
   python query_chromadb.py
   ```
3. Output example:
   ```
   ID: review_1738851234, Title: Inception, Rating: 4, Review: Mind-bending!
   ID: review_1738851250, Title: The Matrix, Rating: 5, Review: Awesome sci-fi!
   ```

## How to test data persistence
- Submit a few reviews at `http://localhost:5000`.
- Stop and restart the ChromaDB container:
  ```bash
  docker-compose down
  docker-compose up -d
  ```
- Check `http://localhost:5000/reviews` or run `query_chromadb.py` to confirm reviews are still there.

## Troubleshooting
- **Slow submission**:
  - Ensure `chromadb_data` is on an SSD (move project to `D:\movie_review_app` if needed).
  - Clear `chromadb_data`:
    ```bash
    rmdir /s /q chromadb_data
    docker-compose up -d
    ```
- **App crashes or restarts**:
  - Set `debug=False` in `flask_chromadb_app.py` (line: `app.run(debug=False, port=5000)`) or use Waitress:
    ```bash
    pip install waitress
    ```
    Update `flask_chromadb_app.py`:
    ```python
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
    ```
- **Port conflicts**:
  - Check if ports 5000 or 8000 are in use:
    ```bash
    netstat -aon | findstr :5000
    netstat -aon | findstr :8000
    ```
- **Errors**:
  - Check ChromaDB logs:
    ```bash
    docker logs movie_review_app_chromadb_1
    ```

## Notes
- The app is similar to a Weaviate project, storing reviews instead of movies.
- Reviews are stored in the `chromadb_data` folder, which persists even if the Docker container restarts.
- Only three timings are printed in the terminal, in seconds (e.g., 0.2499).
- Use the browser (`/reviews`) or `query_chromadb.py` to see stored data.

If you forget how anything works, come back to this README or ask for help!
