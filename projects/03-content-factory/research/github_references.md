# GitHub / 开源流程学习笔记

调研用于借鉴**结构**，本仓库 MVP **不自动发布**、不搬运对方代码授权不明部分。

## 参考仓库

1. [cv-cat/XHS_ALL_IN_ONE](https://github.com/cv-cat/XHS_ALL_IN_ONE)  
   采集 → 内容库 → AI 改写 → 图片 → 发布。学习点：全链路阶段切分、内容库标签。

2. [alextangson/AutoCrew](https://github.com/alextangson/AutoCrew)  
   选题研究 → 平台文案 → 去 AI 味 / 敏感词 → 封面。学习点：发布前检查清单、本地数据目录。

3. [Yice-AI/xhs-marketing-master](https://github.com/Yice-AI/xhs-marketing-master)  
   策略原子 → 多路线 → 封面 prompt；Web 生产与浏览器插件发布分离。学习点：生产与发布解耦（我们更彻底：只生产到本地）。

## 吸收到本 Factory 的设计

- 14 阶段目录与 `outputs/<run_id>/` 打包一致
- `03_fact_check` 强制存在（文化版权 + 资讯口径）
- `13_publish` 固定 `local_only`
- 方向用 `config/directions.md` + `niche_expansion.md` 持续扩小方向
