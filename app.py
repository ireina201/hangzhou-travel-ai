import streamlit as st
import json
import re
import os
import sniffio
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 尝试从 Secrets 读取（云端）
try:
    ZHIPU_API_KEY = st.secrets["ZHIPU_API_KEY"]
    AMAP_KEY = st.secrets["AMAP_KEY"]
except:
    # 本地备用：从 .env 读取
    load_dotenv()
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
    AMAP_KEY = os.getenv("AMAP_KEY")

# 检查 API Key 是否存在
if not ZHIPU_API_KEY:
    st.error("❌ 未找到智谱 API Key")
    st.stop()

# 初始化智谱 AI 客户端
client = ZhipuAI(api_key=ZHIPU_API_KEY)

# 调用 AI 生成行程
def generate_travel_plan(days, budget, preference):
    prompt = f"""你是一名专业的杭州旅游规划师。请生成一份{days}天的杭州旅游行程，预算{budget}，偏好：{preference}。

请严格按照以下 JSON 数组格式输出（不要有任何额外文字）：

[
  {{
    "day": 1,
    "time_slot": "上午",
    "activity": "活动名称",
    "location": "地点名称",
    "reason": "推荐理由"
  }},
  {{
    "day": 1,
    "time_slot": "下午",
    "activity": "活动名称",
    "location": "地点名称",
    "reason": "推荐理由"
  }}
]

要求：
1. 按天划分行程，每天包含上午/下午/晚上活动
2. 每个活动注明地点名称和推荐理由
3. 必须输出 JSON 数组格式，不要有其他文字"""
    
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 解析 JSON
def parse_travel_plan(json_string):
    try:
        match = re.search(r'\[\s*\{.*\}\s*\]', json_string, re.DOTALL)
        if match:
            json_string = match.group()
        data = json.loads(json_string)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get('itinerary', [])
        return []
    except Exception as e:
        print(f"解析错误：{e}")
        return []

# Streamlit 界面
st.set_page_config(page_title="杭州智能旅游规划助手", page_icon="🌸")
st.title("🌸 杭州智能旅游规划助手")
st.markdown("基于 AI+ 高德地图，为你生成个性化杭州行程")

# 侧边栏
with st.sidebar:
    st.header("旅游偏好")
    days = st.slider("游玩天数", 1, 5, 3)
    budget = st.selectbox("预算", ["经济型", "中等", "豪华型"])
    preference = st.text_area("其他偏好", "喜欢历史文化，带父母")
    generate_btn = st.button("生成行程", type="primary")

# 主界面
if generate_btn:
    with st.spinner("🤖 AI 正在规划中..."):
        raw_text = generate_travel_plan(days, budget, preference)
        itinerary = parse_travel_plan(raw_text)
        
        if itinerary:
            st.success("✅ 行程生成成功！")
            
            # 遍历展示每个行程
            for item in itinerary:
                day = item.get('day', '?')
                time_slot = item.get('time_slot', item.get('time', '全天'))
                activity = item.get('activity', '未知活动')
                location = item.get('location', '未知地点')
                reason = item.get('reason', '暂无说明')
                
                with st.expander(f"第{day}天 {time_slot} - {activity}"):
                    st.write(f"**地点**：{location}")
                    st.write(f"**理由**：{reason}")
        else:

            st.error("❌ 解析失败，请重试")
