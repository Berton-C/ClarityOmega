import uuid
import chromadb

CLIENT = chromadb.PersistentClient(path="./chroma_db")
COLLECTION = CLIENT.get_or_create_collection(
    name="memories",
    embedding_function=None
)

def remember(content, embedding, time, weight=1.0):
    if not isinstance(content, str):
        raise TypeError("content must be a str")
    if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
        raise TypeError("embedding must be a list of floats")
    item_id = str(uuid.uuid4())
    COLLECTION.add(
        ids=[item_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[{"time": time, "weight": float(weight)}],
    )
    return item_id

def reinforce(item_id, boost=0.1, cap=3.0):
    if not isinstance(item_id, str):
        raise TypeError("item_id must be a str")
    result = COLLECTION.get(ids=[item_id], include=["metadatas"])
    if not result["ids"]:
        return None
    meta = result["metadatas"][0]
    current_weight = float(meta.get("weight", 1.0))
    new_weight = min(current_weight + boost, cap)
    meta["weight"] = new_weight
    COLLECTION.update(ids=[item_id], metadatas=[meta])
    return new_weight

def decay_all(factor=0.95, baseline=1.0):
    all_items = COLLECTION.get(include=["metadatas"])
    for i, item_id in enumerate(all_items["ids"]):
        meta = all_items["metadatas"][i]
        w = float(meta.get("weight", 1.0))
        new_w = baseline + (w - baseline) * factor
        meta["weight"] = new_w
        COLLECTION.update(ids=[item_id], metadatas=[meta])

def forget_ids(item_ids):
    if not isinstance(item_ids, list) or not all(isinstance(x, str) for x in item_ids):
        raise TypeError("item_ids must be a list of str")
    if not item_ids:
        return []
    COLLECTION.delete(ids=item_ids)
    return item_ids

def forget_id(item_id):
    if not isinstance(item_id, str):
        raise TypeError("item_id must be a str")
    forget_ids([item_id])
    return item_id

def query(query_embedding, k):
    res = query_with_ids(query_embedding, k)
    return [[t, c] for _, t, c, _ in res]

def query_with_ids(query_embedding, k):
    if not isinstance(query_embedding, list) or not all(isinstance(x, (int, float)) for x in query_embedding):
        raise TypeError("query_embedding must be a list of floats")
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be > 0")
    fetch_k = min(k * 3, k + 20)
    res = COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=fetch_k,
        include=["documents", "metadatas", "distances"],
    )
    ids = res["ids"][0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    scored = []
    for i in range(len(ids)):
        t = metas[i].get("time") if metas[i] else None
        w = float(metas[i].get("weight", 1.0)) if metas[i] else 1.0
        similarity = 1.0 / (1.0 + dists[i]) if dists[i] is not None else 0.5
        effective = similarity * w
        scored.append((effective, ids[i], t, docs[i], w))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [[sid, st, sd, sw] for _, sid, st, sd, sw in scored[:k]]
