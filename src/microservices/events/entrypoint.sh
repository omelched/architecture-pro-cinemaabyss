#!/bin/bash

POSITIONAL_ARGS=()
DEGUGGER="${PYDEBUGGER:-false}"
WEB_PORT="${PORT:-8000}"
DEBUGGER_PORT="${DEBUGGER_PORT:-5678}"

while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--debuger)
      # use debugger
      DEGUGGER=true
      shift
    ;;
    -wp|--web-port)
      # set port
      WEB_PORT=$2
      shift
      shift
    ;;
    -dp|--debugger-port)
      # set port for debugger
      DEBUGGER_PORT=$2
      shift
      shift
    ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
    ;;
    *)
      POSITIONAL_ARGS+=("$1")
      shift
    ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}"

case $1 in
  uv|uvicorn)
    # run uvicorn
    module="uvicorn event_handler:app --host 0.0.0.0 --port ${WEB_PORT} --reload"
  ;;
  m|module)
    # run arbitrary module
    module="$2"
  ;;
  *)
    echo "Unknown task $1"
    exit 1
  ;;
esac


if [ $DEGUGGER = true ]; then
  task="python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:${DEBUGGER_PORT} -m ${module}"
else
  task="python -m ${module}"
fi

echo $task
eval $task