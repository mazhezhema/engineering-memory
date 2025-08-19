# 软件工程经验库 (Engineering Memory)

## 项目简介

本项目是一个专门收集、整理和分享来自真实Cursor项目的软件工程经验知识库。通过系统化地记录开发过程中的最佳实践、常见问题解决方案、架构决策和代码模式，帮助新项目快速获得成熟的软件工程经验。

## 核心特性

- **经验收集**: 结构化收集来自真实项目的开发经验
- **智能分类**: 按技术栈、问题域、复杂度等维度组织经验
- **快速检索**: 支持关键词、标签、场景等多维度搜索
- **模板复用**: 提供可直接应用的代码模板和最佳实践
- **持续更新**: 支持经验的版本管理和迭代更新

## 项目结构

```
engineering-memory/
├── experiences/              # 📚 经验库主目录
│   ├── 01-core-principles/      # 🧠 核心工程原则
│   │   ├── error-analysis-framework.md      # 错误分析方法论
│   │   ├── technical-debt-management.md     # 技术债务管理
│   │   └── fundamental-laws.md              # 软件工程基本法则
│   ├── 02-frontend/            # 🎨 前端开发经验
│   │   ├── flutter/               # Flutter框架专题
│   │   ├── react/                 # React框架专题
│   │   └── general/               # 通用前端经验
│   ├── 03-backend/             # ⚙️ 后端开发经验
│   │   ├── python/                # Python技术栈
│   │   ├── nodejs/                # Node.js技术栈
│   │   └── general/               # 通用后端经验
│   ├── 04-database/            # 🗄️ 数据库经验
│   │   ├── postgresql/            # PostgreSQL专题
│   │   ├── nosql/                 # NoSQL数据库
│   │   └── migration/             # 数据迁移经验
│   ├── 05-devops/              # 🚀 DevOps经验
│   │   ├── ci-cd/                 # 持续集成/部署
│   │   ├── monitoring/            # 监控和可观测性
│   │   └── infrastructure/        # 基础设施管理
│   ├── 06-ai-collaboration/    # 🤖 AI协作开发
│   │   ├── cursor-workflows/      # Cursor工作流程
│   │   ├── code-review/           # AI辅助代码审查
│   │   └── automation/            # 智能自动化
│   ├── architecture/           # 📐 架构设计经验
│   ├── patterns/              # 🔧 设计模式和代码模式
│   ├── debugging/             # 🐛 调试和问题解决
│   ├── performance/           # ⚡ 性能优化经验
│   ├── testing/               # 🧪 测试策略和实践
│   └── deployment/            # 📦 部署和运维经验
├── case-studies/            # 📖 实战案例研究
│   ├── success-stories/         # 成功案例分析
│   ├── failure-analysis/        # 失败教训总结
│   └── transformation-journeys/ # 项目转型历程
├── templates/               # 📋 可复用模板
├── tools/                  # 🛠️ 经验管理工具
├── docs/                   # 📄 项目文档
└── scripts/                # 🔧 自动化脚本
```

## 经验格式标准

每个经验条目采用**Markdown格式**，包含：
- **元信息块**: 来源项目、适用范围、难度等级、技术栈
- **背景描述**: 问题产生的背景和环境
- **问题场景**: 具体遇到的问题和挑战
- **解决方案**: 解决思路、具体实现、代码示例
- **收益分析**: 性能提升、可维护性改善等
- **权衡分析**: 优劣势对比和替代方案
- **适用场景**: 何时使用该解决方案
- **注意事项**: 需要避免的反模式
- **相关经验**: 关联的其他经验条目

## 快速开始

### 🔍 搜索经验
```bash
# 按关键词搜索
python tools/search.py -k "react"

# 按技术栈搜索  
python tools/search.py -t "PostgreSQL"

# 按难度搜索
python tools/search.py -d "advanced"

# 按分类搜索
python tools/search.py -c "performance"

# 查看统计信息
python tools/search.py --stats

# 列出所有经验
python tools/search.py --list
```

### 📝 贡献经验
1. 复制经验模板 `templates/quick-template.md`
2. 填写完整的经验信息
3. 放置在相应的分类目录下
4. 使用验证工具检查格式：`python tools/validate.py your-file.md`

### 🛠️ 工具使用
- **搜索工具**: `tools/search.py` - 支持多维度搜索经验
- **验证工具**: `tools/validate.py` - 检查经验格式和质量
- **转换工具**: `tools/yaml_to_md.py` - YAML转Markdown（已弃用）

## 贡献指南

欢迎贡献你的项目经验！请参考[贡献指南](docs/CONTRIBUTING.md)了解如何提交经验。

## 许可证

MIT License
