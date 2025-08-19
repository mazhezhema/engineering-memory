# 贡献指南

感谢你对软件工程经验库的贡献！本指南将帮助你了解如何提交高质量的经验条目。

## 贡献流程

### 1. 准备工作

1. Fork 这个仓库到你的 GitHub 账户
2. Clone 你的 Fork 到本地
3. 创建新的分支进行开发

```bash
git clone https://github.com/你的用户名/engineering-memory.git
cd engineering-memory
git checkout -b add-new-experience
```

### 2. 创建经验条目

1. 确定经验分类和存放位置
2. 使用模板创建新的经验文件
3. 填写完整的经验信息

```bash
# 复制模板文件
cp templates/experience-template.yaml experiences/分类/你的经验名称-YYYY.yaml
```

### 3. 填写经验内容

参考 [经验条目数据模型](experience-schema.md) 填写完整信息：

#### 必填字段
- `id`: 唯一标识符，格式为 `category-subcategory-brief-name-YYYY`
- `title`: 简洁明确的标题
- `category`: 主分类
- `description`: 1-2句话的简短描述
- `problem`: 问题描述和背景
- `solution`: 解决方案和实现

#### 建议填写
- `code_examples`: 具体的代码示例
- `benefits`: 解决方案带来的收益
- `tradeoffs`: 优劣势分析
- `applicable_scenarios`: 适用场景

### 4. 质量标准

#### 内容质量要求

1. **真实性**: 必须来自真实项目经验
2. **完整性**: 包含问题背景、解决方案、代码示例
3. **实用性**: 对其他开发者有参考价值
4. **准确性**: 技术信息准确，代码可运行

#### 代码示例要求

```yaml
code_examples:
  - language: "typescript"
    filename: "components/UserProfile.tsx"
    description: "用户资料组件实现"
    code: |
      import React from 'react';
      
      interface UserProfileProps {
        user: User;
        onUpdate: (user: User) => void;
      }
      
      export const UserProfile: React.FC<UserProfileProps> = ({
        user,
        onUpdate
      }) => {
        // 组件实现
      };
    explanation: "使用TypeScript接口确保类型安全"
    highlight_lines: [3, 8]
    related_files: ["types/User.ts", "hooks/useUser.ts"]
```

#### 文档规范

- 使用中文编写，表达清晰准确
- 代码注释使用英文或中文都可以
- 避免使用过于技术性的术语，适当解释专业概念
- 包含足够的上下文信息

### 5. 验证和测试

提交前使用验证工具检查格式：

```bash
# 验证单个文件
python tools/validate.py experiences/patterns/你的文件.yaml

# 验证整个目录
python tools/validate.py experiences/

# 搜索测试
python tools/search.py -k "你的关键词"
```

### 6. 提交和Pull Request

1. 提交你的更改
```bash
git add experiences/你的分类/你的文件.yaml
git commit -m "feat: 添加React组件组合模式经验"
git push origin add-new-experience
```

2. 创建 Pull Request
   - 标题简洁明确
   - 描述包含经验要点
   - 添加相关标签

### 7. 代码审查

维护者会审查你的提交，可能会要求：

- 补充缺失的信息
- 修正技术错误
- 改进代码示例
- 调整分类或标签

## 经验类型和示例

### 架构设计 (architecture)
- 微服务拆分策略
- API设计模式
- 数据库设计决策
- 系统集成方案

### 设计模式 (patterns)
- 创建型、结构型、行为型模式
- 前端组件设计模式
- 后端服务设计模式

### 调试技巧 (debugging)
- 性能问题排查
- 内存泄漏定位
- 线上故障处理
- 日志分析技巧

### 性能优化 (performance)
- 数据库查询优化
- 前端渲染优化
- 缓存策略设计
- 代码性能调优

### 测试策略 (testing)
- 单元测试最佳实践
- 集成测试设计
- 端到端测试自动化
- 性能测试方案

### 部署运维 (deployment)
- CI/CD流水线设计
- 容器化最佳实践
- 监控告警配置
- 蓝绿部署策略

## 常见问题

### Q: 我的经验不够复杂，值得分享吗？
A: 即使是简单的经验也可能对他人有帮助。关键是要真实和实用。

### Q: 可以分享失败的经验吗？
A: 当然可以！失败经验往往更有价值，可以帮助其他人避免同样的错误。

### Q: 如何确定经验的分类？
A: 参考 [经验条目数据模型](experience-schema.md) 中的分类体系，或在issue中询问。

### Q: 代码示例需要完整可运行吗？
A: 建议提供关键部分的代码，不需要完整项目，但要确保代码逻辑正确。

### Q: 可以引用开源项目的代码吗？
A: 可以，但要注明来源，并确保符合相关开源协议。

## 联系方式

如有问题，可以通过以下方式联系：

- 创建 Issue 讨论
- 发起 Discussion
- 邮件联系维护者

感谢你的贡献！🎉
