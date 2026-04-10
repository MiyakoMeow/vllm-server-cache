# 知行车秘

## 项目配置

- 完全使用`uv`进行依赖管理、实际项目运行等。

- 每次修改后，直接运行，不要加额外参数：
  1. `uv run ruff check --fix`
  2. `uv run ruff format`
  3. `uv run ty check`

- 代码规范：
  - **代码注释必须使用中文**（包括 docstring、行内注释）
  - **提交信息必须使用英文；必须遵循 Convention Commits 规范**：[参考](https://www.conventionalcommits.org/)
## Skill流程特定配置

### brainstorming

- 编写 `设计文档（spec）` 和 `计划文档（plan）` 完成后，运行完整的 review loop 流程。
- 优先选择 `SubAgent-Driven Development` 。每一步完成后，同样运行 review loop 流程。
