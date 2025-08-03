import json
import os

SAVE_FILE = "users_save.json"

def load_users():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_users(users):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def save_user(username, user_data):
    users = load_users()
    users[username] = user_data
    save_users(users)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": password,
        "current_level": 0,
        "last_level_info": {},
        "mistake_book": {
            "chapter1": {},
            "chapter2": {},
            "chapter3": {},
            "chapter4": {},
            "chapter5": []
        }
    }
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    u = users.get(username)
    return u and u["password"] == password

def update_progress(username, lvl, hero=None, score=None, time_sec=None):
    users = load_users()
    u = users.get(username)
    if lvl > u["current_level"]:
        u["current_level"] = lvl
    if lvl == 5 and hero and score is not None and time_sec is not None:
        if not u["last_level_info"] or u["last_level_info"]["score"] < score:
            u["last_level_info"] = {
                "hero": hero,
                "score": score,
                "time_seconds": time_sec
            }
    save_users(users)
    return True

def get_current_level(username):
    u = load_users().get(username)
    return u["current_level"] if u else 0

def update_mistake_book1234(username, chapter, q, user_ans, correct_ans):
    users = load_users()
    user = users.get(username)
    user["mistake_book"][chapter][q] = {
        "user_answer": user_ans,
        "correct_answer": correct_ans
    }
    save_users(users)

def update_mistake_book5(username, chapter, q, path, input_hp, opt_path, opt_hp):
    users = load_users()
    user = users.get(username)
    user["mistake_book"][chapter].append({
        "question": q,
        "user_path": path,
        "user_hp": input_hp,
        "optimal_path": opt_path,
        "optimal_hp": opt_hp
    })
    save_users(users)

def load_rank_data():
    if not os.path.exists("users_save.json"):
        return []
    with open("users_save.json", "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return []

    ranks = []
    for name, info in users.items():
        # Only users who complete full 5 chapters can be shown
        if info.get("current_level") == 5 and info.get("last_level_info"):
            final = info["last_level_info"]
            ranks.append({
                "username": name,
                "hero": final.get("hero", "Unknown"),
                "score": final.get("score", 0),
                "time": final.get("time_seconds", 9999)
            })
    # First sort in score, if score is equal then sort in time.
    return sorted(ranks, key=lambda x: (-x["score"], x["time"]))
