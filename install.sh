#!/usr/bin/env bash
# ==============================================================================
# motion-mini-skills · 一键安装脚本
#
# 用法:
#   curl -sSL https://raw.githubusercontent.com/Janey-deng/wxpd-motion-mini-skills/vX.Y.Z/install.sh | bash -s vX.Y.Z
#   或在已克隆的目录里直接: bash install.sh vX.Y.Z
#
#   (vX.Y.Z 替换为实际版本号, 例: v0.5.1; 不指定参数则自动取 GitHub 上最新 release tag)
#
# 行为:
#   1. 下载指定 tag 的 tarball 到临时目录
#   2. 把 motion.mdc + motion-catalog.md + 7 个 skill md 复制到当前项目的 docs/motion-skills/
#   3. 智能检测当前项目里的 IDE 标志, 在对应位置写"入口指针"文件:
#      - .cursor/         → .cursor/rules/motion.mdc
#      - CLAUDE.md / .claude/ → 在 CLAUDE.md 追加引用块 (幂等)
#      - .codebuddy/      → .codebuddy/rules/motion/RULE.mdc
#   4. 三个 IDE 共存时, 同时写入所有检测到的位置
#
# 不依赖 git / jq / gh, 仅需 curl + tar + bash 4+ (macOS / Linux 默认即有)
# ==============================================================================

set -euo pipefail

REPO="Janey-deng/wxpd-motion-mini-skills"
VERSION="${1:-}"

# ---------- 颜色输出 ----------
if [ -t 1 ]; then
  C_RESET='\033[0m'
  C_BOLD='\033[1m'
  C_GREEN='\033[32m'
  C_YELLOW='\033[33m'
  C_RED='\033[31m'
  C_CYAN='\033[36m'
  C_DIM='\033[2m'
else
  C_RESET='' C_BOLD='' C_GREEN='' C_YELLOW='' C_RED='' C_CYAN='' C_DIM=''
fi

log_info()  { printf "${C_CYAN}ℹ %s${C_RESET}\n" "$*"; }
log_ok()    { printf "${C_GREEN}✓ %s${C_RESET}\n" "$*"; }
log_warn()  { printf "${C_YELLOW}⚠ %s${C_RESET}\n" "$*"; }
log_error() { printf "${C_RED}✗ %s${C_RESET}\n" "$*" >&2; }

# ---------- 1. 解析版本号 ----------
if [ -z "$VERSION" ]; then
  log_info "未指定版本, 自动获取 GitHub 上最新 release tag..."
  VERSION=$(curl -sSL "https://api.github.com/repos/${REPO}/releases/latest" \
    | grep '"tag_name"' \
    | head -n 1 \
    | sed -E 's/.*"tag_name": *"([^"]+)".*/\1/')
  if [ -z "$VERSION" ]; then
    log_error "无法获取最新版本号, 请显式指定版本: bash install.sh vX.Y.Z"
    exit 1
  fi
fi

# 接受 vX.Y.Z / X.Y.Z 两种写法, 内部统一加 v 前缀
case "$VERSION" in
  v*) ;;
  *)  VERSION="v$VERSION" ;;
esac

