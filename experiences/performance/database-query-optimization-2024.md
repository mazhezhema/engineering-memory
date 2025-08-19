# PostgreSQL查询优化解决订单列表性能问题

> **来源**: 电商平台性能优化
> **适用范围**: Performance项目的database-optimization相关问题
> **难度等级**: ⭐⭐⭐⭐
> **技术栈**: PostgreSQL 14, Node.js, Prisma ORM, Redis

## 背景描述

通过索引优化和查询重构，将订单列表接口响应时间从5秒降至200ms

## 问题场景

**具体场景**: 用户订单列表页面加载缓慢，在订单量达到100万时，接口响应时间超过5秒，用户体验极差

**面临挑战**:
- 复杂的多表关联查询
- 缺乏合适的数据库索引
- N+1查询问题
- 大量数据的分页效率低

**约束条件**:
- 不能修改现有数据结构
- 必须保持API兼容性
- 需要在生产环境验证效果

## 解决方案

### 解决思路

分析慢查询日志，识别性能瓶颈，通过添加复合索引和查询优化解决问题

### 具体实现

1. 开启PostgreSQL慢查询日志分析
2. 使用EXPLAIN ANALYZE分析查询执行计划
3. 添加针对性的复合索引
4. 重构ORM查询避免N+1问题
5. 实现查询结果缓存


### 代码示例

#### 1. migrations/add_order_indexes.sql

添加订单查询优化索引

```sql
-- 分析原始查询
EXPLAIN ANALYZE 
SELECT o.id, o.order_number, o.status, o.created_at, o.total_amount,
       u.name as user_name, u.email,
       COUNT(oi.id) as item_count
FROM orders o
JOIN users u ON o.user_id = u.id  
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = $1 
  AND o.created_at >= $2 
  AND o.status IN ('pending', 'processing', 'completed')
GROUP BY o.id, u.name, u.email
ORDER BY o.created_at DESC
LIMIT 20 OFFSET 0;

-- 执行计划显示：Seq Scan on orders (cost=0.00..25000.00 rows=100000)

-- 添加复合索引优化查询
CREATE INDEX CONCURRENTLY idx_orders_user_created_status 
ON orders (user_id, created_at DESC, status) 
WHERE status IN ('pending', 'processing', 'completed');

-- 优化order_items的关联查询
CREATE INDEX CONCURRENTLY idx_order_items_order_id 
ON order_items (order_id);

-- 添加覆盖索引避免回表查询
CREATE INDEX CONCURRENTLY idx_orders_list_covering
ON orders (user_id, created_at DESC) 
INCLUDE (id, order_number, status, total_amount)
WHERE status IN ('pending', 'processing', 'completed');

```

**说明**: 通过复合索引和覆盖索引大幅提升查询性能

#### 2. services/order.service.ts

优化后的订单查询服务

```typescript
import { PrismaClient } from '@prisma/client';
import Redis from 'ioredis';

export class OrderService {
  constructor(
    private prisma: PrismaClient,
    private redis: Redis
  ) {}
  
  async getUserOrders(
    userId: number, 
    page: number = 1, 
    limit: number = 20,
    fromDate?: Date
  ) {
    const cacheKey = `user_orders:${userId}:${page}:${limit}:${fromDate?.getTime()}`;
    
    // 尝试从缓存获取
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }
    
    // 优化后的查询 - 避免N+1问题
    const orders = await this.prisma.order.findMany({
      where: {
        userId,
        createdAt: fromDate ? { gte: fromDate } : undefined,
        status: { in: ['pending', 'processing', 'completed'] }
      },
      include: {
        user: {
          select: { name: true, email: true }
        },
        orderItems: {
          select: { id: true }, // 只选择需要的字段
          // 如果只需要数量，使用聚合查询更高效
        }
      },
      orderBy: { createdAt: 'desc' },
      skip: (page - 1) * limit,
      take: limit
    });
    
    // 优化: 使用单独的聚合查询获取item数量
    const orderIds = orders.map(o => o.id);
    const itemCounts = await this.prisma.orderItem.groupBy({
      by: ['orderId'],
      where: { orderId: { in: orderIds } },
      _count: { id: true }
    });
    
    const itemCountMap = new Map(
      itemCounts.map(ic => [ic.orderId, ic._count.id])
    );
    
    // 组装结果
    const result = {
      data: orders.map(order => ({
        id: order.id,
        orderNumber: order.orderNumber,
        status: order.status,
        createdAt: order.createdAt,
        totalAmount: order.totalAmount,
        userName: order.user.name,
        userEmail: order.user.email,
        itemCount: itemCountMap.get(order.id) || 0
      })),
      pagination: {
        page,
        limit,
        total: await this.getTotalCount(userId, fromDate)
      }
    };
    
    // 缓存结果5分钟
    await this.redis.setex(cacheKey, 300, JSON.stringify(result));
    
    return result;
  }
  
  private async getTotalCount(userId: number, fromDate?: Date) {
    // 使用缓存的总数，避免每次查询都count
    const countCacheKey = `user_orders_count:${userId}:${fromDate?.getTime()}`;
    const cachedCount = await this.redis.get(countCacheKey);
    
    if (cachedCount) {
      return parseInt(cachedCount);
    }
    
    const count = await this.prisma.order.count({
      where: {
        userId,
        createdAt: fromDate ? { gte: fromDate } : undefined,
        status: { in: ['pending', 'processing', 'completed'] }
      }
    });
    
    // 缓存总数10分钟
    await this.redis.setex(countCacheKey, 600, count.toString());
    
    return count;
  }
}

```

