#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
PACKAGE_NAME="portal-da-obra-vscode"
STAMP="$(date +%Y%m%d-%H%M%S)"
STAGING_DIR="$DIST_DIR/${PACKAGE_NAME}-${STAMP}"
ZIP_PATH="$DIST_DIR/${PACKAGE_NAME}-${STAMP}.zip"

mkdir -p "$DIST_DIR"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

# Copia apenas o necessário para execução local no VS Code.
cp -R "$ROOT_DIR/frontend" "$STAGING_DIR/frontend"
cp -R "$ROOT_DIR/backend" "$STAGING_DIR/backend"
cp -R "$ROOT_DIR/scripts" "$STAGING_DIR/scripts"
cp "$ROOT_DIR/README.md" "$STAGING_DIR/README.md"
cp "$ROOT_DIR/docker-compose.yml" "$STAGING_DIR/docker-compose.yml"
cp "$ROOT_DIR/.env.example" "$STAGING_DIR/.env.example"
cp "$ROOT_DIR/.gitignore" "$STAGING_DIR/.gitignore"

# Remove artefatos pesados/locais que não devem ir no pacote.
rm -rf "$STAGING_DIR/backend/.venv" \
       "$STAGING_DIR/frontend/node_modules" \
       "$STAGING_DIR/backend/__pycache__" \
       "$STAGING_DIR/frontend/.next" \
       "$STAGING_DIR/.runtime"
find "$STAGING_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$STAGING_DIR" -type f -name '*.pyc' -delete
find "$STAGING_DIR" -type f -name '*.pyo' -delete

(
  cd "$DIST_DIR"
  zip -r "$(basename "$ZIP_PATH")" "$(basename "$STAGING_DIR")" >/dev/null
)

echo "$ZIP_PATH"
