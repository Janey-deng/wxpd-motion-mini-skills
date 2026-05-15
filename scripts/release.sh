#!/usr/bin/env bash
# ==============================================================================
# motion-mini-skills · 单人维护发版脚本
#
# 用法:
#   bash scripts/release.sh 0.5.1
#
# 行为 (步骤间会暂停让你确认):
#   1. 校验版本号格式 (X.Y.Z, 例: 0.5.1)
#   2. 校验 git 工作区干净, 当前在 main 分支
#   3. 改 VERSION 文件
#   4. 改 .cursor/rules/motion.mdc 头部 "当前版本: **vX.Y.Z**" 标注
#   4.5 同步 README.md 中所有 vOLD → vNEW (raw URL / badge / install 命令 / 文字版本号)
#   4.5 同步 install.sh 错误提示中的版本号示例
#   5. 提示你检查 CHANGELOG.md 是否已经写好新版本条目 (失败则 git checkout 回滚)
#   6. git add + commit + tag + push 到远端
#   7. 提示你去 GitHub 网页创建 Release (本机未装 gh CLI)
#
# 不依赖: gh CLI / jq / sed -i 的 GNU/BSD 差异
# ==============================================================================

set -euo pipefail

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

# 跨平台 sed -i (macOS BSD sed 需要 sed -i '' , GNU sed 用 sed -i)
sed_inplace() {
  if sed --version >/dev/null 2>&1; then
    sed -i "$@"
  else
    sed -i '' "$@"
  fi
}

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# ---------- 1. 校验版本号 ----------
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  log_error "用法: bash scripts/release.sh <版本号>"
  log_error "示例: bash scripts/release.sh 0.5.1"
  exit 1
fi
# 接受 v0.5.1 / 0.5.1 两种写法, 内部统一去掉 v 前缀做版本号比较, 加 v 前缀做 tag
VERSION="${VERSION#v}"
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  log_error "版本号格式错误: $VERSION (应为 X.Y.Z, 例: 0.5.1)"
  exit 1
fi
TAG="v$VERSION"

CURRENT_VERSION="$(cat VERSION 2>/dev/null | tr -d '[:space:]' || echo "未知")"
log_info "当前版本: ${CURRENT_VERSION}"
log_info "目标版本: ${VERSION}"

if [ "$VERSION" = "$CURRENT_VERSION" ]; then
  log_error "目标版本与当前版本相同, 无需发版"
  exit 1
fi

# ---------- 2. 校验 git 状态 ----------
if [ ! -d .git ]; then
  log_error "当前目录不是 git 仓库, 请先 git init / git remote add origin ..."
  exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
  log_warn "当前分支不是 main/master, 而是: $CURRENT_BRANCH"
  read -p "确认要在此分支发版吗? (y/N) " confirm
  [ "$confirm" = "y" ] || exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  log_error "git 工作区有未提交的改动, 请先 commit 或 stash:"
  git status --short
  exit 1
fi

# 确认远端可达
if ! git remote get-url origin >/dev/null 2>&1; then
  log_error "未配置 git remote origin, 请先 git remote add origin git@github.com:Janey-deng/wxpd-motion-mini-skills.git"
  exit 1
fi

# 确认 tag 不存在
if git rev-parse "$TAG" >/dev/null 2>&1; then
  log_error "tag $TAG 已存在 (本地), 请删除后重试: git tag -d $TAG"
  exit 1
fi
if git ls-remote --tags origin "$TAG" 2>/dev/null | grep -q "$TAG"; then
  log_error "tag $TAG 已存在 (远端), 不允许重发同一版本号"
  exit 1
fi

log_ok "git 状态检查通过 (分支: $CURRENT_BRANCH)"

# ---------- 3. 改 VERSION ----------
echo "$VERSION" > VERSION
log_ok "已更新 VERSION → $VERSION"

# ---------- 4. 改 motion.mdc 头部版本号 ----------
MDC=".cursor/rules/motion.mdc"
if [ -f "$MDC" ] && grep -q "当前版本: \*\*v" "$MDC"; then
  sed_inplace "s/当前版本: \*\*v[0-9.]*\*\*/当前版本: **v$VERSION**/g" "$MDC"
  log_ok "已更新 $MDC 头部版本号 → v$VERSION"
