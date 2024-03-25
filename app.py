import streamlit as st
import requests
import json

# Streamlit 页面设置
st.title('搜索服务')
st.write('输入查询，获取相关文本。')

# 接口地址
API_URL = 'http://test18.kydev.net/rag/search_string'

# 文本类型字典
c_dict={
'01':'二级概述',
'02':'三级_症状_概述_1',
'03':'三级_优先检查_概述_1',
'04':'三级_诊断标准_概述_1',
'05':'三级_查体与体征_概述_1',
'06':'三级_问诊与症状_概述_1',
'07':'三级_体征_概述_1',
'08':'三级_查体技巧_概述_1',
'09':'三级_问诊技巧_概述_1',
'10':'三级_新检查_概述_1',
'11':'三级_风险评估和危险分层_概述_1',
'12':'三级_可选检查_概述_1',
'13':'三级_危险因素_概述_1',
'14':'三级_诱因_概述_1',
'15':'三级_症状_概述_0',
'16':'三级_优先检查_概述_0',
'17':'三级_诊断标准_概述_0',
'18':'三级_查体与体征_概述_0',
'19':'三级_问诊与症状_概述_0',
'20':'三级_体征_概述_0',
'21':'三级_查体技巧_概述_0',
'22':'三级_问诊技巧_概述_0',
'23':'三级_新检查_概述_0',
'24':'三级_风险评估和危险分层_概述_0',
'25':'三级_可选检查_概述_0',
'26':'三级_危险因素_概述_0',
'27':'三级_诱因_概述_0',
'28':'三级内容'
}

# 加载ID和文本的映射
@st.cache
def load_id_to_text_mapping():
    with open('data2.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return {item['id']: item['content'] for item in data}

id_to_text = load_id_to_text_mapping()

# 获取文本类型的函数
def get_text_type(text_id):
    type_code = str(text_id)[-5:-3]  # 获取ID的倒数第4、倒数第5位数字组成的字符串
    return c_dict.get(type_code, "未知类型")  # 从字典中查找对应的文本类型

# 创建一个文本输入框
query = st.text_input('请输入你的查询：')

# 当用户输入查询并点击按钮时
if st.button('搜索'):
    if query:  # 确保输入不为空
        # 发送请求到接口
        response = requests.post(API_URL, json={"query": query,'n':10})
        if response.status_code == 200:
            # 解析返回的ID列表
            top_ids = response.json().get('data', [])
            top_sim = response.json().get('sim', [])
            column = response.json().get('col_name', [])
            content = response.json().get('content', [])
            # 获取对应的文本和类型
            #results = [(id_to_text.get(top_ids[i], "未找到对应的文本"), get_text_type(top_ids[i]),top_sim[i]) for i in range(len(top_ids))]
            # 将结果显示在网页上
            results=[(top_ids[i],column[i],top_sim[i],content[i]) for i in range(len(top_ids))]
            for id,col1,sim,con in results:
                st.write(f"ID: {id}")
                st.write(f"类型: {col1}")
                st.write(f"相似度:{sim}")
                st.write(f"文本: {con}")
                st.write("")  # 添加空行以分隔不同的结果
        else:
            st.error(f'查询失败，状态码：{response.status_code}')
    else:
        st.error('查询字符串不能为空！')
