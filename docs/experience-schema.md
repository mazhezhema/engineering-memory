# 经验条目数据模型 (Experience Schema)

## 核心数据结构

### 经验条目 (Experience Entry)

```yaml
id: string                    # 唯一标识符
title: string                 # 经验标题
category: string              # 主分类
subcategory: string           # 子分类
tags: string[]                # 标签列表
difficulty: enum              # 难度等级: beginner | intermediate | advanced | expert
tech_stack: string[]          # 相关技术栈
description: string           # 简短描述
context:                      # 背景信息
  project_type: string        # 项目类型
  team_size: number          # 团队规模
  timeline: string           # 时间线
  business_domain: string    # 业务领域
problem:                      # 问题描述
  scenario: string           # 具体场景
  challenges: string[]       # 面临的挑战
  constraints: string[]      # 约束条件
solution:                     # 解决方案
  approach: string           # 解决思路
  implementation: string     # 具体实现
  code_examples: CodeExample[] # 代码示例
  architecture_diagram: string # 架构图路径
benefits:                     # 收益
  performance_gain: string   # 性能提升
  maintainability: string    # 可维护性
  scalability: string        # 可扩展性
  cost_reduction: string     # 成本降低
tradeoffs:                    # 权衡
  pros: string[]             # 优势
  cons: string[]             # 劣势
  alternatives: Alternative[] # 替代方案
applicable_scenarios: string[] # 适用场景
anti_patterns: string[]       # 反模式提醒
related_experiences: string[] # 相关经验ID
metadata:                     # 元数据
  author: string             # 作者
  source_project: string     # 来源项目
  created_at: date           # 创建时间
  updated_at: date           # 更新时间
  version: string            # 版本号
  review_status: enum        # 审核状态: draft | reviewed | published
  quality_score: number      # 质量评分 (1-10)
```

### 代码示例 (Code Example)

```yaml
language: string              # 编程语言
filename: string              # 文件名
description: string           # 代码说明
code: string                  # 代码内容
explanation: string           # 解释说明
highlight_lines: number[]     # 重点行号
related_files: string[]       # 相关文件
```

### 替代方案 (Alternative)

```yaml
name: string                  # 方案名称
description: string           # 方案描述
pros: string[]                # 优势
cons: string[]                # 劣势
implementation_effort: enum   # 实现难度: low | medium | high
```

## 分类体系

### 主分类 (Categories)

1. **architecture** - 架构设计
   - microservices - 微服务架构
   - monolith - 单体架构
   - serverless - 无服务器架构
   - event-driven - 事件驱动架构
   - layered - 分层架构

2. **patterns** - 设计模式
   - creational - 创建型模式
   - structural - 结构型模式
   - behavioral - 行为型模式
   - architectural - 架构模式
   - integration - 集成模式

3. **debugging** - 调试和问题解决
   - performance-issues - 性能问题
   - memory-leaks - 内存泄漏
   - concurrency-bugs - 并发问题
   - integration-failures - 集成失败
   - deployment-issues - 部署问题

4. **performance** - 性能优化
   - database-optimization - 数据库优化
   - caching-strategies - 缓存策略
   - frontend-optimization - 前端优化
   - api-optimization - API优化
   - infrastructure-tuning - 基础设施调优

5. **testing** - 测试策略
   - unit-testing - 单元测试
   - integration-testing - 集成测试
   - e2e-testing - 端到端测试
   - performance-testing - 性能测试
   - security-testing - 安全测试

6. **deployment** - 部署和运维
   - ci-cd - 持续集成/部署
   - containerization - 容器化
   - monitoring - 监控
   - logging - 日志管理
   - security - 安全配置

### 难度等级定义

- **beginner**: 初学者级别，基础概念和简单实现
- **intermediate**: 中级水平，需要一定经验和理解
- **advanced**: 高级水平，需要深入理解和复杂实现
- **expert**: 专家级别，需要丰富经验和创新思维

### 质量评分标准

- **9-10分**: 优秀 - 完整、准确、有深度见解
- **7-8分**: 良好 - 内容完整，有实用价值
- **5-6分**: 一般 - 基本完整，需要改进
- **3-4分**: 较差 - 内容不完整或有错误
- **1-2分**: 很差 - 内容严重不足或错误较多
