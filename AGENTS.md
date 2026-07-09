# OpenCode 智能体集群最高元规则

1. 【严格状态回滚】外环（Reviewer/Implementer）对代码的任何物理修改，必须无条件触发内环（Tester）的回归测试。未经过 Tester 确认的代码严禁交付。
2. 【原子化熔断】任何子代理之间的局部循环（如 Test-Debug）最大重试次数为 3 次。达到上限必须向 Builder 提交 Failure Summary 并挂起。
3. 【生态与参考先导】Planner 与 Architect 在承接任务后，第一动作必须是检索 knowledge/skills/、knowledge/boilerplates/ 以及由 @reference-miner 动态抓取的 knowledge/references/。严禁凭空盲写，凡有成熟开源实现或脚手架的，必须优先借调或临摹。
4. 【无代码中转】Builder 严禁读取、存储、中转任何具体的代码片段，仅允许处理状态码与 Summary JSON。
5. 【影子沙箱隔离】@reference-miner 的一切克隆与解压行为，必须在独立的本地沙箱 .opencode_tmp/sandbox/ 中进行，禁止其直接接触生产源码区。
6. 【状态持久化】Builder 必须在每次操作前后读写 knowledge/state/current.json。状态文件丢失时必须重建。这是对抗上下文压缩和会话重启的唯一保障。
7. 【协议校验强制】所有子代理的返回结果必须通过 JSON Schema 校验。缺少 status、summary、artifacts、issues 任一字段的响应必须被拒绝并重试。非 JSON 响应必须被拒绝并重试。
8. 【并行加速】当 RESEARCH 阶段存在多个独立的知识缺口时，Builder 必须并行调度 @researcher 和 @reference-miner。DESIGN 阶段无依赖的组件可并行设计。
