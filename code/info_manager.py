import json
import os

SAVE_FILE = "users_save.json"

# 加载所有用户数据
def load_users():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ 用户数据文件损坏，已重置为空。")
        return {}


# 保存所有用户数据
def save_users(users):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def save_user(username, user_data):
    if not os.path.exists(SAVE_FILE):
        users = {}
    else:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    users[username] = user_data
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# 注册新用户（判断用户名是否已存在）
def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": password,
        "current_level": 0,
        "last_level_info": {},
        "mistake_book":{
            "chapter1":{},
            "chapter2":{},
            "chapter3":{},
            "chapter4":{},
            "chapter5":{}
        }
    }
    save_users(users)
    return True

# 登录验证
def login_user(username, password):
    users = load_users()
    user = users.get(username)
    if not user or user["password"] != password:
        return False

    return True

# 更新关卡信息，通关5关时记录最后一关信息
def update_progress(username, current_level, hero_name=None, score=None, time_seconds=None):
    users = load_users()
    user = users.get(username)
    if current_level > user["current_level"]:
        user["current_level"] = current_level
    if (current_level == 5 and hero_name and score is not None and time_seconds is not None and
            (not user["last_level_info"] or user["last_level_info"]["score"] < score)):
        user["last_level_info"] = {
            "hero": hero_name,
            "score": score,
            "time_seconds": time_seconds
        }
    save_users(users)
    return True

def get_current_level(username):
    users = load_users()
    user = users.get(username)
    return user["current_level"]

# For chapter 1, 2, 3
def update_mistake_book123(username, chapter, question, user_answer, correct_answer):
    users = load_users()
    user = users.get(username)
    user["mistake_book"][chapter][question] = {
        "user_answer": user_answer,
        "correct_answer": correct_answer
    }
    save_users(users)

# # 获取通关后的最后一关信息
# def get_final_level_info(username):
#     users = load_users()
#     user = users.get(username)
#     if not user:
#         print("❌ 用户不存在。")
#         return None
#     if user["current_level"] < 5:
#         print(f"⚠️ 用户 {username} 尚未通关全部 5 关。")
#         return None
#     return user["last_level_info"]

