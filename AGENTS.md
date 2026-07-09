# OpenCode 智能体集群最高元规则

1. 【严格状态回滚】外环（Reviewer/Implementer）对代码的任何物理修改，必须无条件触发内环（Tester）的回归测试。未经过 Tester 确认的代码严禁交付。
2. 【原子化熔断】任何子代理之间的局部循环（如 Test-Debug）最大重试次数为 3 次。达到上限必须向 Builder 提交 Failure Summary 并挂起。
3. 【技能先导】Planner 与 Architect 在承接任务后，第一动作必须是检索 `knowledge/skills/`，严禁重复造轮子。
4. 【无代码中转】Builder 严禁读取、存储、中转任何具体的代码片段，仅允许处理状态码与 Summary JSON。
