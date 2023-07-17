[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

开箱即用的 flask + Gunicorn + Nginx + Docker Web Application 开发、部署方案。满足 12 factor 指导原则和 CI/CD 开发流程。

## Requirements

- Python 3.11
- PDM
- Docker
- Git

## Features

- 使用 PDM 管理项目和依赖
- 集成 MySQL + Redis
- Type Hint + Pyright 静态类型检查
- Black + ruff 代码检查
- 统一环境变量管理和配置管理
- 基于 structlog 的日志管理
- 统一错误处理
- 权限管理
- 基于 pydantic 的请求参数校验
- 基于 redis 的多层缓存设计
- 集成 celery 任务队列
- 集成 meilisearch 全文搜索
- 基于 Websocket 的实时通信
- 分布式锁 `task/lock.py`
- 符合 RESTful API 设计规范
- 基于 Docker Compose 部署
- pre-commit + GitHub Actions 自动化代码检查
- 支持 mkdocs 文档生成
- ...

## Port

- web: 5000
- mysql: 3306
- redis: 6379
- meilisearch: 7700
- celery_flower: 5555
- nginx: 8000

## Checklists

- [ ] pyproject.toml
  - [ ] dependencies version
  - [ ] [tool.black] required-version
  - [ ] [tool.ruff] required-version
- [ ] .github/workflows
  - [ ] [quality.yml] python-version、pdm-version
  - [ ] [doc.yml] python-version、pdm-version
- [ ] .pre-commit-config.yaml
  - [ ] dependencies version

## 运行

```sh
# 本地运行文档
pdm doc
# or pdm run doc or pdm run mkdocs serve
```
