---
title: "Cross-scene Encrypted Traffic Anomaly Detection via Lifelong Learning"
collection: publications
category: manuscripts
permalink: /publication/2025-12-01-lead-framework
excerpt: '提出一种面向加密流量异常检测的终身学习方法，搭建含元知识库与向量指纹检索的 LEAD 框架。'
date: 2025-12-01
venue: 'IEEE GLOBECOM 2026 (Under Review)'
citation: 'Yang, Q. et al. "Cross-scene Encrypted Traffic Anomaly Detection via Lifelong Learning." Submitted to <i>IEEE GLOBECOM 2026</i>.'
---

本文提出一种面向加密流量异常检测的终身学习方法 **LEAD 框架**，解决跨场景下流量分布漂移导致的模型灾难性遗忘问题。

核心贡献：
- 构建 **元知识库** 存储历史流量模式，实现跨场景知识复用
- 设计 **向量指纹检索机制**，快速匹配流量样本与历史模式
- 引入 **EWC (Elastic Weight Consolidation)** 抗遗忘策略，保障模型持续学习能力
- 依托轻量化 **1D-CNN** 实现高效流量特征提取与模块化迭代更新
