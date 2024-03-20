import streamlit as st
import requests
import json

# Streamlit 页面设置
st.title('搜索服务')
st.write('输入查询，获取相关文本。')

# 接口地址
API_URL = 'http://test18.kydev.net/rag/search_string'

# 加载ID和文本的映射
@st.cache
def load_id_to_text_mapping():
    with open('your_json_file.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return {item['id']: item['content'] for item in data}

id_to_text = load_id_to_text_mapping()

# 创建一个文本输入框
query = st.text_input('请输入你的查询：')

# 当用户输入查询并点击按钮时
if st.button('搜索'):
    if query:  # 确保输入不为空
        # 发送请求到接口
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            # 解析返回的ID列表
            top_ids = response.json().get('data', [])
            # 获取对应的文本
            results = [id_to_text.get(i, "未找到对应的文本") for i in top_ids]
            # 将结果显示在网页上
            for result in results:
                st.write(result)
        else:
            st.error(f'查询失败，状态码：{response.status_code}')
    else:
        st.error('查询字符串不能为空！')
