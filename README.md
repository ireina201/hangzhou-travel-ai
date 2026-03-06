# 🌸 杭州智能旅游规划助手

基于 AI + 高德地图的个性化旅游规划 Web 应用

## 🎯 项目简介
本项目使用大语言模型（智谱 AI）和高德地图 API，为用户生成个性化的杭州旅游行程。用户可自定义游玩天数、预算和偏好，AI 会自动生成详细的日程安排。

## ✨ 功能特点
- 🤖 AI 智能生成个性化行程
- 📅 支持 1-5 天灵活规划
- 💰 经济型/中等/豪华型预算选择
-  简洁美观的 Streamlit 界面
- ️ 可集成高德地图计算路线距离

## 🛠️ 技术栈
- **后端**: Python, ZhipuAI API, 高德地图 API
- **前端**: Streamlit
- **部署**: Streamlit Cloud, GitHub
- **其他**: JSON, Requests, python-dotenv

## 🚀 在线演示
访问：https://hangzhou-travel-ai.streamlit.app

## 📦 本地运行
```bash
# 1. 克隆仓库
git clone https://github.com/ireina201/hangzhou-travel-ai.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key（创建 .streamlit/secrets.toml）
ZHIPU_API_KEY = "你的智谱 Key"
AMAP_KEY = "你的高德 Key"

# 4. 运行应用
streamlit run app.py
