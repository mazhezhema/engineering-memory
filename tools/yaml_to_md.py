#!/usr/bin/env python3
"""
YAML经验转换为Markdown格式工具
将现有的YAML格式经验文件转换为统一的Markdown格式
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List
import argparse

class YamlToMarkdownConverter:
    def __init__(self):
        self.difficulty_stars = {
            'beginner': '⭐⭐',
            'intermediate': '⭐⭐⭐',
            'advanced': '⭐⭐⭐⭐',
            'expert': '⭐⭐⭐⭐⭐'
        }
    
    def convert_yaml_to_markdown(self, yaml_file: Path) -> str:
        """将单个YAML文件转换为Markdown格式"""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # 构建Markdown内容
            md_content = self.build_markdown_content(data)
            return md_content
            
        except Exception as e:
            print(f"转换文件 {yaml_file} 时出错: {e}")
            return ""
    
    def build_markdown_content(self, data: Dict[str, Any]) -> str:
        """构建Markdown内容"""
        lines = []
        
        # 标题
        title = data.get('title', '未命名经验')
        lines.append(f"# {title}")
        lines.append("")
        
        # 元信息块
        lines.append(self.build_meta_block(data))
        lines.append("")
        
        # 背景描述
        description = data.get('description', '')
        if description:
            lines.append("## 背景描述")
            lines.append("")
            lines.append(description)
            lines.append("")
        
        # 问题场景
        if 'problem' in data:
            lines.append("## 问题场景")
            lines.append("")
            problem = data['problem']
            
            if 'scenario' in problem:
                lines.append(f"**具体场景**: {problem['scenario']}")
                lines.append("")
            
            if 'challenges' in problem and problem['challenges']:
                lines.append("**面临挑战**:")
                for challenge in problem['challenges']:
                    lines.append(f"- {challenge}")
                lines.append("")
            
            if 'constraints' in problem and problem['constraints']:
                lines.append("**约束条件**:")
                for constraint in problem['constraints']:
                    lines.append(f"- {constraint}")
                lines.append("")
        
        # 解决方案
        if 'solution' in data:
            lines.append("## 解决方案")
            lines.append("")
            solution = data['solution']
            
            if 'approach' in solution:
                lines.append("### 解决思路")
                lines.append("")
                lines.append(solution['approach'])
                lines.append("")
            
            if 'implementation' in solution:
                lines.append("### 具体实现")
                lines.append("")
                lines.append(solution['implementation'])
                lines.append("")
            
            # 代码示例
            if 'code_examples' in solution and solution['code_examples']:
                lines.append("### 代码示例")
                lines.append("")
                
                for i, example in enumerate(solution['code_examples'], 1):
                    if 'filename' in example:
                        lines.append(f"#### {i}. {example['filename']}")
                    else:
                        lines.append(f"#### 示例 {i}")
                    lines.append("")
                    
                    if 'description' in example:
                        lines.append(example['description'])
                        lines.append("")
                    
                    if 'code' in example:
                        language = example.get('language', 'text')
                        lines.append(f"```{language}")
                        lines.append(example['code'])
                        lines.append("```")
                        lines.append("")
                    
                    if 'explanation' in example:
                        lines.append(f"**说明**: {example['explanation']}")
                        lines.append("")
        
        # 收益分析
        if 'benefits' in data:
            lines.append("## 收益分析")
            lines.append("")
            benefits = data['benefits']
            
            for key, value in benefits.items():
                if value:
                    key_chinese = self.translate_benefit_key(key)
                    lines.append(f"**{key_chinese}**: {value}")
                    lines.append("")
        
        # 权衡分析
        if 'tradeoffs' in data:
            lines.append("## 权衡分析")
            lines.append("")
            tradeoffs = data['tradeoffs']
            
            if 'pros' in tradeoffs and tradeoffs['pros']:
                lines.append("### 优势")
                for pro in tradeoffs['pros']:
                    lines.append(f"- ✅ {pro}")
                lines.append("")
            
            if 'cons' in tradeoffs and tradeoffs['cons']:
                lines.append("### 劣势")
                for con in tradeoffs['cons']:
                    lines.append(f"- ❌ {con}")
                lines.append("")
            
            if 'alternatives' in tradeoffs and tradeoffs['alternatives']:
                lines.append("### 替代方案")
                lines.append("")
                for alt in tradeoffs['alternatives']:
                    lines.append(f"**{alt['name']}**: {alt['description']}")
                    if 'pros' in alt and alt['pros']:
                        lines.append("- 优势: " + ", ".join(alt['pros']))
                    if 'cons' in alt and alt['cons']:
                        lines.append("- 劣势: " + ", ".join(alt['cons']))
                    lines.append("")
        
        # 适用场景
        if 'applicable_scenarios' in data and data['applicable_scenarios']:
            lines.append("## 适用场景")
            lines.append("")
            for scenario in data['applicable_scenarios']:
                lines.append(f"- {scenario}")
            lines.append("")
        
        # 注意事项
        if 'anti_patterns' in data and data['anti_patterns']:
            lines.append("## 注意事项")
            lines.append("")
            for anti_pattern in data['anti_patterns']:
                lines.append(f"- ⚠️ {anti_pattern}")
            lines.append("")
        
        # 相关经验
        if 'related_experiences' in data and data['related_experiences']:
            lines.append("## 相关经验")
            lines.append("")
            for related in data['related_experiences']:
                lines.append(f"- [{related}]({related})")
            lines.append("")
        
        # 更新记录
        if 'metadata' in data:
            lines.append("---")
            lines.append("")
            lines.append("**更新记录**:")
            metadata = data['metadata']
            created_date = metadata.get('created_at', '')
            updated_date = metadata.get('updated_at', '')
            author = metadata.get('author', '')
            source_project = metadata.get('source_project', '')
            
            if created_date:
                lines.append(f"- {created_date}: 创建")
            if updated_date and updated_date != created_date:
                lines.append(f"- {updated_date}: 更新")
            if author:
                lines.append(f"- 作者: {author}")
            if source_project:
                lines.append(f"- 来源项目: {source_project}")
        
        return "\n".join(lines)
    
    def build_meta_block(self, data: Dict[str, Any]) -> str:
        """构建元信息块"""
        lines = []
        
        # 来源信息
        metadata = data.get('metadata', {})
        source_project = metadata.get('source_project', '')
        if source_project:
            lines.append(f"> **来源**: {source_project}")
        
        # 适用范围
        category = data.get('category', '')
        subcategory = data.get('subcategory', '')
        if category and subcategory:
            lines.append(f"> **适用范围**: {category.title()}项目的{subcategory}相关问题")
        
        # 难度等级
        difficulty = data.get('difficulty', 'intermediate')
        stars = self.difficulty_stars.get(difficulty, '⭐⭐⭐')
        lines.append(f"> **难度等级**: {stars}")
        
        # 技术栈
        tech_stack = data.get('tech_stack', [])
        if tech_stack:
            tech_str = ', '.join(tech_stack)
            lines.append(f"> **技术栈**: {tech_str}")
        
        return '\n'.join(lines)
    
    def translate_benefit_key(self, key: str) -> str:
        """翻译收益字段名"""
        translations = {
            'performance_gain': '性能提升',
            'maintainability': '可维护性',
            'scalability': '可扩展性',
            'cost_reduction': '成本降低'
        }
        return translations.get(key, key.replace('_', ' ').title())
    
    def convert_file(self, yaml_file: Path, output_dir: Path = None) -> bool:
        """转换单个文件"""
        if not yaml_file.exists():
            print(f"文件不存在: {yaml_file}")
            return False
        
        # 生成Markdown内容
        md_content = self.convert_yaml_to_markdown(yaml_file)
        if not md_content:
            return False
        
        # 确定输出路径
        if output_dir is None:
            output_dir = yaml_file.parent
        
        output_file = output_dir / f"{yaml_file.stem}.md"
        
        # 写入Markdown文件
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"✅ 转换完成: {yaml_file} → {output_file}")
            return True
        except Exception as e:
            print(f"❌ 写入文件失败 {output_file}: {e}")
            return False
    
    def convert_directory(self, experiences_dir: Path) -> None:
        """转换整个目录的YAML文件"""
        yaml_files = list(experiences_dir.rglob("*.yaml"))
        
        if not yaml_files:
            print("未找到YAML文件")
            return
        
        print(f"找到 {len(yaml_files)} 个YAML文件")
        
        success_count = 0
        for yaml_file in yaml_files:
            if self.convert_file(yaml_file):
                success_count += 1
        
        print(f"\n转换完成: {success_count}/{len(yaml_files)} 个文件成功")

def main():
    parser = argparse.ArgumentParser(description='将YAML经验转换为Markdown格式')
    parser.add_argument('path', nargs='?', default='experiences', 
                       help='要转换的YAML文件或包含YAML文件的目录')
    parser.add_argument('-o', '--output', 
                       help='输出目录（默认为原文件同目录）')
    
    args = parser.parse_args()
    
    converter = YamlToMarkdownConverter()
    path = Path(args.path)
    
    if path.is_file() and path.suffix == '.yaml':
        # 转换单个文件
        output_dir = Path(args.output) if args.output else None
        converter.convert_file(path, output_dir)
    elif path.is_dir():
        # 转换整个目录
        converter.convert_directory(path)
    else:
        print(f"❌ 无效路径或非YAML文件: {path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
