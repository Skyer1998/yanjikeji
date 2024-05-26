import requests
import json
from flask import Flask, request, render_template, jsonify

API_KEY = "hd8DzXIj9P4cGFgrpAtIUYY3"
SECRET_KEY = "Po4VDPKya4jZ7TBBggisHssMzy4gYOHt"

messages = []
app = Flask(__name__)


def main(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": text,
        "temperature": 0.2,
        "top_p": 0.8,
        "penalty_score": 1,
        "disable_search": False,
        "enable_citation": False,
        "response_format": "text"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    result_content = data['result']
    print(result_content)
    return result_content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
def add_user_message(content):
    """将用户消息添加到messages列表中。"""
    messages.append({"role": "user", "content": content})
def add_assistant_message(content):
    """将助手（大模型）消息添加到messages列表中。"""
    messages.append({"role": "assistant", "content": content})

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    add_user_message(user_input)
    text = main(messages)
    add_assistant_message(text)
    return jsonify({"assistant_message": text})

if __name__ == '__main__':
    add_user_message('我希望你帮我生成一份民间借贷起诉状，一个问题一个问题的问，一次只问一个要素，要素收集齐全后生成起诉状')
    add_assistant_message("好的")
    app.run(debug=True)