**说明**: 通过分离聚合查询、添加缓存、优化字段选择来提升性能

#### 3. monitoring/query-monitor.ts

查询性能监控工具

```typescript
import { PrismaClient } from '@prisma/client';

export class QueryMonitor {
  static setupPrismaLogging(prisma: PrismaClient) {
    // 监控慢查询
    prisma.$use(async (params, next) => {
      const start = Date.now();
      const result = await next(params);
      const duration = Date.now() - start;
      
      // 记录超过100ms的查询
      if (duration > 100) {
        console.warn(`Slow query detected:`, {
          model: params.model,
          action: params.action,
          duration: `${duration}ms`,
          args: JSON.stringify(params.args, null, 2)
        });
      }
      
      return result;
    });
  }
  
  static async analyzeQueryPerformance() {
    // 可以集成到监控系统中
    const slowQueries = await this.getSlowQueries();
    
    slowQueries.forEach(query => {
      if (query.duration > 1000) {
        // 发送告警
        this.sendAlert(query);
      }
    });
  }
  
  private static async getSlowQueries() {
    // 从数据库日志或监控系统获取慢查询
    // 这里是示例实现
    return [];
  }
  
  private static sendAlert(query: any) {
    // 发送告警到团队
    console.error('Critical slow query:', query);
  }
}

```

**说明**: 添加查询性能监控，及时发现和解决性能问题

## 收益分析

**性能提升**: 订单列表接口响应时间从5秒降至200ms，性能提升25倍

**可维护性**: 添加了监控机制，能及时发现新的性能问题

**可扩展性**: 优化后系统可支持更大的数据量和并发访问

**成本降低**: 减少数据库CPU使用率60%，降低了服务器成本

## 权衡分析

### 优势
- ✅ 显著提升查询性能
- ✅ 添加了缓存机制提高响应速度
- ✅ 建立了性能监控体系

### 劣势
- ❌ 增加了索引维护成本
- ❌ 缓存增加了数据一致性复杂度
- ❌ 需要定期分析和优化索引

### 替代方案

**读写分离方案**: 使用读库分担查询压力
- 优势: 减少主库压力, 提高并发能力
- 劣势: 增加架构复杂度, 数据同步延迟

**分表分库方案**: 按用户或时间维度分片
- 优势: 支持更大数据量, 线性扩展
- 劣势: 查询复杂度增加, 跨片事务困难

## 适用场景

- 大数据量的查询性能优化
- 复杂多表关联查询优化
- 高并发场景下的数据库性能调优
- 电商订单、用户行为等海量数据查询

## 注意事项

- ⚠️ 避免过度创建索引，要根据实际查询模式设计
- ⚠️ 不要忽略索引的维护成本和存储开销
- ⚠️ 避免缓存所有查询结果，要考虑数据更新频率
- ⚠️ 不要依赖ORM自动生成的查询，关键路径要手动优化

---

**更新记录**:
- 2024-01-20: 创建
- 作者: 李四
- 来源项目: 电商平台性能优化