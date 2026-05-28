#!/bin/bash
# 安装 Git hooks
# 运行: bash install-hooks.sh

echo "安装 Git pre-push 钩子..."
cp .githooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
echo "✅ 已安装 pre-push 钩子"
echo ""
echo "安全提示："
echo "  git push               # 正常推送"
echo "  git push --no-verify   # 跳过钩子（仅在完全确定时使用）"
