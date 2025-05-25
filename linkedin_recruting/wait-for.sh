#!/usr/bin/env bash
# wait-for.sh

set -e

TIMEOUT=30
QUIET=0

print_usage() {
  echo "Usage: wait-for.sh host:port [--timeout=seconds] [--quiet] -- command args"
}

wait_for() {
  local host="$1"
  local port="$2"
  local start_ts=$(date +%s)
  while :; do
    if nc -z "$host" "$port" >/dev/null 2>&1; then
      if [ "$QUIET" -ne 1 ]; then
        echo "✔ Connection to $host:$port succeeded"
      fi
      break
    fi
    sleep 1
    if [ $(( $(date +%s) - start_ts )) -ge "$TIMEOUT" ]; then
      echo "✖ Timeout while waiting for $host:$port" >&2
      exit 1
    fi
  done
}

# Parse arguments
HOST_PORT=""
CMD=()
while [ $# -gt 0 ]; do
  case "$1" in
    --timeout=*)
      TIMEOUT="${1#*=}"
      shift
      ;;
    --quiet)
      QUIET=1
      shift
      ;;
    --)
      shift
      CMD=("$@")
      break
      ;;
    *:*)
      HOST_PORT="$1"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      print_usage
      exit 1
      ;;
  esac
done

if [ -z "$HOST_PORT" ] || [ ${#CMD[@]} -eq 0 ]; then
  print_usage
  exit 1
fi

# Extract host and port
IFS=':' read -r HOST PORT <<< "$HOST_PORT"

# Wait for host:port
wait_for "$HOST" "$PORT"

# Execute command
exec "${CMD[@]}"
