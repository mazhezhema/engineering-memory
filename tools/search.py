#!/usr/bin/env python3
"""
经验库搜索工具
支持按关键词、标签、技术栈、难度等维度搜索经验
"""

import os
import yaml
import json
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path
import argparse

class ExperienceSearcher:
    def __init__(self, experiences_dir: str = "experiences"):
        self.experiences_dir = Path(experiences_dir)
        self.experiences = []
        self.load_experiences()
    
    def load_experiences(self):
        """加载所有经验文件"""
        self.experiences = []
        
        for yaml_file in self.experiences_dir.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    experience = yaml.safe_load(f)
                    experience['file_path'] = str(yaml_file)
                    self.experiences.append(experience)
            except Exception as e:
                print(f"错误: 无法加载 {yaml_file}: {e}")
    
    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """按关键词搜索"""
        results = []
        keyword_lower = keyword.lower()
        
        for exp in self.experiences:
            # 搜索标题、描述、标签
            if (keyword_lower in exp.get('title', '').lower() or
                keyword_lower in exp.get('description', '').lower() or
                any(keyword_lower in tag.lower() for tag in exp.get('tags', [])) or
                keyword_lower in exp.get('category', '').lower() or
                keyword_lower in exp.get('subcategory', '').lower()):
                results.append(exp)
        
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
        """格式化搜索结果"""
        return f"""
📋 {experience.get('title', 'No Title')}
🏷️  分类: {experience.get('category', 'N/A')} > {experience.get('subcategory', 'N/A')}
⭐ 难度: {experience.get('difficulty', 'N/A')}
🔧 技术栈: {', '.join(experience.get('tech_stack', []))}
📝 描述: {experience.get('description', 'No description')}
📁 文件: {experience.get('file_path', 'N/A')}
"""

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
