# 部署指南 - GitHub Pages + Google Scholar

这个文档详细说明如何将论文库部署到 GitHub Pages 并被 Google Scholar 索引。

## 📋 前置需求

- GitHub 账号
- Git 基础知识
- 不需要编程经验！

## 🚀 分步部署指南

### 第 1 步：创建 GitHub 仓库

1. 登录 [github.com](https://github.com)
2. 点击右上角 "+" → "New repository"
3. 填写信息：
   - **Repository name**: `preprint`（或任意名称）
   - **Description**: "My Academic Papers and Preprints"
   - **Public**: ✓ 选中（必须公开才能被 Google Scholar 爬取）
   - **Add README.md**: ✗（我们已有）
4. 点击 "Create repository"

### 第 2 步：本地初始化（首次）

```bash
# 进入项目目录
cd my-preprints-vault

# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial commit: academic papers vault"

# 关联远程仓库（替换 yourusername）
git remote add origin https://github.com/yourusername/preprint.git

# 推送到 main 分支
git branch -M main
git push -u origin main
```

### 第 3 步：启用 GitHub Pages

1. 进入仓库主页 → **Settings**
2. 左侧菜单 → **Pages**
3. **Build and deployment**：
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
4. 点击 **Save**

等待部署完成（通常 1-2 分钟）。页面会显示：

```
Your site is live at https://yourusername.github.io/preprint/
```

### 第 4 步：配置自定义域名（可选）

如果你有自己的域名：

1. **Settings** → **Pages**
2. **Custom domain**: 输入你的域名（例如 `papers.example.com`）
3. 根据提示配置 DNS 记录

### 第 5 步：提交到搜索引擎

#### Google Search Console

1. 访问 [search.google.com/search-console](https://search.google.com/search-console)
2. 点击 **Add property**
3. 选择 **URL prefix**，输入你的网站 URL
4. 验证所有权（按提示操作）
5. 提交 sitemap：
   - 左侧 → **Sitemaps**
   - 输入: `https://yourusername.github.io/preprint/sitemap.xml`
   - 点击 **Submit**

#### Google Scholar（最重要！）

1. 访问 [scholar.google.com/intl/en/scholar/inclusion.html](https://scholar.google.com/intl/en/scholar/inclusion.html)
2. 点击 "Request inclusion" 标签页
3. 填写表单：
   - **Website owner**: 你的名字
   - **Website URL**: `https://yourusername.github.io/preprint/`
   - **Website language**: 中文（或你的语言）
   - **Email**: 你的邮箱
4. 提交请求

**重要**: Google Scholar 通常需要 2-4 周才能索引新网站。确保在索引前：
- ✅ 所有元标签正确
- ✅ PDF 可直接访问
- ✅ 至少有 1-2 篇论文
- ✅ 网站已公开

#### Microsoft Academic Search（可选）

1. 访问 [academic.microsoft.com/profile/edit](https://academic.microsoft.com/profile/edit)
2. 创建学者档案
3. 添加你的论文

## 🔐 重要的 URL 替换

部署前，你需要将以下占位符替换为实际值：

### 在 `index.html` 中：

```html
<!-- 第 1 处：sitemap 链接 -->
<a href="sitemap.xml" class="nav-link">网站地图</a>

<!-- 第 2 处：GitHub 链接 -->
<a href="https://github.com/yourusername/preprint" class="nav-link" target="_blank">GitHub</a>

<!-- 第 3 处：schema.org 数据 -->
"url": "https://yourusername.github.io/preprint/",
```

### 在 `sitemap.xml` 中：

```xml
<!-- 替换所有的 yourusername -->
https://yourusername.github.io/preprint/
```

### 在所有论文页面（`papers/*/index.html`）中：

```html
<!-- 替换论文 URL -->
<meta name="citation_pdf_url" content="https://yourusername.github.io/preprint/papers/paper-id/manuscript.pdf">
<meta name="citation_abstract_html_url" content="https://yourusername.github.io/preprint/papers/paper-id/">

<!-- 替换 schema.org 数据中的 URL -->
"url": "https://yourusername.github.io/preprint/papers/paper-id/"
```

## 📊 验证部署

### 检查 Google Search Console

1. 进入 Search Console
2. 点击你的网站
3. **Coverage** → 查看索引状态
4. **Sitemaps** → 查看提交状态

### 在浏览器中测试

```
# 检查网站是否可访问
https://yourusername.github.io/preprint/

# 检查 sitemap
https://yourusername.github.io/preprint/sitemap.xml

# 检查单篇论文
https://yourusername.github.io/preprint/papers/example-paper-001/
```

### 使用 Google 在线工具

1. **URL 检查工具**：https://support.google.com/webmasters/answer/9012289
   - 输入你的网站 URL
   - 检查索引状态

2. **富媒体测试工具**：https://search.google.com/test/rich-results
   - 输入论文页面 URL
   - 验证 Schema.org 标记

### 验证元标签

在浏览器中右键 → "检查" (Inspect)：

```html
<!-- 查看是否存在这些标签 -->
<meta name="citation_title" content="...">
<meta name="citation_author" content="...">
<meta name="citation_publication_date" content="...">
<meta name="citation_pdf_url" content="...">
```

## 🔄 更新和维护

### 添加新论文

```bash
# 1. 使用脚本
python3 add_paper.py --title "New Paper" --authors "Author" --pdf paper.pdf

# 或手动添加后...

# 2. 提交更改
git add papers/new-paper/ sitemap.xml papers-manifest.json
git commit -m "Add new paper: New Paper Title"
git push origin main

# 3. 等待 GitHub Pages 自动部署（1-2 分钟）
```

### 更新已有论文

```bash
# 编辑论文页面或替换 PDF

# 提交更改
git add papers/paper-id/
git commit -m "Update paper: paper-id"
git push origin main
```

### 监控索引进度

Google Scholar 索引进度查询：

1. 在 Google 中搜索：`site:yourusername.github.io/preprint`
2. 查看返回的论文数量
3. 在 Google Scholar 中搜索你的论文标题

## 🐛 故障排除

### 问题 1：网站无法访问

**症状**: 访问 `https://yourusername.github.io/preprint/` 显示 404

**解决**:
- [ ] 确认仓库是 public
- [ ] 确认 Pages 已启用（Settings → Pages）
- [ ] 等待 1-2 分钟让部署完成
- [ ] 查看 GitHub Actions（仓库 → Actions）检查部署状态

### 问题 2：样式不显示

**症状**: 页面显示但样式错乱

**解决**:
- [ ] 清除浏览器缓存（Ctrl+F5）
- [ ] 检查 `.nojekyll` 文件是否存在
- [ ] 查看浏览器控制台（F12）是否有错误
- [ ] 检查 CSS 文件路径：`assets/style.css`

### 问题 3：PDF 无法下载

**症状**: PDF 链接返回 404

**解决**:
- [ ] 确认 PDF 文件在正确路径：`papers/paper-id/manuscript.pdf`
- [ ] 检查文件名是否与 HTML 中的匹配
- [ ] 确认 PDF 文件没有损坏
- [ ] Git 推送时包含了 PDF 文件

### 问题 4：Google Scholar 不收录

**症状**: 2-4 周后论文仍未出现在 Google Scholar

**解决**:
- [ ] 验证所有 `citation_*` meta 标签存在且正确
- [ ] 检查日期格式：必须是 `YYYY/MM/DD`
- [ ] 确保 PDF URL 可直接访问
- [ ] 在 Google Scholar 页面重新提交网站
- [ ] 等待更长时间（有时需要 6-8 周）

### 问题 5：sitemap 显示 XML 错误

**症状**: 访问 sitemap.xml 显示解析错误

**解决**:
- [ ] 使用在线 XML 验证器：[www.xmlvalidation.com](https://www.xmlvalidation.com/)
- [ ] 检查 XML 语法（特别是 `<` 和 `&`）
- [ ] 使用 `&amp;` 而不是 `&`
- [ ] 确认所有标签都正确关闭

## 📈 监控和优化

### 查看访问统计（GitHub）

虽然 GitHub Pages 不提供内置分析，但可以：

1. 添加 Google Analytics
2. 在 `index.html` 中添加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

获取你的 Google Analytics ID：https://analytics.google.com

### 查看搜索排名

在 Search Console 中：

1. 左侧 → **Performance**
2. 查看你的网站在 Google 搜索中的排名
3. 查看哪些查询将用户带到你的网站

## 🎓 最佳实践

- ✅ 每个月更新至少一次论文列表
- ✅ 定期检查 Search Console 的错误
- ✅ 添加新论文时自动更新 sitemap
- ✅ 在其他学术社交网络上宣传（Twitter, LinkedIn）
- ✅ 建立自己的学者档案（Google Scholar, arXiv, ORCID）
- ✅ 在论文中相互引用和链接

## 📞 获取帮助

如果遇到问题，请查阅：

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Google Search Console 帮助](https://support.google.com/webmasters)
- [Google Scholar 常见问题](https://scholar.google.com/intl/en/scholar/faq.html)

---

**部署成功！** 🎉 你的论文库现在已上线并被学术搜索引擎检索。

下一步：[添加你的第一篇论文](QUICK_START.md#4-添加第一篇论文)
