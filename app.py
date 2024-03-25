import streamlit as st
import requests
import json
import re
# Streamlit 页面设置
st.title('搜索服务')
st.write('输入查询，获取相关文本。')

# 接口地址
API_URL = 'http://test18.kydev.net/rag/search_string'

# 文本类型字典
# c_dict={
# '01':'二级概述',
# '02':'三级_症状_概述_1',
# '03':'三级_优先检查_概述_1',
# '04':'三级_诊断标准_概述_1',
# '05':'三级_查体与体征_概述_1',
# '06':'三级_问诊与症状_概述_1',
# '07':'三级_体征_概述_1',
# '08':'三级_查体技巧_概述_1',
# '09':'三级_问诊技巧_概述_1',
# '10':'三级_新检查_概述_1',
# '11':'三级_风险评估和危险分层_概述_1',
# '12':'三级_可选检查_概述_1',
# '13':'三级_危险因素_概述_1',
# '14':'三级_诱因_概述_1',
# '15':'三级_症状_概述_0',
# '16':'三级_优先检查_概述_0',
# '17':'三级_诊断标准_概述_0',
# '18':'三级_查体与体征_概述_0',
# '19':'三级_问诊与症状_概述_0',
# '20':'三级_体征_概述_0',
# '21':'三级_查体技巧_概述_0',
# '22':'三级_问诊技巧_概述_0',
# '23':'三级_新检查_概述_0',
# '24':'三级_风险评估和危险分层_概述_0',
# '25':'三级_可选检查_概述_0',
# '26':'三级_危险因素_概述_0',
# '27':'三级_诱因_概述_0',
# '28':'三级内容'
# }

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
c_dict = {
    '词条名': '99',
    '一级': '98',
    '二级': '97',
    '二级概述': '01',
    '三级_x_概述_1': ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14'],
    '三级_x_概述_0': ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27'],
    '三级内容': '28'
}
def standardize_category1(category):
    return re.sub(r'三级_(.+?)_概述_1', r'三级_x_概述_1', category)
def standardize_category2(category):
    return re.sub(r'三级_(.+?)_概述_0', r'三级_x_概述_0', category)
query = st.text_input('请输入你的查询：')
number = st.number_input('请输入召回数目(1-50)', min_value=1, max_value=50, value=20)

# 创建复选框让用户选择展示哪些列
options = list(c_dict.keys())
selected_options = st.multiselect('选择展示的类别：', options)

# 当用户输入查询并点击按钮时
if st.button('搜索'):
    if query:  # 确保输入不为空
        # 发送请求到接口
        response = requests.post(API_URL, json={"query": query, 'n': number})
        if response.status_code == 200:
            # 解析返回的数据列表
            top_ids = response.json().get('data', [])
            top_sim = response.json().get('sim', [])
            column = response.json().get('col_name', [])
            content = response.json().get('content', [])

            # 将结果按照用户选择的类别筛选
            filtered_results = []
            for i in range(len(top_ids)):
                col1 = column[i]
                standardized = standardize_category2(standardize_category1(col1))
                # 检查当前列是否在用户选择的选项中
                if standardized in selected_options:
                    filtered_results.append((top_ids[i], col1, top_sim[i], content[i]))
                        

            # 将筛选后的结果显示在网页上
            for id, col1, sim, con in filtered_results:
                st.write(f"ID: {id}")
                st.write(f"类型: {col1}")
                st.write(f"相似度:{sim}")
                st.write(f"文本: {con}")
                st.write("")  # 添加空行以分隔不同的结果
        else:
            st.error(f'查询失败，状态码：{response.status_code}')
    else:
        st.error('查询字符串不能为空！')
