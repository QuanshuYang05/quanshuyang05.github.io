# 杨荃舒个人主页 — academicpages Jekyll GitHub Pages

杨荃舒的学术个人主页，基于 [academicpages](https://github.com/academicpages/academicpages.github.io) 模板。

定位：**AI + 网络流量安全 + 深度学习**

## 构建与预览

```bash
bundle install
bundle exec jekyll serve
```

本地预览：http://127.0.0.1:4000/

## 目录结构

```
├── _config.yml           站点全局配置（个人信息、主题、集合）
├── _data/
│   └── navigation.yml    顶部导航栏
├── _pages/
│   ├── about.md          首页（AI 流量安全方向）
│   ├── cv.md             CV 页面
│   ├── publications.html 论文列表页
│   └── portfolio.html    项目列表页
├── _publications/        论文条目（2篇）
├── _portfolio/           项目条目（7个）
├── _includes/            HTML 模板片段
├── _layouts/             页面布局
├── _sass/                SCSS 样式
├── assets/               CSS/JS/字体
└── images/               图片（头像、favicon 等）
```

## 常用编辑操作

| 操作 | 文件 |
|------|------|
| 修改个人信息 | `_config.yml` → `author` 部分 |
| 修改首页内容 | `_pages/about.md` |
| 修改 CV | `_pages/cv.md` |
| 添加论文 | `_publications/` 创建 `.md` 文件 |
| 添加项目 | `_portfolio/` 创建 `.md` 文件 |
| 替换头像 | `images/profile.png` |

## 部署

推送到 GitHub 仓库 `QuanshuYang05/QuanshuYang05.github.io`，
GitHub Pages 自动构建部署到 https://quanshuyang05.github.io/。
