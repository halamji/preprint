# 项目完成检查清单

这个清单帮助你快速部署论文库。

## ✅ 前置检查

- [ ] 已安装 Git
- [ ] 拥有 GitHub 账号
- [ ] 有至少一篇论文的 PDF

## 🔧 本地设置

- [ ] 下载/克隆项目
- [ ] 查看项目结构（已完成 ✓）

## 📝 个性化配置

在部署前，修改以下文件：

### 1. 主页配置（`index.html`）

- [ ] 修改 `<h1>` - 改成你的名字或标题
- [ ] 修改 `<p class="subtitle">` - 改成你的副标题
- [ ] 修改 `<p class="description">` - 改成网站描述
- [ ] 修改 GitHub 链接：`https://github.com/yourusername/preprint`
- [ ] 修改 schema.org 数据中的 `url`

### 2. 网站地图（`sitemap.xml`）

- [ ] 将所有 `yourusername.github.io` 替换为你的实际 GitHub Pages URL
- [ ] 更新 `<lastmod>` 日期（可选）

### 3. 论文页面（`papers/example-paper-001/index.html`）

虽然这是示例，但检查格式：
- [ ] 理解元标签结构
- [ ] 理解 Schema.org 标记

### 4. Robots.txt

- [ ] 如有自定义域名，更新 sitemap 链接

## 📚 添加第一篇论文

### 方法 1：自动添加（推荐）

```bash
python3 add_paper.py \
  --title "Your Paper Title" \
  --authors "Your Name,Co-author" \
  --abstract "Abstract text here..." \
  --pdf /path/to/your/paper.pdf
```

- [ ] 论文目录已创建
- [ ] PDF 已复制
- [ ] HTML 已生成
- [ ] Sitemap 已更新

### 方法 2：手动添加

```bash
# 复制示例论文目录
cp -r papers/example-paper-001 papers/my-first-paper

# 替换 PDF
cp /path/to/your/paper.pdf papers/my-first-paper/manuscript.pdf

# 编辑 HTML
nano papers/my-first-paper/index.html
# 修改：标题、作者、摘要、元标签等

# 更新 sitemap.xml
# 添加新的 <url> 条目
```

- [ ] 论文目录已创建：`papers/my-first-paper/`
- [ ] PDF 已放置：`papers/my-first-paper/manuscript.pdf`
- [ ] HTML 已编辑：`papers/my-first-paper/index.html`
- [ ] Sitemap 已更新

## 🚀 GitHub 部署

### 1. 创建 GitHub 仓库

- [ ] 在 GitHub 上创建新仓库（名称：`preprint`）
- [ ] 仓库设置为 **Public**（重要！）

### 2. 本地 Git 初始化

```bash
git init
git add .
git commit -m "Initial commit: Academic papers vault"
git remote add origin https://github.com/yourusername/preprint.git
git branch -M main
git push -u origin main
```

- [ ] 文件已提交
- [ ] 已推送到 GitHub

### 3. 启用 GitHub Pages

- [ ] 进入仓库 Settings → Pages
- [ ] Branch: `main`
- [ ] Folder: `/ (root)`
- [ ] 点击 Save

等待 1-2 分钟...

- [ ] 网站已在线：`https://yourusername.github.io/preprint/`

### 4. 验证部署

- [ ] 访问主页 - 能否看到论文列表？
- [ ] 点击论文 - 能否打开论文页面？
- [ ] 下载 PDF - PDF 能否成功下载？
- [ ] 检查样式 - 页面显示是否正确？

## 🔍 搜索引擎提交

### 1. Google Search Console

- [ ] 访问 https://search.google.com/search-console
- [ ] 添加网站属性
- [ ] 验证所有权（按提示）
- [ ] 提交 sitemap：`https://yourusername.github.io/preprint/sitemap.xml`
- [ ] 请求索引你的主页

### 2. Google Scholar

- [ ] 访问 https://scholar.google.com/intl/en/scholar/inclusion.html
- [ ] 点击 "Request inclusion"
- [ ] 填写表单并提交

### 3. 其他搜索引擎（可选）

- [ ] Bing Webmaster Tools
- [ ] Yandex （如面向俄语用户）
- [ ] 百度 （如面向中文用户）

## ⏱️ 等待索引

- [ ] 等待 2-4 周让 Google Scholar 索引
- [ ] 定期检查 Search Console 的索引状态
- [ ] 在 Google 中搜索你的论文标题验证

## 📊 验证和监控

- [ ] 在 Google Scholar 中搜索你的名字
- [ ] 在 Google Scholar 中搜索论文标题
- [ ] 查看 Search Console 的搜索性能报告
- [ ] 检查论文页面的 Rich Results

## 🎓 后续维护

- [ ] 添加更多论文（按需）
- [ ] 定期更新 sitemap（添加论文后）
- [ ] 监控 Search Console 错误
- [ ] 回应学术社交网络的引用

## 🎉 完成！

如果以上项目都完成，恭喜！你已成功部署了论文库。

### 进阶功能（可选）

- [ ] 添加 Google Analytics 追踪
- [ ] 集成数学公式渲染（MathJax）
- [ ] 添加论文分类/标签功能
- [ ] 集成 GitHub Discussions 评论
- [ ] 创建 RSS 订阅源

## 📞 需要帮助？

- 查看 `QUICK_START.md` - 快速开始指南
- 查看 `DEPLOYMENT.md` - 详细部署指南
- 查看 `README.md` - 完整项目文档

---

**启动成功！** 🚀 现在世界可以发现你的研究了。
