#!/usr/bin/env python3
"""
经验库验证工具
检查经验条目的格式、完整性和质量
"""

import os
import yaml
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path
import argparse

class ExperienceValidator:
    def __init__(self):
        self.required_fields = [
            'id', 'title', 'category', 'subcategory', 'tags', 
            'difficulty', 'tech_stack', 'description'
        ]
        self.valid_categories = [
            'architecture', 'patterns', 'debugging', 
            'performance', 'testing', 'deployment'
        ]
        self.valid_difficulties = [
            'beginner', 'intermediate', 'advanced', 'expert'
        ]
        self.errors = []
        self.warnings = []
    
    def validate_file(self, file_path: Path) -> Dict[str, Any]:
        """验证单个经验文件"""
        self.errors = []
        self.warnings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"文件解析错误: {e}")
            return {'valid': False, 'errors': self.errors, 'warnings': self.warnings}
        
        # 检查必需字段
        self._check_required_fields(data)
        
        # 检查字段格式
        self._check_field_formats(data)
        
        # 检查内容质量
        self._check_content_quality(data)
        
        # 检查文件命名
        self._check_file_naming(file_path, data)
        
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def _check_required_fields(self, data: Dict[str, Any]):
        """检查必需字段"""
        for field in self.required_fields:
            if field not in data:
                self.errors.append(f"缺少必需字段: {field}")
            elif not data[field]:
                self.errors.append(f"字段 {field} 不能为空")
    
    def _check_field_formats(self, data: Dict[str, Any]):
        """检查字段格式"""
        # 检查分类
        if 'category' in data:
            if data['category'] not in self.valid_categories:
                self.errors.append(f"无效的分类: {data['category']}")
        
        # 检查难度
        if 'difficulty' in data:
            if data['difficulty'] not in self.valid_difficulties:
                self.errors.append(f"无效的难度: {data['difficulty']}")
        
        # 检查标签格式
        if 'tags' in data:
            if not isinstance(data['tags'], list):
                self.errors.append("tags 字段必须是数组")
            elif len(data['tags']) == 0:
                self.warnings.append("建议添加至少一个标签")
        
        # 检查技术栈格式
        if 'tech_stack' in data:
            if not isinstance(data['tech_stack'], list):
                self.errors.append("tech_stack 字段必须是数组")
        
        # 检查ID格式
        if 'id' in data:
            expected_pattern = f"{data.get('category', '')}-"
            if not data['id'].startswith(expected_pattern):
                self.warnings.append(f"ID建议以 {expected_pattern} 开头")
    
    def _check_content_quality(self, data: Dict[str, Any]):
        """检查内容质量"""
        # 检查描述长度
        if 'description' in data:
            desc_len = len(data['description'])
            if desc_len < 20:
                self.warnings.append("描述过短，建议至少20个字符")
            elif desc_len > 200:
                self.warnings.append("描述过长，建议控制在200个字符内")
        
        # 检查是否有解决方案
        if 'solution' not in data:
            self.errors.append("缺少 solution 字段")
        elif not data['solution'].get('approach'):
            self.errors.append("solution.approach 不能为空")
        
        # 检查代码示例
        solution = data.get('solution', {})
        code_examples = solution.get('code_examples', [])
        if not code_examples:
            self.warnings.append("建议添加代码示例")
        else:
            for i, example in enumerate(code_examples):
                if not example.get('language'):
                    self.errors.append(f"代码示例 {i+1} 缺少 language 字段")
                if not example.get('code'):
                    self.errors.append(f"代码示例 {i+1} 缺少 code 字段")
        
        # 检查元数据
        metadata = data.get('metadata', {})
        if not metadata.get('author'):
            self.warnings.append("建议添加作者信息")
        if not metadata.get('created_at'):
            self.warnings.append("建议添加创建日期")
        
        quality_score = metadata.get('quality_score', 0)
        if quality_score < 5:
            self.warnings.append("质量评分较低，建议改进内容")
    
    def _check_file_naming(self, file_path: Path, data: Dict[str, Any]):
        """检查文件命名规范"""
        filename = file_path.stem
        category = data.get('category', '')
        
        # 检查文件是否在正确的目录
        if category and category not in str(file_path.parent):
            self.warnings.append(f"文件应该放在 {category} 目录下")
        
        # 检查文件名是否包含年份
        if '2024' not in filename and '2023' not in filename:
            self.warnings.append("建议在文件名中包含年份")
    
    def validate_directory(self, experiences_dir: str) -> Dict[str, Any]:
        """验证整个经验库目录"""
        experiences_path = Path(experiences_dir)
        results = {}
        total_files = 0
        valid_files = 0
        
        for yaml_file in experiences_path.rglob("*.yaml"):
            total_files += 1
            result = self.validate_file(yaml_file)
            results[str(yaml_file)] = result
            
            if result['valid']:
                valid_files += 1
        
        return {
            'total_files': total_files,
            'valid_files': valid_files,
            'results': results
        }

def main():
    parser = argparse.ArgumentParser(description='验证经验库文件')
    parser.add_argument('path', nargs='?', default='experiences', 
                       help='要验证的文件或目录路径')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    validator = ExperienceValidator()
    path = Path(args.path)
    
    if path.is_file():
        # 验证单个文件
        result = validator.validate_file(path)
        
        print(f"📋 验证文件: {path}")
        
        if result['valid']:
            print("✅ 文件格式正确")
        else:
            print("❌ 文件存在错误")
        
        if result['errors']:
            print("\n🚨 错误:")
            for error in result['errors']:
                print(f"  - {error}")
        
        if result['warnings']:
            print("\n⚠️  警告:")
            for warning in result['warnings']:
                print(f"  - {warning}")
    
    elif path.is_dir():
        # 验证整个目录
        results = validator.validate_directory(str(path))
        
        print(f"📁 验证目录: {path}")
        print(f"总文件数: {results['total_files']}")
        print(f"有效文件数: {results['valid_files']}")
        print(f"验证通过率: {results['valid_files']}/{results['total_files']} ({results['valid_files']/max(results['total_files'], 1)*100:.1f}%)")
        
        if args.verbose:
            print("\n📊 详细结果:")
            for file_path, result in results['results'].items():
                status = "✅" if result['valid'] else "❌"
                print(f"{status} {file_path}")
                
                if result['errors']:
                    for error in result['errors']:
                        print(f"    🚨 {error}")
                
                if result['warnings']:
                    for warning in result['warnings']:
                        print(f"    ⚠️  {warning}")
        else:
            # 只显示有问题的文件
            problem_files = [
                (path, result) for path, result in results['results'].items() 
                if not result['valid'] or result['warnings']
            ]
            
            if problem_files:
                print("\n⚠️  需要注意的文件:")
                for file_path, result in problem_files:
                    status = "❌" if not result['valid'] else "⚠️ "
                    print(f"{status} {file_path}")
    
    else:
        print(f"❌ 路径不存在: {path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
