from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch


app = FastAPI()


# Загрузка модели с поддержкой русского языка
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Заглушка: словарь постов
POSTS = {
    1: "Сегодня гулял в парке и слушал музыку — очень расслабляет.",
    2: "Посмотрел новый фильм, очень рекомендую!",
    3: "Обожаю видеоигры, особенно стратегические.",
    4: "Съездил в горы, природа невероятная!",
    5: "Новая книга по психологии дала много инсайтов.",
}


# Кэшируем эмбеддинги
post_ids = list(POSTS.keys())
post_texts = list(POSTS.values())
post_embeddings = model.encode(post_texts, convert_to_tensor=True)


# Схема входного запроса
class RecommendRequest(BaseModel):
    text: str
    top_k: int = 3


@app.get("/")
def root():
    return {"message": "POSTOJKA is running"}


@app.post("/recommend")
def recommend_posts(request: RecommendRequest):
    query_embedding = model.encode(request.text, convert_to_tensor=True)
    similarity_scores = util.cos_sim(query_embedding, post_embeddings)[0]
    top = torch.topk(similarity_scores, k=min(request.top_k, len(post_ids)))

    results = [
        {"post_id": post_ids[i], "score": round(score.item(), 3)}
        for i, score in zip(top.indices, top.values)
    ]
    return {"recommended": results}
