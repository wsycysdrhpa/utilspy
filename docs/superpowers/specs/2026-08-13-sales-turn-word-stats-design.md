# Design: 销售每轮平均单词数统计（人工 vs 机器人）

日期：2026-08-13  
脚本：`test_local/business/analyse_llm3_human/scripts/statistics.py`

## 目标

统计所有对话中销售每轮说的平均单词个数，人工与机器人分开统计并对比。

## 输入 / 输出

| 项 | 人工 | 机器人 |
|----|------|--------|
| 输入文件 | `output/hum_dialog_sop_stage_sample1.xlsx` | `output/llm_dialog_sop_stage_sample1.xlsx` |
| 对话字段 | `conversation_log_filtered` | `dialog_detail` |
| 销售角色 | `assistant` | `bot` |
| 客户角色 | `user` | `user` |

输出：

- 终端打印对比汇总
- `output/sales_turn_word_stats.md` 简要报告

## 轮次与词数规则

1. **分词**：`str.split()`（按空白切分，适用于印尼语）
2. **一轮定义**：同一角色连续多句合并为 1 轮，该轮词数 = 各句词数之和
3. **人工开局门槛**（仅人工）：从对话开头起跳过销售轮，直到某销售轮词数 **> 5**，该轮及之后的销售轮才计入统计；之后即使销售轮较短也计入
4. **机器人**：忽略全部 `overtime` 条目；过滤后若相邻仍是 bot，同样合并为 1 轮；从第一条有效 bot 轮开始统计（无 >5 门槛）
5. 客户轮不参与分子/分母

## 指标（两侧各算一套）

对每通通话提取销售轮词数列表后：

| 指标 | 计算 |
|------|------|
| 有效通话数 | 至少有 1 个计入的销售轮 |
| 销售总轮次 | 所有计入销售轮数之和 |
| 销售总词数 | 所有计入销售轮词数之和 |
| **全局均值** | 销售总词数 ÷ 销售总轮次 |
| **通话均值的均值** | mean(每通：该通词数 ÷ 该通轮次)；无销售轮的通话不计入 |

## 实现要点

- 单脚本本地统计，不调用 LLM
- 复用项目内常见的 Excel 读取与 JSON 解析模式（与 `acquire_sop_stage.py` 等一致）
- 人工解析 `messages[]` 的 `role` / `content`
- 机器人解析 `items[]`：`create.bot.message`、`chat.user/bot.message`；跳过 `overtime`；忽略 `destroy` 等无 message 结构
- 解析失败的行跳过并计数，不中断整批

## 非目标

- 不做 SOP / 阶段交叉分析
- 不输出每通明细 Excel
- 不使用中文翻译列（`*_zh`）
