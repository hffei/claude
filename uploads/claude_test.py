import requests

data = {
    "q": "这个文件讲的是什么",
    "key": "",  # 密钥
}

files = {
    'file': ('中文.pdf', open('中文.pdf', 'rb'))
}
url = "http://23.224.232.204/claude_api"
resp = requests.post(url, data=data, files=files)               # 第一次上传文件，要传files
print(resp.json())


id = resp.json()['id']
conversation_id = resp.json()['conversation_id']                # 获取之前聊天记录的id


data = {
    "q": "之前文件的名字是什么",
    "key": "",  # 密钥
    "id": id,
    "conversation_id": conversation_id
}

url = "http://23.224.232.204/claude_api"
resp = requests.post(url, data=data)               # 再次进入之前聊天记录的时候可以不用传files，但是要传id和conversation_id
print(resp.json())


