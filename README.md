# skill-for-promoting-my-understanding-of-codebase

**Codebase to Course Plus**：把项目源码变成可追溯、可交互、可以跟着敲的课程。

基于 [Zara Zhang 的 codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) 增强，适合普通软件项目和科研 / 机器学习代码，特别适合结合论文理解实现。skill 名称为 **`codebase-to-course-plus`**。

## 能做什么

- 用中文解释真实源码，记录代码版本、配置、入口、文件与行号。
- 将论文概念对应到实现，追踪张量形状、轴含义、坐标系、损失和梯度路径。
- 提供分步跟敲任务、起始代码、提示、参考答案与检查方法。
- 生成带有代码解释、测验、数据流动画、术语提示的交互课程。
- 使用本地 HTML / CSS / JS 和系统字体，生成结果可以离线打开。
- 检查引用的源码是否变化，以及章节导航、本地资源和基本交互配置。

## 在 Codex 中安装

克隆仓库，在仓库根目录运行安装脚本：

```bash
git clone https://github.com/cheung-0209/skill-for-promoting-my-understanding-of-codebase.git
cd skill-for-promoting-my-understanding-of-codebase
sh ./install-codebase-to-course-plus.sh
```

脚本默认安装完整 skill 到 `~/.agents/skills/codebase-to-course-plus`；已有同名目录时会停止。Codex 通常自动发现变化，未出现时重启。当前个人与项目 skills 路径见 [OpenAI 官方文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

若当前 Codex 版本使用其他 skills 目录，可显式指定：

```bash
sh ./install-codebase-to-course-plus.sh --dest /path/to/skills
```

安装脚本适用于 macOS / Linux。其他平台可以手动复制整个 `codebase-to-course-plus` 文件夹到实际使用的 skills 目录。运行课程辅助工具需要 Python 3.9+，只使用标准库。

## 开始学习

在 Codex 中输入：

```text
使用 $codebase-to-course-plus，把 https://github.com/barry664/DeformCL
制作成中文交互式源码跟敲课程。
结合论文解释数据预处理、forward、中心线变形、张量形状与坐标系、
损失函数和训练 / 推理的区别。
每章提供真实源码行号、分步跟敲任务、提示、参考答案和检查方法。
优先设计 CPU 可完成的小练习，输出可离线打开的完整课程目录。
```

也可以指定本地项目：

```text
使用 $codebase-to-course-plus，把当前项目制作成中文交互课程。
我会 Python，想通过跟敲理解主要数据流，先讲主路径，再讲扩展模块。
```

## 仓库结构

```text
codebase-to-course-plus/
  SKILL.md                 课程生成流程与触发范围
  agents/openai.yaml       Codex 显示信息
  references/              源码阅读、科研讲解、跟敲和质量规范
  scripts/course.py        初始化、源码提取、构建与静态检查
  assets/course/           本地课程模板与交互引擎
  SOURCE.md                上游来源、固定提交与改动说明
install-codebase-to-course-plus.sh
tests/test_course.py
安装与使用.md
验证记录.md
```

## 验证

运行辅助工具的回归检查：

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖源码提取与篡改检测、非法行号、路径越界、重复章节、资源缺失、远程资源和数据流配置。测试在临时目录创建样例，结束后清理。模板另外经过离线浏览器排版与交互检查，详细范围见 [验证记录](验证记录.md)。

课程中的教学示例会与原作者代码分开标注；模型训练、真实数据推理和论文指标复现会按实际执行情况说明。

## 来源

保留原版的交互课程设计，并增加源码证据、科研讲解、跟敲练习和离线工具。上游固定提交及许可状态见 [SOURCE.md](codebase-to-course-plus/SOURCE.md)。

详细安装和使用方法见 [安装与使用.md](安装与使用.md)。
