#!/usr/bin/env python3
"""
经验库搜索工具
支持按关键词、标签、技术栈、难度等维度搜索经验
支持YAML和Markdown格式的经验文件
"""

import os
import yaml
import json
import sys
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import argparse

class ExperienceSearcher:
    def __init__(self, experiences_dir: str = "experiences"):
        self.experiences_dir = Path(experiences_dir)
        self.experiences = []
        self.load_experiences()
    
    def load_experiences(self):
        """加载所有经验文件（支持YAML和Markdown格式）"""
        self.experiences = []
        
        # 加载YAML格式的经验
        for yaml_file in self.experiences_dir.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    experience = yaml.safe_load(f)
                    experience['file_path'] = str(yaml_file)
                    experience['format'] = 'yaml'
                    self.experiences.append(experience)
            except Exception as e:
                print(f"错误: 无法加载YAML文件 {yaml_file}: {e}")
        
        # 加载Markdown格式的经验
        for md_file in self.experiences_dir.rglob("*.md"):
            try:
                experience = self.parse_markdown_experience(md_file)
                if experience:
                    experience['file_path'] = str(md_file)
                    experience['format'] = 'markdown'
                    self.experiences.append(experience)
            except Exception as e:
                print(f"错误: 无法加载Markdown文件 {md_file}: {e}")
    
    def parse_markdown_experience(self, md_file: Path) -> Optional[Dict[str, Any]]:
        """解析Markdown格式的经验文件"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析标题
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem
            
            # 解析元信息（在 > 块中）
            meta_pattern = r'> \*\*([^*]+)\*\*:\s*(.+?)(?=\n(?:> |[^>]))'
            meta_matches = re.findall(meta_pattern, content, re.DOTALL)
            meta_info = {key: value.strip() for key, value in meta_matches}
            
            # 解析技术栈
            tech_stack = []
            tech_stack_text = meta_info.get('技术栈', '')
            if tech_stack_text:
                tech_stack = [tech.strip() for tech in tech_stack_text.split(',')]
            
            # 解析难度等级
            difficulty = 'intermediate'  # 默认值
            difficulty_text = meta_info.get('难度等级', '')
            if '⭐⭐⭐⭐⭐' in difficulty_text:
                difficulty = 'expert'
            elif '⭐⭐⭐⭐' in difficulty_text:
                difficulty = 'advanced'
            elif '⭐⭐⭐' in difficulty_text:
                difficulty = 'intermediate'
            elif '⭐⭐' in difficulty_text:
                difficulty = 'beginner'
            
            # 从文件路径推断分类
            path_parts = md_file.parts
            category = 'general'
            subcategory = 'general'
            
            if len(path_parts) >= 2:
                category_part = path_parts[-2]
                if category_part.startswith('0') and '-' in category_part:
                    category = category_part.split('-', 1)[1]
                elif category_part in ['flutter', 'react', 'python', 'cursor-workflows']:
                    subcategory = category_part
                    # 从上级目录获取category
                    if len(path_parts) >= 3:
                        parent_part = path_parts[-3]
                        if parent_part.startswith('0') and '-' in parent_part:
                            category = parent_part.split('-', 1)[1]
                else:
                    category = category_part
            
            # 提取标签（从内容中寻找标签模式）
            tags = []
            tags_match = re.search(r'标签[：:]\s*\[([^\]]+)\]', content)
            if tags_match:
                tags = [tag.strip().strip('"').strip("'") for tag in tags_match.group(1).split(',')]
            else:
                # 从技术栈和分类推断标签
                tags = tech_stack.copy()
                if category not in tags:
                    tags.append(category)
                if subcategory != 'general' and subcategory not in tags:
                    tags.append(subcategory)
            
            # 提取描述（从背景描述或问题场景部分）
            description = ''
            desc_match = re.search(r'## 背景描述\s*\n\n(.+?)(?=\n##)', content, re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()[:200] + '...' if len(desc_match.group(1)) > 200 else desc_match.group(1).strip()
            else:
                # 尝试从标题下方的内容提取
                intro_match = re.search(r'^# .+?\n\n(.+?)(?=\n##)', content, re.DOTALL)
                if intro_match:
                    description = intro_match.group(1).strip()[:200] + '...' if len(intro_match.group(1)) > 200 else intro_match.group(1).strip()
            
            # 生成ID
            experience_id = f"{category}-{subcategory}-{md_file.stem}".lower().replace(' ', '-')
            
            return {
                'id': experience_id,
                'title': title,
                'category': category,
                'subcategory': subcategory,
                'tags': tags,
                'difficulty': difficulty,
                'tech_stack': tech_stack,
                'description': description,
                'content': content,
                'source': meta_info.get('来源', ''),
                'applicable_scope': meta_info.get('适用范围', '')
            }
            
        except Exception as e:
            print(f"解析Markdown文件 {md_file} 时出错: {e}")
            return None
    
    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """按关键词搜索（支持YAML和Markdown格式）"""
        results = []
        keyword_lower = keyword.lower()
        
        for exp in self.experiences:
            # 基础字段搜索
            if (keyword_lower in exp.get('title', '').lower() or
                keyword_lower in exp.get('description', '').lower() or
                any(keyword_lower in tag.lower() for tag in exp.get('tags', [])) or
                keyword_lower in exp.get('category', '').lower() or
                keyword_lower in exp.get('subcategory', '').lower()):
                results.append(exp)
                continue
            
            # 对于Markdown格式，也搜索内容
            if exp.get('format') == 'markdown':
                content = exp.get('content', '')
                if keyword_lower in content.lower():
                    results.append(exp)
                    continue
            
            # 对于YAML格式，搜索解决方案等字段
            if exp.get('format') == 'yaml':
                solution = exp.get('solution', {})
                if isinstance(solution, dict):
                    if (keyword_lower in solution.get('approach', '').lower() or
                        keyword_lower in solution.get('implementation', '').lower()):
                        results.append(exp)
                        continue
        
        return results
    
    def search_by_tech_stack(self, tech: str) -> List[Dict[str, Any]]:
        """按技术栈搜索"""
        results = []
        tech_lower = tech.lower()
        
        for exp in self.experiences:
            tech_stack = exp.get('tech_stack', [])
            if any(tech_lower in stack.lower() for stack in tech_stack):
                results.append(exp)
        
        return results
    
    def search_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """按难度搜索"""
        return [exp for exp in self.experiences 
                if exp.get('difficulty', '').lower() == difficulty.lower()]
    
    def search_by_category(self, category: str, subcategory: str = None) -> List[Dict[str, Any]]:
        """按分类搜索"""
        results = []
        
        for exp in self.experiences:
            if exp.get('category', '').lower() == category.lower():
                if subcategory is None or exp.get('subcategory', '').lower() == subcategory.lower():
                    results.append(exp)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取经验库统计信息"""
        categories = {}
        difficulties = {}
        tech_stacks = {}
        
        for exp in self.experiences:
            # 统计分类
            cat = exp.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            # 统计难度
            diff = exp.get('difficulty', 'unknown')
            difficulties[diff] = difficulties.get(diff, 0) + 1
            
            # 统计技术栈
            for tech in exp.get('tech_stack', []):
                tech_stacks[tech] = tech_stacks.get(tech, 0) + 1
        
        return {
            'total_experiences': len(self.experiences),
            'categories': categories,
            'difficulties': difficulties,
            'top_tech_stacks': dict(sorted(tech_stacks.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def format_search_result(self, experience: Dict[str, Any]) -> str:
        """格式化搜索结果（支持YAML和Markdown格式）"""
        format_emoji = "📄" if experience.get('format') == 'markdown' else "🗂️"
        
        # 处理技术栈显示
        tech_stack = experience.get('tech_stack', [])
        tech_stack_str = ', '.join(tech_stack) if tech_stack else 'N/A'
        
        # 处理标签显示
        tags = experience.get('tags', [])
        tags_str = ', '.join(tags[:5]) if tags else 'N/A'  # 最多显示5个标签
        if len(tags) > 5:
            tags_str += f" (+{len(tags)-5}个更多)"
        
        result = f"""
📋 {experience.get('title', 'No Title')} {format_emoji}
🏷️  分类: {experience.get('category', 'N/A')} > {experience.get('subcategory', 'N/A')}
⭐ 难度: {experience.get('difficulty', 'N/A')}
🔧 技术栈: {tech_stack_str}
🏃 标签: {tags_str}
📝 描述: {experience.get('description', 'No description')}
📁 文件: {experience.get('file_path', 'N/A')}"""
        
        # 对于Markdown格式，显示来源信息
        if experience.get('format') == 'markdown':
            source = experience.get('source', '')
            if source:
                result += f"\n🎯 来源: {source}"
        
        return result

def main():
    parser = argparse.ArgumentParser(description='搜索软件工程经验库')
    parser.add_argument('-k', '--keyword', help='按关键词搜索')
    parser.add_argument('-t', '--tech', help='按技术栈搜索')
    parser.add_argument('-d', '--difficulty', help='按难度搜索 (beginner/intermediate/advanced/expert)')
    parser.add_argument('-c', '--category', help='按分类搜索')
    parser.add_argument('-s', '--subcategory', help='按子分类搜索 (需要与-c一起使用)')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--list', action='store_true', help='列出所有经验')
    
    args = parser.parse_args()
    
    searcher = ExperienceSearcher()
    
    if args.stats:
        stats = searcher.get_stats()
        print("📊 经验库统计信息:")
        print(f"总经验数: {stats['total_experiences']}")
        print(f"分类分布: {json.dumps(stats['categories'], ensure_ascii=False, indent=2)}")
        print(f"难度分布: {json.dumps(stats['difficulties'], ensure_ascii=False, indent=2)}")
        print(f"热门技术栈: {json.dumps(stats['top_tech_stacks'], ensure_ascii=False, indent=2)}")
        return
    
    results = []
    
    if args.keyword:
        results = searcher.search_by_keyword(args.keyword)
    elif args.tech:
        results = searcher.search_by_tech_stack(args.tech)
    elif args.difficulty:
        results = searcher.search_by_difficulty(args.difficulty)
    elif args.category:
        results = searcher.search_by_category(args.category, args.subcategory)
    elif args.list:
        results = searcher.experiences
    else:
        parser.print_help()
        return
    
    if not results:
        print("❌ 没有找到匹配的经验")
        return
    
    print(f"🔍 找到 {len(results)} 个相关经验:")
    for exp in results:
        print(searcher.format_search_result(exp))
        print("-" * 80)

if __name__ == "__main__":
    main()