else
  log_warn "$MDC 中未找到 \"当前版本: **vX.Y.Z**\" 标注, 跳过自动同步"
fi

# ---------- 4.5 同步 README.md 与 install.sh 内的版本号引用 ----------
# 设计: 仅在"当前可识别为版本号引用"的位置替换, 不做盲目全文替换。
# README.md 不包含任何历史版本号叙述 (历史在 CHANGELOG.md),
# install.sh 仅替换 "例: vX.Y.Z" 形式的示例 (历史 bug 叙述里的 v0.5.0 不动)。

OLD_VER="$CURRENT_VERSION"

if [ -f README.md ] && [ -n "$OLD_VER" ] && [ "$OLD_VER" != "未知" ]; then
  # README.md 中所有 vOLD → vNEW (经验证 README 无历史版本号引用, 安全)
  sed_inplace "s|v${OLD_VER}|v${VERSION}|g" README.md
  log_ok "已更新 README.md 版本号引用 (v${OLD_VER} → v${VERSION})"
else
  log_warn "未找到 README.md 或当前版本号未知, 跳过 README 同步"
fi

if [ -f install.sh ] && [ -n "$OLD_VER" ] && [ "$OLD_VER" != "未知" ]; then
  # 只替换 "例: vOLD" 这类示例引用 (避免误伤 L111/L112 历史 bug 叙述)
  sed_inplace "s|例: v${OLD_VER}|例: v${VERSION}|g" install.sh
  log_ok "已更新 install.sh 错误提示中的版本号示例 (v${OLD_VER} → v${VERSION})"
fi

# ---------- 5. 提示检查 CHANGELOG ----------
echo ""
log_warn "⚠ 请确认 CHANGELOG.md 顶部已经写好 [${VERSION}] 条目!"
log_warn "  (本脚本不会自动写 changelog, 需要你手动整理本次变更内容)"
echo ""
if ! grep -q "## \[${VERSION}\]" CHANGELOG.md 2>/dev/null; then
  log_error "CHANGELOG.md 中未找到 [${VERSION}] 条目"
  log_error "请先在 CHANGELOG.md 顶部加一段, 然后重新运行本脚本"
  # 用 git checkout 一次性回滚所有可能被本脚本修改的文件 (干净彻底, 不会误伤)
  # 前提: 脚本开始时 git 工作区已校验为干净 (见上文 git status --porcelain 检查)
  git checkout -- VERSION "$MDC" README.md install.sh 2>/dev/null || true
  log_info "已回滚 VERSION / $MDC / README.md / install.sh 的改动"
  exit 1
fi
log_ok "CHANGELOG.md 中找到 [${VERSION}] 条目"

# ---------- 6. 显示待提交的 diff ----------
echo ""
log_info "本次提交将包含以下改动:"
git --no-pager diff --stat
echo ""
git --no-pager diff
echo ""
read -p "确认无误后回车继续 commit + tag + push (Ctrl+C 取消): "

# ---------- 7. commit + tag + push ----------
git add -A
git commit -m "release: v$VERSION

详见 CHANGELOG.md [${VERSION}] 条目。"

git tag -a "$TAG" -m "Release $TAG"
log_ok "已创建本地 tag $TAG"

log_info "推送到远端 (main + tag)..."
git push origin "$CURRENT_BRANCH"
git push origin "$TAG"
log_ok "已推送 commit 与 tag 到远端"

# ---------- 8. 提示创建 GitHub Release ----------
echo ""
printf "${C_BOLD}${C_GREEN}✓ v$VERSION 发版完成${C_RESET}\n\n"
printf "${C_BOLD}下一步 (手动)${C_RESET}: 在 GitHub 网页创建 Release\n"
printf "  ${C_CYAN}https://github.com/Janey-deng/wxpd-motion-mini-skills/releases/new?tag=$TAG${C_RESET}\n"
printf "  - Release title 建议填: ${C_DIM}v$VERSION${C_RESET}\n"
printf "  - Release notes 复制 CHANGELOG.md 中 [${VERSION}] 条目下的内容\n\n"
printf "${C_BOLD}同事使用新版本${C_RESET}:\n"
printf "  ${C_DIM}curl -sSL https://raw.githubusercontent.com/Janey-deng/wxpd-motion-mini-skills/$TAG/install.sh | bash -s $TAG${C_RESET}\n"
