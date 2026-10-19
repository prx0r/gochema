#!/usr/bin/env bash
# r2.sh — thin wrapper over aws cli for the gochema R2 bucket.
# Creds from /root/.r2-env at runtime. Nothing secret lives here.
set -euo pipefail
ENV_FILE="${R2_ENV:-/root/.r2-env}"
# shellcheck disable=SC1090
set -a; . "$ENV_FILE" >/dev/null 2>&1; set +a
export AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="$R2_SECRET_KEY"
BUCKET="${R2_BUCKET:?R2_BUCKET missing}"
case "${1:-}" in
  ls)   shift; aws --endpoint-url "$R2_ENDPOINT" s3 ls "s3://$BUCKET/$*" ;;
  fetch) shift; aws --endpoint-url "$R2_ENDPOINT" s3 cp "s3://$BUCKET/$1" "$2" ;;
  *) echo "usage: r2.sh ls <prefix> | fetch <key> <dest>"; exit 1 ;;
esac
