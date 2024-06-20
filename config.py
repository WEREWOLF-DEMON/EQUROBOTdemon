
# --------------M----------------------------------

import os
from os import getenv
# ---------------R---------------------------------
API_ID = int(os.environ.get("API_ID", "16874790"))
# ------------------------------------------------
API_HASH = os.environ.get("API_HASH", "46aa49adca0f1d184eb2a2f4a48a1df9")
# ----------------D--------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7109817776:AAFG1MI-eRurvUOgOQOZkvcMo_9ksYQgfWE")
# -----------------A-------------------------------
BOT_USERNAME = os.environ.get("BOT_USERNAME", "EQUROBOT")
# ------------------X------------------------------
OWNER_ID = int(os.environ.get("OWNER_ID", "7427691214"))

EVAL = list(map(int, getenv("EVAL", "7427691214 7091230649").split()))
# ------------------X------------------------------
DEEP_API = os.environ.get("DEEP_API", "bf9ee957-9fad-46f5-a403-3e96ca9004e4")
# ------------------------------------------------
LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1002050666864"))
# ------------------------------------------------
GPT_API = os.environ.get("GPT_API", "sk-proj-mVFcWVTW1tWBxlZd79WQT3BlbkFJsQTe0GyIm1tHg3IRtL9c")
# ------------------------------------------------
DAXX_API = os.environ.get("DAXX_API", "5163c49d-b696-47f1-8cf9-")
