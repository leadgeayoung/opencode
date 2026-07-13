# 多智能体集群规则 — session 启动时同步到 ./AGENTS.md
# 所有 agent 必须遵守这些规则，包括 Builder 本身和各个子代理

rules:
  - id: 0
    title: 单一事实源
    text: >
      以下文件是各自领域的唯一事实来源，禁止硬编码或重复：
      engine/state-machine.yaml（状态转换规则与计数器定义），
      engine/state-schema.json（WorkflowState 枚举与状态 JSON Schema）。
      子 agent 的校验逻辑必须引用上述文件。

  - id: 1
    title: 严格状态回滚
    text: >
      外环（Reviewer/Implementer）对代码的任何物理修改，
      必须无条件触发内环（Tester）的回归测试。
      未经过 Tester 确认的代码严禁交付。

  - id: 2
    title: 原子化熔断
    text: >
      任何子代理之间的局部循环（如 Test-Debug）最大重试次数为 3 次。
      达到上限必须向 Builder 提交 Failure Summary 并挂起。

  - id: 3
    title: 生态与参考先导
    text: >
      Planner 与 Architect 在承接任务后，第一动作必须是检索
      .opencode/knowledge/skills/、.opencode/knowledge/boilerplates/
      以及由 @reference-miner 动态抓取的 .opencode/knowledge/references/。
      严禁凭空盲写。

  - id: 4
    title: 无代码中转
    text: >
      Builder 严禁读取、存储、中转任何具体的代码片段，
      仅允许处理状态码与 Summary JSON。

  - id: 5
    title: 影子沙箱隔离
    text: >
      @reference-miner 的一切克隆与解压行为，必须在独立的本地沙箱
      .opencode/sandbox/ 中进行，禁止其直接接触生产源码区。

  - id: 6
    title: 状态持久化
    text: >
      Builder 必须在每次操作前后读写 current.json。
      状态文件丢失时必须重建。

  - id: 7
    title: 协议校验强制
    text: >
      所有子代理的返回结果必须通过 MCP validate_response 校验。
      缺少 status、summary、artifacts、issues 任一字段的响应
      必须被拒绝并重试。

  - id: 8
    title: 并行加速
    text: >
      当 RESEARCH 阶段存在多个独立的知识缺口时，Builder 必须并行调度
      @researcher 和 @reference-miner。在所有并发任务返回前不推进
      workflow_state。

  - id: 9
    title: Artifact 引用原则
    text: >
      所有子代理返回的 artifacts 必须遵循引用传递。禁止将代码内容、
      日志正文、文档全文内联到 artifacts 中。违反此规则的响应
      由 MCP validate_response 拒绝。
