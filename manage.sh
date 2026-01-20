#!/bin/bash

# 论文库管理脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    cat << EOF
${BLUE}学术论文库 - 管理脚本${NC}

用法: ./manage.sh <命令> [选项]

命令:
    list          列出所有论文
    add           添加新论文（需要参数）
    validate      验证 HTML 和 sitemap
    clean         清理临时文件
    serve         本地预览（需要 Python 3）
    help          显示此帮助

示例:
    ./manage.sh list
    ./manage.sh add --title "论文名" --authors "作者" --pdf paper.pdf
    ./manage.sh validate
    ./manage.sh serve

EOF
}

list_papers() {
    echo -e "${BLUE}📚 已发布论文列表:${NC}\n"
    
    if [ -d "papers" ]; then
        count=0
        for dir in papers/*/; do
            if [ -f "$dir/index.html" ]; then
                basename=$(basename "$dir")
                count=$((count + 1))
                
                # 从 HTML 中提取标题
                if [ -f "$dir/index.html" ]; then
                    title=$(grep -o '<meta name="citation_title" content="[^"]*"' "$dir/index.html" | head -1 | sed 's/.*content="\(.*\)"/\1/')
                    if [ -z "$title" ]; then
                        title=$(grep -o '<h1[^>]*>[^<]*' "$dir/index.html" | sed 's/<h1[^>]*>//')
                    fi
                    echo -e "${GREEN}$count.${NC} $title"
                    echo "   📁 $basename"
                fi
                
                if [ -f "$dir/manuscript.pdf" ]; then
                    size=$(ls -lh "$dir/manuscript.pdf" | awk '{print $5}')
                    echo "   📄 PDF ($size)"
                fi
                echo
            fi
        done
        
        if [ $count -eq 0 ]; then
            echo -e "${YELLOW}⚠  暂无论文${NC}"
        else
            echo -e "${GREEN}✓ 共 $count 篇论文${NC}"
        fi
    else
        echo -e "${RED}✗ papers 目录不存在${NC}"
    fi
}

validate() {
    echo -e "${BLUE}🔍 验证项目配置${NC}\n"
    
    errors=0
    warnings=0
    
    # 检查必需文件
    echo "检查必需文件..."
    for file in index.html sitemap.xml .nojekyll assets/style.css assets/main.js; do
        if [ -f "$file" ]; then
            echo -e "${GREEN}✓${NC} $file"
        else
            echo -e "${RED}✗${NC} $file (缺失)"
            errors=$((errors + 1))
        fi
    done
    
    echo
    echo "检查论文页面..."
    
    paper_count=0
    for dir in papers/*/; do
        if [ -f "$dir/index.html" ]; then
            paper_count=$((paper_count + 1))
            basename=$(basename "$dir")
            
            # 检查必需的 meta 标签
            has_title=$(grep -c 'citation_title' "$dir/index.html" || echo 0)
            has_author=$(grep -c 'citation_author' "$dir/index.html" || echo 0)
            has_pdf=$(grep -c 'citation_pdf_url' "$dir/index.html" || echo 0)
            has_date=$(grep -c 'citation_publication_date' "$dir/index.html" || echo 0)
            
            if [ "$has_title" -eq 0 ] || [ "$has_author" -eq 0 ] || [ "$has_pdf" -eq 0 ]; then
                echo -e "${RED}✗${NC} $basename (缺少关键元标签)"
                errors=$((errors + 1))
            else
                echo -e "${GREEN}✓${NC} $basename"
            fi
            
            # 检查 PDF 文件
            if [ ! -f "$dir/manuscript.pdf" ]; then
                echo -e "  ${YELLOW}⚠${NC}  缺少 PDF 文件"
                warnings=$((warnings + 1))
            fi
        fi
    done
    
    echo
    echo "检查 sitemap.xml..."
    
    if grep -q "scholar:metadata" sitemap.xml; then
        echo -e "${GREEN}✓${NC} 包含 Google Scholar 元数据"
    else
        echo -e "${YELLOW}⚠${NC}  建议添加 Google Scholar 元数据"
        warnings=$((warnings + 1))
    fi
    
    echo
    echo -e "${BLUE}=== 验证结果 ===${NC}"
    echo -e "论文总数: ${GREEN}$paper_count${NC}"
    echo -e "错误数: $([ $errors -eq 0 ] && echo -e ${GREEN} || echo -e ${RED})$errors${NC}"
    echo -e "警告数: $([ $warnings -eq 0 ] && echo -e ${GREEN} || echo -e ${YELLOW})$warnings${NC}"
}

serve() {
    echo -e "${BLUE}🌐 启动本地服务器${NC}\n"
    
    if command -v python3 &> /dev/null; then
        port=8000
        url="http://localhost:$port"
        echo -e "访问地址: ${GREEN}$url${NC}"
        echo -e "按 ${YELLOW}Ctrl+C${NC} 停止服务器\n"
        python3 -m http.server $port
    else
        echo -e "${RED}✗ 需要 Python 3${NC}"
        exit 1
    fi
}

add_paper_interactive() {
    echo -e "${BLUE}📝 添加新论文${NC}\n"
    
    read -p "论文标题: " title
    read -p "作者（用逗号分隔）: " authors
    read -p "摘要: " abstract
    read -p "PDF 文件路径（可选）: " pdf_path
    read -p "关键词（用逗号分隔，可选）: " keywords
    
    if command -v python3 &> /dev/null && [ -f "add_paper.py" ]; then
        python3 add_paper.py \
            --title "$title" \
            --authors "$authors" \
            --abstract "$abstract" \
            ${pdf_path:+--pdf "$pdf_path"} \
            ${keywords:+--keywords "$keywords"}
    else
        echo -e "${RED}✗ 无法运行 add_paper.py${NC}"
        exit 1
    fi
}

clean() {
    echo -e "${BLUE}🧹 清理临时文件${NC}\n"
    
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
    find . -name "*.pyc" -delete 2>/dev/null
    find . -name ".DS_Store" -delete 2>/dev/null
    find . -name "*.bak" -delete 2>/dev/null
    
    echo -e "${GREEN}✓ 清理完成${NC}"
}

# 主程序
case "$1" in
    list)
        list_papers
        ;;
    add)
        if [ $# -gt 1 ]; then
            python3 add_paper.py "${@:2}"
        else
            add_paper_interactive
        fi
        ;;
    validate)
        validate
        ;;
    serve)
        serve
        ;;
    clean)
        clean
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        echo "使用 './manage.sh help' 获取帮助"
        exit 1
        ;;
esac
