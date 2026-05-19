from io import StringIO
import io
import pandas as pd
import chromadb
import config
import traceback


# This is where you would prepare your dataset, e.g., load documents, preprocess them, etc.
chroma_client = chromadb.PersistentClient(
        config.DB_PATH
    )  # Ensure the collection is loaded

async def add_new_document(file_data, filename, collection_name="my_collection"):
    
    collection = chroma_client.get_or_create_collection(name=collection_name)

    #data_stream = io.BytesIO(file_data)

    df = pd.read_csv(StringIO(file_data))

    documents = []
    metadatas = []
    ids = []
    id = 1

    for i, series in df.iterrows():
        #print(f"Line read from file: {series.to_string(index=False)}")  # Debug print to check the content of each line
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

async def query_uploaded_documents(query_text=None):
     # Ensure the collection is loaded
    collection = chroma_client.get_collection(name="my_collection")  # Ensure the collection is loaded
    results = collection.query(
        query_texts=[query_text],  # Chroma will embed this for you
        n_results=3,  # how many results to return
    )
    return {"results": results}

async def load_panji_database():

    try:
        for file in config.PANJI_FILES_PATH:
            with open(file, "r") as f:
                file_data = f.read()
                filename = file.split("/")[-1]  # Extract the filename from the path
                await add_new_document(file_data=file_data, filename=filename, collection_name="panji_docs_collection")
        
        return {"message": "Panji database loaded and indexed successfully."}
    except Exception as e:
        print(f"Error loading Panji database: {e, traceback.format_exc()}")
        raise {"error": f"Error loading Panji database: {e}"}


async def query_panji_database(query_text=None):
    collection = None
    chroma_client.list_collections()  # List collections to ensure the client is working
    try:
        collection = chroma_client.get_collection(name="panji_docs_collection")  # Try to get the collection
        
    except Exception as e:
        print(f"Error accessing Panji collection: {e}")
        
    if collection:
        print("Collection loaded successfully.")
        
    else:
        print("ReLoading the database...")
        await load_panji_database()  # Load the Panji database before querying
        collection = chroma_client.get_collection(name="panji_docs_collection")
    
    results = collection.query(
        query_texts=[query_text],  # Chroma will embed this for you
        n_results=5,  # how many results to return
    )
      # Ensure changes are saved to disk
    return {"results": results}
