from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


app = FastAPI()


# Загружаем модель
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Заглушка: посты
POSTS = {
    1: "Сегодня гулял в парке и слушал музыку — очень расслабляет.",
    2: "Посмотрел новый фильм, очень рекомендую!",
    3: "Обожаю видеоигры, особенно стратегические.",
    4: "Съездил в горы, природа невероятная!",
    5: "Новая книга по психологии дала много инсайтов.",
}


# Храним id и текст
post_ids = list(POSTS.keys())
post_texts = list(POSTS.values())


# Эмбеддинги
embeddings = model.encode(post_texts, convert_to_numpy=True, normalize_embeddings=True).astype("float32")


# FAISS: строим индекс
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)


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
