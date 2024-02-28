from flask import Flask, request, render_template, session, Response, jsonify
import requests
# from werkzeug.utils import secure_filename
import os
from openai import OpenAI
from dotenv import load_dotenv


# 引入环境变量
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 删除文件
file_id = "cneb20mcp7f0ud9jevt0"
client.files.delete(file_id=file_id)
