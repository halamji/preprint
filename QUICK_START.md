# GitHub Pages + Google Scholar 学术论文库

> 一个完整的学术论文在线发布平台，支持 GitHub Pages 免费托管，自动被 Google Scholar、Microsoft Academic 等学术搜索引擎检索。

## ⚡ 快速开始（5 分钟）

### 1. 使用此模板

点击 GitHub 上的 "Use this template" 按钮，创建你的仓库。

### 2. 启用 GitHub Pages

```
设置 → Pages → Branch: main → Folder: / (root) → Save
```

等待部署完成（通常 1-2 分钟），你会看到网站 URL。

### 3. 修改基本信息

编辑 `index.html` 的 `<header>` 部分和 `sitemap.xml` 的 URL：

```html
<!-- index.html -->
<h1>📚 Your Name's Papers</h1>
<p>Your description here</p>
```

```xml
<!-- sitemap.xml -->
<!-- 将 yourusername 替换为你的 GitHub 用户名 -->
```

### 4. 添加第一篇论文

**方法 A：使用脚本（推荐）**

```bash
python3 add_paper.py \
  --title "My First Paper" \
  --authors "Your Name,Co-author" \
  --abstract "The abstract of your paper" \
  --pdf ~/my_paper.pdf
```

**方法 B：手动添加**

```bash
# 1. 复制示例论文目录
cp -r papers/example-paper-001 papers/my-paper

# 2. 替换 PDF
cp ~/my_paper.pdf papers/my-paper/manuscript.pdf

# 3. 编辑 papers/my-paper/index.html 修改元数据

# 4. 在 sitemap.xml 中添加该论文的 URL
```

### 5. 提交更改

```bash
git add papers/ sitemap.xml papers-manifest.json
git commit -m "Add new paper: My First Paper"
git push origin main
```

等待 GitHub Pages 部署（1-2 分钟后访问你的网站）。

## 📋 项目结构

```
my-preprints-vault/
├── .nojekyll                  # 禁用 Jekyll（必需）
├── index.html                 # 主页 - 所有论文列表
├── sitemap.xml                # 网站地图（Google 爬虫需要）
├── papers-manifest.json       # 论文元数据列表
├── papers/
│   ├── example-paper-001/
│   │   ├── index.html         # 论文详情页（含 Google Scholar 元数据）
│   │   └── manuscript.pdf     # 论文 PDF
│   ├── paper-2/
│   │   ├── index.html
│   │   └── manuscript.pdf
│   └── ...
├── assets/
│   ├── style.css              # 样式
│   └── main.js                # 页面逻辑
└── README.md                  # 本文件
```

## 🔍 为什么使用这个方案？

| 特性 | 说明 |
|------|------|
| **免费托管** | GitHub Pages 完全免费，自动 HTTPS |
| **Google Scholar 友好** | 包含正确的 citation meta tags |
| **自动索引** | Sitemap + Schema.org 标记 |
| **易于维护** | 简单的 HTML 结构，无数据库 |
| **版本控制** | 所有论文历史记录都在 Git 中 |
| **无供应商锁定** | 纯 HTML + CSS，可随时迁移 |

## 🚀 核心功能

### 1. Google Scholar 索引

通过正确的 HTML 元标签，你的论文会被 Google Scholar 自动发现：

```html
<meta name="citation_title" content="论文标题">
<meta name="citation_author" content="作者1">
<meta name="citation_author" content="作者2">
<meta name="citation_publication_date" content="YYYY/MM/DD">
<meta name="citation_pdf_url" content="https://...">
```

### 2. 网站地图（Sitemap）

`sitemap.xml` 告诉搜索引擎你有哪些论文：

```xml
<url>
    <loc>https://yourusername.github.io/preprint/papers/paper-id/</loc>
    <lastmod>2026-01-20</lastmod>
    <scholar:metadata>
        <scholar:pdf_url>https://.../manuscript.pdf</scholar:pdf_url>
    </scholar:metadata>
</url>
```

### 3. Schema.org 结构化数据

让搜索引擎能够解析你的论文信息：

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    "headline": "论文标题",
    "author": [{"@type": "Person", "name": "作者"}],
    "datePublished": "2026-01-20"
}
</script>
```

## 📊 管理大量论文

### 使用 papers-manifest.json

对于大量论文，在根目录创建 `papers-manifest.json`：

```json
[
    {
        "id": "paper-001",
        "title": "Paper Title",
        "authors": "Author1, Author2",
        "year": 2026,
        "date": "2026-01-20",
        "abstract": "Abstract text",
        "keywords": ["keyword1", "keyword2"],
        "pdfUrl": "papers/paper-001/manuscript.pdf",
        "pageUrl": "papers/paper-001/index.html"
    }
]
```

主页会自动从这个文件加载所有论文。

## ✨ 自定义

### 修改样式

编辑 `assets/style.css` 修改颜色和字体：

```css
:root {
    --primary-color: #2c3e50;      /* 主颜色 */
    --secondary-color: #3498db;    /* 强调色 */
    --accent-color: #e74c3c;       /* 标记色 */
}
```

### 添加分类

修改 `papers-manifest.json` 添加 `category` 字段，然后修改 `assets/main.js` 实现分类过滤。

### 集成数学公式

在 `index.html` 中添加 MathJax：

```html
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

## 🔗 搜索引擎提交

### Google Search Console

1. 访问 https://search.google.com/search-console
2. 添加你的网站
3. 提交 sitemap：`https://yourusername.github.io/preprint/sitemap.xml`
4. 请求索引你的主页面

### Google Scholar

1. 访问 https://scholar.google.com/intl/en/scholar/inclusion.html
2. 填写表单提交你的网站

## 🐛 常见问题

### Q: 论文为什么没有出现在 Google Scholar？

A: Google Scholar 通常需要 2-4 周才能索引新网站。确保：
- [ ] 元标签正确（`citation_*`）
- [ ] PDF 可直接访问
- [ ] 论文 URL 在 sitemap.xml 中
- [ ] 已在 Search Console 中提交

### Q: 如何支持多种语言？

A: 修改 `lang` 属性并提供翻译的元数据：

```html
<html lang="en">
<meta name="citation_title" content="English Title">
```

### Q: 我可以添加评论吗？

A: 可以集成 Disqus 或 GitHub Discussions，在 `papers/*/index.html` 中添加：

```html
<div id="disqus_thread"></div>
```

### Q: 如何做到私密发布？

A: 使用 GitHub 的私有仓库 + GitHub Pages（需要 Pro），或使用其他托管方案。

## 📈 性能优化

- [ ] 压缩 PDF 文件（保持可读性）
- [ ] 使用 CDN 加速（GitHub Pages 已包含）
- [ ] 启用浏览器缓存
- [ ] 使用 WebP 图片格式（如有）

## 🔐 隐私和安全

- [ ] 默认不收集用户数据
- [ ] 所有通信均通过 HTTPS（GitHub Pages 提供）
- [ ] 无第三方追踪代码（可选择添加 Google Analytics）

## 📚 参考资源

- [GitHub Pages 官方文档](https://pages.github.com/)
- [Google Scholar 收录指南](https://scholar.google.com/intl/en/scholar/inclusion.html)
- [Schema.org ScholarlyArticle](https://schema.org/ScholarlyArticle)
- [Web.dev SEO 最佳实践](https://web.dev/lighthouse-seo/)

## 📝 许可证

本项目使用 MIT 许可证。

---

**开始使用** 👉 [创建你的论文库](#快速开始5-分钟)

有问题？提交 GitHub Issue 或查看完整 README.md
