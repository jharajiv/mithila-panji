from io import StringIO
import io
import pandas as pd
import chromadb
import config


async def add_documents(file_data, filename):
    # This is where you would prepare your dataset, e.g., load documents, preprocess them, etc.
    chroma_client = chromadb.PersistentClient(
        config.DB_PATH
    )  # Ensure the collection is loaded

    collection = chroma_client.create_collection(name="my_collection")

    data_stream = io.BytesIO(file_data)

    df = pd.read_csv(StringIO(data_stream))

   
        
    documents = []
    metadatas = []
    ids = []
    id = 1

    for i, series in df.iterrows():
        print(f"Line read from file: {series.to_string(index=False)}")  # Debug print to check the content of each line
        if i == 0:
            continue  # Skip the header row
        line = series.to_string(index=False)  # Convert the row to a string representation
        documents.append(line)
        metadatas.append({"document_name": filename, "index": line[0]})
        ids.append(str(id))
        id += 1

    collection.add(
                ids=ids,  # Use the index as the document ID
                documents=documents,
                metadatas=metadatas
            )
    
    return {"message": "Documents loaded and indexed successfully."}


async def query_documents(query_text=None):
    chroma_client = chromadb.PersistentClient(
        config.DB_PATH
    )  # Ensure the collection is loaded
    collection = chroma_client.get_collection(name="my_collection")  # Ensure the collection is loaded
    results = collection.query(
        query_texts=[query_text],  # Chroma will embed this for you
        n_results=3,  # how many results to return
    )
    return {"results": results}
