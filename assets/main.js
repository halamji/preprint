// 论文数据管理和页面生成
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const papers = await loadPapersMetadata();
        displayPapers(papers);
        updateSchemaPart(papers);
    } catch (error) {
        console.error('加载论文失败:', error);
        showError();
    }
});

// 从 papers 目录加载论文元数据
async function loadPapersMetadata() {
    try {
        // 尝试加载 papers-manifest.json（如果存在）
        const response = await fetch('papers-manifest.json');
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.log('使用备选论文列表');
    }
    
    // 备选：返回示例论文
    return getDefaultPapers();
}

// 获取默认论文列表
function getDefaultPapers() {
    return [
        {
            id: 'example-paper-001',
            title: '示例论文：深度学习在自然语言处理中的应用',
            authors: 'Your Name, Co-Author Name',
            year: 2026,
            date: '2026-01-20',
            abstract: '这是一篇示例论文。请替换为您的实际论文信息。本论文探讨了深度学习技术在自然语言处理领域的最新应用。',
            keywords: ['深度学习', '自然语言处理', '神经网络'],
            pdfUrl: 'papers/example-paper-001/manuscript.pdf',
            pageUrl: 'papers/example-paper-001/index.html',
            arxiv: null,
            doi: null
        }
    ];
}

// 显示论文卡片
function displayPapers(papers) {
    const container = document.getElementById('papers-container');
    
    if (!papers || papers.length === 0) {
        container.innerHTML = '<div class="no-papers"><p>📭 暂无论文</p><p>请上传您的论文</p></div>';
        return;
    }

    container.innerHTML = papers.map(paper => createPaperCard(paper)).join('');
}

// 创建论文卡片 HTML
function createPaperCard(paper) {
    const year = new Date(paper.date || paper.year).getFullYear();
    const keywords = paper.keywords ? paper.keywords.slice(0, 3).join(', ') : '';
    
    return `
        <div class="paper-card" itemscope itemtype="https://schema.org/ScholarlyArticle">
            <h3 itemprop="headline">${escapeHtml(paper.title)}</h3>
            <div class="paper-meta">
                <div class="paper-meta-item">
                    <span class="paper-meta-label">作者:</span>
                    <span itemprop="author">${escapeHtml(paper.authors)}</span>
                </div>
                <div class="paper-meta-item">
                    <span class="paper-meta-label">年份:</span>
                    <span itemprop="datePublished">${year}</span>
                </div>
                ${keywords ? `<div class="paper-meta-item">
                    <span class="paper-meta-label">关键词:</span>
                    <span itemprop="keywords">${escapeHtml(keywords)}</span>
                </div>` : ''}
            </div>
            <p class="paper-abstract" itemprop="description">${escapeHtml(paper.abstract)}</p>
            <div class="paper-links">
                <a href="${paper.pageUrl}" class="paper-link">📄 论文页面</a>
                <a href="${paper.pdfUrl}" class="paper-link" itemprop="url" download>📥 下载PDF</a>
                ${paper.arxiv ? `<a href="https://arxiv.org/abs/${paper.arxiv}" class="paper-link external" target="_blank">arXiv</a>` : ''}
                ${paper.doi ? `<a href="https://doi.org/${paper.doi}" class="paper-link external" target="_blank">DOI</a>` : ''}
            </div>
        </div>
    `;
}

// 更新 Schema.org 结构化数据
function updateSchemaPart(papers) {
    const schemaScript = document.querySelector('script[type="application/ld+json"]');
    if (!schemaScript) return;

    const schemaData = JSON.parse(schemaScript.textContent);
    schemaData.hasPart = papers.map(paper => ({
        "@type": "ScholarlyArticle",
        "headline": paper.title,
        "author": paper.authors,
        "datePublished": paper.date || new Date(paper.year, 0, 1).toISOString().split('T')[0],
        "abstract": paper.abstract,
        "url": paper.pageUrl,
        "fileFormat": "PDF",
        "url": paper.pdfUrl
    }));

    schemaScript.textContent = JSON.stringify(schemaData, null, 2);
}

// 显示错误消息
function showError() {
    const container = document.getElementById('papers-container');
    container.innerHTML = '<div class="no-papers"><p>❌ 加载失败</p><p>请检查论文列表配置</p></div>';
}

// HTML 转义函数（防止 XSS）
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
