from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
from load_posts import load_posts
import psycopg2

app = FastAPI()


# Загружаем модель
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


posts = load_posts()
post_ids = list(posts.keys())
post_texts = list(posts.values())


embeddings = model.encode(
    post_texts,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype("float32")


index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)


@app.on_event("startup")
def startup_event():
    print(f"Loaded {len(posts)} posts into FAISS index.")


# Запрос
class RecommendRequest(BaseModel):
    text: str
    top_k: int = 3


@app.post("/recommend")
def recommend_posts(request: RecommendRequest):
    query_vector = model.encode(request.text, convert_to_numpy=True, normalize_embeddings=True).astype("float32").reshape(1, -1)

    distances, indices = index.search(query_vector, k=min(request.top_k, len(post_ids)))

    results = []
    for idx, score in zip(indices[0], distances[0]):
        post_id = post_ids[idx]
        results.append({"post_id": post_id, "score": round(float(score), 3)})

    return {"recommended": results}


@app.post("/reindex")
def reindex():
    global index, post_ids
    posts = load_posts()
    post_ids = list(posts.keys())
    texts = list(posts.values())

    embeddings = model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return {"message": f"Reindexed {len(posts)} posts."}
