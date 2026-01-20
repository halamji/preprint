#!/usr/bin/env python3
"""
论文添加辅助脚本
帮助用户快速添加新论文到论文库

使用方法:
    python3 add_paper.py --title "论文标题" --authors "作者1,作者2" --pdf /path/to/paper.pdf
"""

import argparse
import json
import os
import shutil
import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(title):
    """将论文标题转换为安全的目录名"""
    # 转小写，替换特殊字符
    name = title.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')


def create_paper_directory(paper_id, title, authors, abstract, year, pdf_path, keywords=None):
    """创建论文目录结构"""
    
    # 确定论文目录名
    papers_dir = Path('papers')
    paper_dir = papers_dir / paper_id
    
    # 创建目录
    paper_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制 PDF 文件
    if pdf_path and os.path.exists(pdf_path):
        dest_pdf = paper_dir / 'manuscript.pdf'
        shutil.copy2(pdf_path, dest_pdf)
        print(f"✓ 已复制 PDF: {dest_pdf}")
    else:
        print("⚠ 未提供 PDF 文件，请稍后手动放置")
    
    # 生成日期
    pub_date = datetime.now().strftime('%Y-%m-%d')
    pub_date_slash = datetime.now().strftime('%Y/%m/%d')
    
    # 创建 index.html
    authors_list = [a.strip() for a in authors.split(',')]
    citation_authors = '\n    '.join([f'<meta name="citation_author" content="{a}">' 
                                      for a in authors_list])
    
    authors_html = ', '.join(authors_list)
    keywords_str = ', '.join(keywords) if keywords else '研究, 学术'
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>论文：{title}</title>
    <meta name="description" content="{abstract}">
    <meta name="keywords" content="{keywords_str}">
    
    <!-- Google Scholar 元数据（重要！） -->
    <meta name="citation_title" content="{title}">
    {citation_authors}
    <meta name="citation_publication_date" content="{pub_date_slash}">
    <meta name="citation_pdf_url" content="https://yourusername.github.io/preprint/papers/{paper_id}/manuscript.pdf">
    <meta name="citation_abstract_html_url" content="https://yourusername.github.io/preprint/papers/{paper_id}/">
    <meta name="citation_keywords" content="{keywords_str}">
    
    <!-- Schema.org 结构化数据 -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": "{title}",
        "author": [
            {json.dumps([{"@type": "Person", "name": a} for a in authors_list], ensure_ascii=False)[1:-1]}
        ],
        "datePublished": "{pub_date}",
        "description": "{abstract}",
        "keywords": "{keywords_str}",
        "mainEntity": {{
            "@type": "CreativeWork"
        }}
    }}
    </script>
    
    <link rel="stylesheet" href="../../assets/style.css">
    <style>
        .paper-detail {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 900px;
            margin: 20px auto;
        }}
        
        .paper-detail h1 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        
        .paper-detail .authors {{
            color: #3498db;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .paper-detail .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding: 20px;
            background: #f5f7fa;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .meta-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .meta-label {{
            font-weight: 600;
            color: #3498db;
            font-size: 0.85em;
            margin-bottom: 3px;
        }}
        
        .meta-value {{
            color: #2c3e50;
        }}
        
        .abstract-section {{
            margin: 25px 0;
        }}
        
        .abstract-section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        
        .abstract-section p {{
            line-height: 1.8;
            color: #555;
            text-align: justify;
        }}
        
        .keywords {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 15px 0;
        }}
        
        .keyword {{
            background: #3498db;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .download-section {{
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            font-weight: 500;
        }}
        
        .btn-primary {{
            background: #3498db;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #2980b9;
            transform: translateY(-2px);
        }}
        
        .btn-secondary {{
            background: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
        }}
        
        .btn-secondary:hover {{
            background: #bdc3c7;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../../" class="back-link">← 返回论文列表</a>
        
        <article class="paper-detail" itemscope itemtype="https://schema.org/ScholarlyArticle">
            <h1 itemprop="headline">{title}</h1>
            
            <div class="authors" itemprop="author">
                {authors_html}
            </div>
            
            <div class="meta-info">
                <div class="meta-item">
                    <span class="meta-label">发表日期</span>
                    <span class="meta-value" itemprop="datePublished">{pub_date}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">机构</span>
                    <span class="meta-value">Your University</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">类型</span>
                    <span class="meta-value">预印本/论文稿</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">语言</span>
                    <span class="meta-value">中文</span>
                </div>
            </div>
            
            <section class="abstract-section">
                <h2>摘要 (Abstract)</h2>
                <p itemprop="abstract">
                    {abstract}
                </p>
                
                <div class="keywords">
                    {' '.join([f'<span class="keyword">{kw}</span>' for kw in (keywords if keywords else [])])}
                </div>
            </section>
            
            <div class="download-section">
                <a href="manuscript.pdf" class="btn btn-primary" download>📥 下载 PDF</a>
                <a href="https://arxiv.org/" class="btn btn-secondary" target="_blank">arXiv 链接 (可选)</a>
                <a href="https://doi.org/" class="btn btn-secondary" target="_blank">DOI 链接 (可选)</a>
            </div>
            
            <section class="abstract-section" style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1;">
                <h2>引用格式 (Citation)</h2>
                <pre style="background: #f5f7fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
{authors_html}. "{title}." {pub_date}.

@article{{yourname{year},
  title={{{title}}},
  author={{{authors_html}}},
  year={{{year}}},
  url={{https://yourusername.github.io/preprint/papers/{paper_id}/}}
}}
                </pre>
            </section>
        </article>
    </div>
</body>
</html>'''
    
    index_path = paper_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ 已创建索引页: {index_path}")
    
    return paper_dir, pub_date


def update_sitemap(paper_id, pub_date):
    """更新 sitemap.xml"""
    
    sitemap_path = Path('sitemap.xml')
    
    if not sitemap_path.exists():
        print("⚠ sitemap.xml 不存在")
        return
    
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在 </urlset> 前添加新条目
    new_entry = f'''    <url>
        <loc>https://yourusername.github.io/preprint/papers/{paper_id}/</loc>
        <lastmod>{pub_date}</lastmod>
        <changefreq>never</changefreq>
        <priority>0.8</priority>
        <scholar:metadata>
            <scholar:publication_date>{pub_date}</scholar:publication_date>
            <scholar:pdf_url>https://yourusername.github.io/preprint/papers/{paper_id}/manuscript.pdf</scholar:pdf_url>
        </scholar:metadata>
    </url>
    
'''
    
    # 检查是否已存在
    if f'papers/{paper_id}/' in content:
        print("⚠ 该论文已在 sitemap.xml 中")
        return
    
    content = content.replace('</urlset>', new_entry + '</urlset>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已更新 sitemap.xml")


def update_manifest(paper_id, title, authors, abstract, year, keywords=None):
    """更新 papers-manifest.json"""
    
    manifest_path = Path('papers-manifest.json')
    
    pub_date = datetime.now().strftime('%Y-%m-%d')
    
    paper_entry = {
        "id": paper_id,
        "title": title,
        "authors": authors,
        "year": year,
        "date": pub_date,
        "abstract": abstract,
        "keywords": keywords if keywords else [],
        "pdfUrl": f"papers/{paper_id}/manuscript.pdf",
        "pageUrl": f"papers/{paper_id}/index.html",
        "arxiv": None,
        "doi": None
    }
    
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
    else:
        papers = []
    
    # 检查是否已存在
    if any(p['id'] == paper_id for p in papers):
        print("⚠ 该论文已在 papers-manifest.json 中")
        return
    
    papers.append(paper_entry)
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已更新 papers-manifest.json")


def main():
    parser = argparse.ArgumentParser(
        description='添加新论文到论文库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python3 add_paper.py \\
    --title "深度学习在计算机视觉中的应用" \\
    --authors "张三,李四" \\
    --abstract "本论文讨论了..." \\
    --pdf ~/paper.pdf \\
    --keywords "深度学习,计算机视觉,CNN"
        '''
    )
    
    parser.add_argument('--title', required=True, help='论文标题')
    parser.add_argument('--authors', required=True, help='作者（用逗号分隔）')
    parser.add_argument('--abstract', required=True, help='论文摘要')
    parser.add_argument('--year', type=int, default=datetime.now().year, help='出版年份')
    parser.add_argument('--pdf', help='PDF 文件路径')
    parser.add_argument('--keywords', help='关键词（用逗号分隔）')
    parser.add_argument('--id', help='自定义论文 ID（默认从标题生成）')
    
    args = parser.parse_args()
    
    # 生成论文 ID
    paper_id = args.id or f"{sanitize_filename(args.title)}-{datetime.now().strftime('%Y-%m-%d')}"
    
    print(f"📝 添加新论文: {args.title}")
    print(f"   ID: {paper_id}")
    print()
    
    # 处理关键词
    keywords = [k.strip() for k in args.keywords.split(',')] if args.keywords else []
    
    # 创建论文目录
    paper_dir, pub_date = create_paper_directory(
        paper_id,
        args.title,
        args.authors,
        args.abstract,
        args.year,
        args.pdf,
        keywords
    )
    
    # 更新 sitemap.xml
    update_sitemap(paper_id, pub_date)
    
    # 更新 papers-manifest.json
    update_manifest(paper_id, args.title, args.authors, args.abstract, args.year, keywords)
    
    print()
    print("✅ 完成！")
    print()
    print("后续步骤:")
    print("1. 如果未提供 PDF，请手动复制到: papers/{}/manuscript.pdf".format(paper_id))
    print("2. (可选) 编辑 papers/{}/index.html 添加更多详细信息".format(paper_id))
    print("3. 运行以下命令提交更改:")
    print()
    print("   git add papers/{} sitemap.xml papers-manifest.json".format(paper_id))
    print('   git commit -m "Add new paper: {}"'.format(args.title))
    print("   git push origin main")
    print()


if __name__ == '__main__':
    main()