if ! [[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  log_error "版本号格式错误: $VERSION (应为 vX.Y.Z, 例: v0.5.1)"
  exit 1
fi

printf "${C_BOLD}motion-mini-skills 安装器${C_RESET}\n"
printf "${C_DIM}仓库: ${REPO}${C_RESET}\n"
printf "${C_DIM}版本: ${VERSION}${C_RESET}\n"
printf "${C_DIM}目标项目: $(pwd)${C_RESET}\n\n"

# ---------- 2. 下载 tarball ----------
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

TARBALL_URL="https://github.com/${REPO}/archive/refs/tags/${VERSION}.tar.gz"
log_info "下载 ${VERSION} 源码..."
if ! curl -fsSL "$TARBALL_URL" -o "$TMP_DIR/src.tar.gz"; then
  log_error "下载失败: $TARBALL_URL"
  log_error "请检查版本号是否存在, 或网络是否能访问 github.com"
  exit 1
fi
tar -xzf "$TMP_DIR/src.tar.gz" -C "$TMP_DIR"

# tar 解压后目录名为 <repo>-<version-without-v>
SRC_DIR="$TMP_DIR/$(basename "$REPO")-${VERSION#v}"
if [ ! -d "$SRC_DIR" ]; then
  log_error "解压后未找到源码目录: $SRC_DIR"
  exit 1
fi

# 校验源码完整性 (确保关键文件都在)
for required in ".cursor/rules/motion.mdc" "docs/motion-catalog.md" "docs/skills"; do
  if [ ! -e "$SRC_DIR/$required" ]; then
    log_error "源码不完整, 缺少: $required"
    exit 1
  fi
done
log_ok "源码下载与校验完成"

# ---------- 3. 复制主体内容到 docs/motion-skills/ ----------
TARGET_DOCS="docs/motion-skills"
log_info "安装主体内容到 ${TARGET_DOCS}/ ..."
mkdir -p "$TARGET_DOCS/skills"
cp "$SRC_DIR/.cursor/rules/motion.mdc"  "$TARGET_DOCS/motion.mdc"
cp "$SRC_DIR/docs/motion-catalog.md"    "$TARGET_DOCS/motion-catalog.md"

# 清理旧残留: v0.5.0 install.sh 误把 _template.md 等开发期文件复制到了同事项目里,
# 升级到 v0.5.1+ 时主动删掉, 避免 AI 误读 _template.md 当作 skill 调用
rm -f "$TARGET_DOCS/skills/_"*.md 2>/dev/null || true

# 仅复制实际 skill 文件, 排除以 _ 开头的开发期内部文件 (例: _template.md)
find "$SRC_DIR/docs/skills" -maxdepth 1 -name "*.md" -not -name "_*" -exec cp {} "$TARGET_DOCS/skills/" \;

SKILL_COUNT=$(find "$TARGET_DOCS/skills" -maxdepth 1 -name "*.md" -not -name "_*" | wc -l | tr -d ' ')
log_ok "已安装 1 份协议 + 1 份目录 + ${SKILL_COUNT} 个 skill"

# ---------- 4. 智能检测 IDE 并写入口指针 ----------
DETECTED=()

# 入口指针的统一正文 (告诉 AI 去读 docs/motion-skills/motion.mdc)
make_entry_body() {
  cat <<EOF
本项目使用 motion-mini-skills (${VERSION}) 提供的动效协议生成微信小程序动效代码。

**使用方式**:

1. 用户提到"动效 / 动画 / 入场 / 弹窗 / 浮入 / 上滑 / 下落 / 渐显"等关键词时, 必须先阅读以下文件:
   - 协议: \`docs/motion-skills/motion.mdc\` (强制规则)
   - 目录: \`docs/motion-skills/motion-catalog.md\` (查可用 skill 列表)
   - Skill 实现: \`docs/motion-skills/skills/<skill-id>.md\` (具体代码)

2. 严格按协议中的 \`[MUST]\` / \`[MUST NOT]\` 约束生成代码 (例: 时长 ≤ 600ms, 仅用 transform/opacity, 必须输出自查报告)。

3. 不要凭记忆编造动效代码, 必须使用 \`docs/motion-skills/skills/\` 中已定义的 skill。
EOF
}

# --- Cursor (.cursor/rules/motion.mdc) ---
if [ -d ".cursor" ]; then
  mkdir -p .cursor/rules
  {
    echo "---"
    echo "description: motion-mini-skills 动效协议入口指针 (${VERSION}) - 引导 AI 读取 docs/motion-skills/motion.mdc"
    echo "alwaysApply: true"
    echo "---"
    echo ""
    echo "# motion-mini-skills 入口"
    echo ""
    make_entry_body
  } > .cursor/rules/motion.mdc
  DETECTED+=("Cursor (.cursor/rules/motion.mdc)")
fi

# --- Claude Code (CLAUDE.md, 幂等追加) ---
CLAUDE_MARKER="<!-- motion-mini-skills:begin -->"
CLAUDE_END="<!-- motion-mini-skills:end -->"

if [ -f "CLAUDE.md" ] || [ -d ".claude" ]; then
  # CLAUDE.md 不存在则创建空文件
  [ -f "CLAUDE.md" ] || touch CLAUDE.md

  # 幂等: 如果已经追加过, 先把旧块删掉再追加新版
  if grep -q "$CLAUDE_MARKER" CLAUDE.md 2>/dev/null; then
    # 用 awk 删除标记之间的旧块 (跨平台, 不依赖 sed -i 的 macOS/GNU 差异)
    awk -v start="$CLAUDE_MARKER" -v end="$CLAUDE_END" '
      $0 == start { skip=1; next }
      $0 == end   { skip=0; next }
      !skip       { print }
    ' CLAUDE.md > CLAUDE.md.tmp && mv CLAUDE.md.tmp CLAUDE.md
  fi

  {
    # 确保跟前面内容隔一空行
    [ -s CLAUDE.md ] && echo ""
    echo "$CLAUDE_MARKER"
    echo "## motion-mini-skills 动效协议 (${VERSION})"
    echo ""
    make_entry_body
    echo "$CLAUDE_END"
  } >> CLAUDE.md
  DETECTED+=("Claude Code (CLAUDE.md)")
fi

# --- CodeBuddy (.codebuddy/rules/motion/RULE.mdc) ---
if [ -d ".codebuddy" ]; then
  mkdir -p .codebuddy/rules/motion
  {
    echo "---"
    echo "description: motion-mini-skills 动效协议入口指针 (${VERSION}) - 引导 AI 读取 docs/motion-skills/motion.mdc"
    echo "alwaysApply: true"
    echo "enabled: true"
    echo "updatedAt: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "---"
    echo ""
    echo "# motion-mini-skills 入口"
    echo ""
    make_entry_body
  } > .codebuddy/rules/motion/RULE.mdc
  DETECTED+=("CodeBuddy (.codebuddy/rules/motion/RULE.mdc)")
fi

# ---------- 5. 输出安装结果 ----------
echo ""
printf "${C_BOLD}${C_GREEN}✓ motion-mini-skills ${VERSION} 安装完成${C_RESET}\n\n"
printf "${C_BOLD}主体内容${C_RESET}: ${TARGET_DOCS}/ (协议 + 目录 + ${SKILL_COUNT} 个 skill)\n"

if [ ${#DETECTED[@]} -eq 0 ]; then
  echo ""
  log_warn "未检测到任何支持的 IDE 标志 (.cursor/ / CLAUDE.md / .codebuddy/)"
  log_warn "主体内容已就绪, 但 AI 不会自动读取"
  echo ""
  printf "${C_BOLD}你可以选择${C_RESET}:\n"
  printf "  ${C_DIM}①${C_RESET} 在 AI 对话中手动 @ ${TARGET_DOCS}/motion.mdc 引用协议\n"
  printf "  ${C_DIM}②${C_RESET} 直接复制 ${TARGET_DOCS}/skills/ 中对应 skill md 的内容粘贴到 AI prompt\n"
  printf "  ${C_DIM}③${C_RESET} 切换到支持项目级 rules 的 IDE (Cursor / Claude Code / CodeBuddy) 后重新执行安装\n"
else
  echo ""
  printf "${C_BOLD}已写入入口指针${C_RESET}:\n"
  for entry in "${DETECTED[@]}"; do
    printf "  ${C_GREEN}✓${C_RESET} ${entry}\n"
  done
  echo ""
  printf "${C_BOLD}下一步${C_RESET}: 在 AI 对话中直接说人话即可, 例如:\n"
  printf "  ${C_DIM}\"给 pages/order 页的底部确认弹窗加一个优雅入场动效\"${C_RESET}\n"
fi

echo ""
printf "${C_DIM}变更日志: https://github.com/${REPO}/blob/${VERSION}/CHANGELOG.md${C_RESET}\n"
printf "${C_DIM}回滚到旧版: 重新执行 \`bash install.sh v<旧版本号>\` 即可${C_RESET}\n"
