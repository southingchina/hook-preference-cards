# 钩子心选 · Hook Preference Cards

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português (Brasil)](README.pt-BR.md)

一个只在本地运行的卡片偏好筛选网页。逐张选择喜欢、不喜欢、跳过或“不是有效开场”，支持撤销、保存恢复、特征统计及 JSON/CSV 导出。可改造成标题、创意或写作练习的偏好筛选器。

## 快速启动

Python 3.10+，仅标准库，无需安装前端依赖：

```shell
git clone https://github.com/southingchina/hook-preference-cards.git
cd hook-preference-cards
python server.py --port 8769
```

浏览器打开 http://127.0.0.1:8769 。选择保存在 `runtime/`，退出再启动可继续。端口可更改；`--state` 可指定独立的状态文件。服务仅绑定回环地址，不包含公网部署或多用户认证。

## 示例数据与替换

仓库只有 **20 条原创合成示例**，没有博主原句、个人偏好记录或真实平台数据。`data/hooks.json` 是卡片数组，主要字段为 `id`、`text`、`author`、`title`、`url`、`tags`、`review.status`；示例点赞数 0 不是实际数据。

替换数据时保持 ID 唯一，`review.status` 为 `approved` 才进入可选队列。新卡池请配合新的 `--state` 文件，避免旧选择与新数据不一致。统计反映当前个人选择，不代表内容传播效果或普遍受众偏好。

## 实现

- `model.py`：按 revision 检查并发更新、原子保存、备份恢复、队列和撤销。
- `server.py`：固定静态路由、本地 JSON API、CSV 导出及来源检查。
- `static/`：原生 HTML/CSS/JavaScript；没有在线分析或第三方资源请求。
- `prepare.py`：保留开场摘录的完整句辅助函数，不含原始抓取或私有数据路径。

## 验证

```shell
python -m unittest discover -s tests -v
```

测试覆盖状态/撤销/冲突、备份与迁移逻辑、真实回环 HTTP 保存/导出、来源检查及固定静态路由。公开版只包含通用卡片筛选核心；私有批次生成、真实素材审核、个性化推荐及其历史验收不在发布范围中。

MIT。欢迎使用自己的合法数据扩展；本仓库示例可随代码一起使用。
