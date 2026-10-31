#!/bin/sh
# Install this local bundle without downloading or overwriting an existing skill.
set -eu
bundle_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skill_name=codebase-to-course-plus
skills_root="${HOME}/.agents/skills"
if [ "${1:-}" = "--dest" ] && [ "$#" -eq 2 ]; then
  skills_root=$2
elif [ "$#" -ne 0 ]; then
  printf '%s\n' "Usage: sh $0 [--dest /path/to/skills]" >&2
  exit 2
fi
source_dir="$bundle_dir/$skill_name"
target_dir="$skills_root/$skill_name"
if [ ! -f "$source_dir/SKILL.md" ]; then
  printf '%s\n' "找不到完整的 skill 文件夹：$source_dir" >&2
  exit 1
fi
if [ -e "$target_dir" ] || [ -L "$target_dir" ]; then
  printf '%s\n' "目标已存在，未覆盖：$target_dir" "请先检查已有版本，再自行备份或选择其他安装位置。" >&2
  exit 1
fi
mkdir -p -- "$skills_root"
cp -R -- "$source_dir" "$target_dir"
printf '%s\n' "已安装：$target_dir" '下一轮对话可尝试 $codebase-to-course-plus；未出现时重启 Codex。'
