# AI 应用开发路线
目标：2027成为可面试的AI应用开发/Python 后端

## 当前项目
知识卡片工具：命令行增删查->SQLite->FastAPI->LLM摘要。

## 技术栈

- Python 3.12+
- Pytest
- 后续:SQlite、FastAPI、Docker

## 目录

```text
ai-app-roadmap/
|- src/     # 源码
|- tests/   # 测试
|- data/     # 本地数据，不提交
|- README.md
```

## 运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -requirements.txt
python -m pytest -q
```

## 进度

- [x] 创建仓库
- [ ] Day 1：cards.py 的 JSON 存取 + 5 条测试
- [ ] 第 1 周：CLI 的 add/list/search
- [ ] 第 2 周：SQLite
- [ ] 第 3 周：FastAPI
- [ ] 第 4 周：LLM 摘要 + 部署

## 说明

- 本项目用于学习与求职作品集。
- 不提交密钥、虚拟环境和个人数据