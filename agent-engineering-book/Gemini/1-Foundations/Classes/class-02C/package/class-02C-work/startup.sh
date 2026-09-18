#!/usr/bin/env bash
#
# Class 02C startup.
#
#   source ./class-02C-work/startup.sh                       # use .env as it stands
#   source ./class-02C-work/startup.sh PROJECT_ID            # switch project
#   source ./class-02C-work/startup.sh PROJECT_ID REGION     # switch project and region
#   ./class-02C-work/startup.sh PROJECT_ID --check           # report only, change nothing
#
# REGION defaults to us-central1. PROJECT_ID defaults to whatever .env already
# names.
#
# Use `source`. A script cannot activate a virtual environment in the shell that
# launched it, so running this as ./startup.sh does everything except leave you
# inside .venv, and says so at the end.
#
# What it does, in order: create or repair .venv, write PROJECT_ID and REGION
# into .env, point gcloud at that project, refresh Application Default
# Credentials if they do not match, confirm the required APIs, stop a stale
# server from an earlier project, and activate the venv.
#
# The step that matters most is ADC. `gcloud auth login` credentials the gcloud
# command; `gcloud auth application-default login` writes the credentials the
# agent and the Cloud Trace exporter actually use. Changing projects without the
# second one leaves the lab silently pointed at the old project.

# Sourced or executed? Determines `return` vs `exit`, and whether activating
# the venv can outlive this script.
_c02c_sourced=0
if [ -n "${ZSH_EVAL_CONTEXT:-}" ]; then
  case "$ZSH_EVAL_CONTEXT" in *:file*) _c02c_sourced=1 ;; esac
elif [ -n "${BASH_SOURCE:-}" ]; then
  [ "${BASH_SOURCE[0]}" != "$0" ] && _c02c_sourced=1
fi

# `set -e` in a sourced script would kill the caller's interactive shell on the
# first non-zero status, so it is only safe on the executed path.
if [ "$_c02c_sourced" -eq 0 ]; then
  set -uo pipefail
fi

_c02c_main() {
  local project_arg="" region_arg="" check=0
  local failed=0 warned=0

  # ------------------------------------------------------------- arguments

  local arg
  for arg in "$@"; do
    case "$arg" in
      --check|-n)  check=1 ;;
      --fix)       check=0 ;;   # accepted: fixing is now the default
      -h|--help)
        sed -n '3,20p' "$_c02c_self" | sed 's/^# \{0,1\}//'
        return 0
        ;;
      -*)
        echo "Unknown option: $arg"
        echo "Usage: startup.sh [PROJECT_ID] [REGION] [--check]"
        return 2
        ;;
      *)
        if [ -z "$project_arg" ]; then project_arg="$arg"
        elif [ -z "$region_arg" ]; then region_arg="$arg"
        else
          echo "Too many arguments: $arg"
          echo "Usage: startup.sh [PROJECT_ID] [REGION] [--check]"
          return 2
        fi
        ;;
    esac
  done

  pass() { printf '  PASS  %s\n' "$1"; }
  warn() { printf '  WARN  %s\n' "$1"; warned=$((warned + 1)); }
  fail() { printf '  FAIL  %s\n' "$1"; failed=$((failed + 1)); }
  did()  { printf '  DONE  %s\n' "$1"; }
  step() { printf '\n%s\n' "$1"; }

  # ---------------------------------------------------------- 1. locate pkg

  step "1. Package"

  local root=""
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/pyproject.toml" ] && [ -d "$dir/adk_multiagent_systems" ]; then
      root="$dir"
      break
    fi
    dir="$(dirname "$dir")"
  done

  if [ -z "$root" ] && [ -n "$_c02c_self" ]; then
    dir="$(cd "$(dirname "$_c02c_self")/.." 2>/dev/null && pwd)"
    if [ -n "$dir" ] && [ -f "$dir/pyproject.toml" ]; then
      root="$dir"
    fi
  fi

  if [ -z "$root" ]; then
    fail "not inside the class-02C package"
    echo "        cd into class-02C (the directory holding pyproject.toml) and retry."
    return 1
  fi
  pass "package root: $root"
  C02C_ROOT="$root"

  # ------------------------------------------------------------- 2. venv

  step "2. Virtual environment"

  if [ -f "$root/.venv/bin/activate" ]; then
    pass ".venv present"
  elif [ "$check" -eq 1 ]; then
    fail ".venv missing (would be created)"
  else
    echo "  ....  creating .venv"
    if python3 -m venv "$root/.venv" \
       && "$root/.venv/bin/python" -m pip install --upgrade pip --quiet \
       && "$root/.venv/bin/python" -m pip install -e "$root" --quiet; then
      did ".venv created and project installed"
    else
      fail "could not create .venv"
      echo "        python3 -m venv .venv && source .venv/bin/activate && python -m pip install -e ."
    fi
  fi

  # -------------------------------------------------------------- 3. .env

  step "3. .env"

  if [ ! -f "$root/.env" ]; then
    if [ "$check" -eq 1 ]; then
      fail ".env missing (would be created from .env.vertex.example)"
    elif [ -f "$root/.env.vertex.example" ]; then
      cp "$root/.env.vertex.example" "$root/.env"
      did ".env created from .env.vertex.example"
    else
      fail "no .env and no .env.vertex.example to copy"
      return 1
    fi
  fi

  # Read the current values without exporting the whole file yet.
  local env_project env_region
  env_project="$(sed -n 's/^GOOGLE_CLOUD_PROJECT=//p' "$root/.env" | tail -1)"
  env_region="$(sed -n 's/^GOOGLE_CLOUD_LOCATION=//p' "$root/.env" | tail -1)"

  local project region
  project="${project_arg:-$env_project}"
  region="${region_arg:-${env_region:-us-central1}}"
  [ "$region" = "global" ] && region="us-central1"
  [ -z "$region" ] && region="us-central1"

  if [ -z "$project" ] || [ "$project" = "replace_with_your_google_cloud_project_id" ]; then
    fail "no project id"
    echo "        Pass one:  source ./class-02C-work/startup.sh YOUR_PROJECT_ID"
    return 1
  fi

  # Rewrite the two keys in place, preserving every other line and comment.
  if [ "$project" != "$env_project" ] || [ "$region" != "$env_region" ]; then
    if [ "$check" -eq 1 ]; then
      fail ".env says project='$env_project' region='$env_region', want '$project'/'$region'"
    else
      local tmp
      tmp="$(mktemp)"
      sed -e "s|^GOOGLE_CLOUD_PROJECT=.*|GOOGLE_CLOUD_PROJECT=$project|" \
          -e "s|^GOOGLE_CLOUD_LOCATION=.*|GOOGLE_CLOUD_LOCATION=$region|" \
          "$root/.env" > "$tmp"
      grep -q '^GOOGLE_CLOUD_PROJECT=' "$tmp" || printf 'GOOGLE_CLOUD_PROJECT=%s\n' "$project" >> "$tmp"
      grep -q '^GOOGLE_CLOUD_LOCATION=' "$tmp" || printf 'GOOGLE_CLOUD_LOCATION=%s\n' "$region" >> "$tmp"
      cat "$tmp" > "$root/.env"
      rm -f "$tmp"
      did ".env updated: project=$project region=$region"
    fi
  else
    pass "project=$project region=$region"
  fi

  set -a
  # shellcheck disable=SC1090,SC1091
  . "$root/.env"
  set +a
  export GOOGLE_CLOUD_PROJECT="$project"
  export GOOGLE_CLOUD_LOCATION="$region"
  export PROJECT_ID="$project"

  local mode=apikey
  if [ "${GOOGLE_GENAI_USE_VERTEXAI:-}" = "TRUE" ]; then
    mode=vertex
    pass "GOOGLE_GENAI_USE_VERTEXAI=TRUE (Agent Platform)"
  elif [ -n "${GOOGLE_API_KEY:-}" ]; then
    pass "GOOGLE_API_KEY set (AI Studio key)"
  else
    fail "neither GOOGLE_GENAI_USE_VERTEXAI=TRUE nor GOOGLE_API_KEY is set in .env"
  fi

  # ------------------------------------------------------------ 4. gcloud

  step "4. gcloud"

  if ! command -v gcloud >/dev/null 2>&1; then
    fail "gcloud is not installed or not on PATH"
    return 1
  fi

  local account config_project
  account="$(gcloud config get-value account 2>/dev/null)"
  config_project="$(gcloud config get-value project 2>/dev/null)"

  if [ -n "$account" ] && [ "$account" != "(unset)" ]; then
    pass "account: $account"
  else
    fail "no active gcloud account"
    echo "        gcloud auth login"
  fi

  if [ "$config_project" = "$project" ]; then
    pass "gcloud project matches .env"
  elif [ "$check" -eq 1 ]; then
    fail "gcloud project is '$config_project', want '$project'"
  elif gcloud config set project "$project" >/dev/null 2>&1; then
    did "gcloud project set to $project"
  else
    fail "could not set gcloud project to $project"
  fi

  # A new lab instance issues a new project AND a new student account. The old
  # account often still works, so this is a warning, not a failure.
  case "$account" in
    student-*@qwiklabs.net)
      local acct_n proj_n
      acct_n="$(printf '%s' "$account" | sed -n 's/^student-\([0-9][0-9]*\)-.*/\1/p')"
      proj_n="$(printf '%s' "$project" | sed -n 's/^qwiklabs-gcp-\([0-9][0-9]*\)-.*/\1/p')"
      if [ -n "$acct_n" ] && [ -n "$proj_n" ] && [ "$acct_n" != "$proj_n" ]; then
        warn "account is student-$acct_n but project is qwiklabs-gcp-$proj_n"
        echo "        Harmless if this account still has access — step 6 proves it."
        echo "        If step 6 cannot list services:  gcloud auth list"
        echo "                                         gcloud config set account <this lab's account>"
      fi
      ;;
  esac

  # --------------------------------------------------------------- 5. ADC

  step "5. Application Default Credentials"

  local adc_path adc_quota adc_ok=1
  adc_path="${GOOGLE_APPLICATION_CREDENTIALS:-${CLOUDSDK_CONFIG:-$HOME/.config/gcloud}/application_default_credentials.json}"

  if [ -f "$adc_path" ]; then
    adc_quota="$(python3 -c "
import json, sys
try:
    print(json.load(open(sys.argv[1])).get('quota_project_id') or '')
except Exception:
    print('')
" "$adc_path" 2>/dev/null)"
    [ "$adc_quota" = "$project" ] || adc_ok=0
    gcloud auth application-default print-access-token >/dev/null 2>&1 || adc_ok=0
  else
    adc_quota=""
    adc_ok=0
  fi

  if [ "$adc_ok" -eq 1 ]; then
    pass "ADC valid for $project"
  elif [ "$check" -eq 1 ]; then
    fail "ADC is stale (quota project '${adc_quota:-unset}', want '$project')"
    echo "        gcloud auth application-default login"
    echo "        gcloud auth application-default set-quota-project $project"
  else
    echo "  ....  ADC quota project is '${adc_quota:-unset}', not '$project'"
    echo "  ....  a browser window will open for sign-in"
    if gcloud auth application-default login \
       && gcloud auth application-default set-quota-project "$project" >/dev/null 2>&1; then
      did "ADC refreshed for $project"
    else
      fail "ADC refresh did not complete"
      echo "        gcloud auth application-default login"
      echo "        gcloud auth application-default set-quota-project $project"
    fi
  fi

  # ---------------------------------------------------------- 6. services

  step "6. Google Cloud APIs"

  local -a required
  required=(cloudtrace.googleapis.com logging.googleapis.com monitoring.googleapis.com)
  [ "$mode" = vertex ] && required+=(aiplatform.googleapis.com)

  local enabled svc
  enabled="$(gcloud services list --enabled --project="$project" --format='value(config.name)' 2>/dev/null)"

  if [ -z "$enabled" ]; then
    warn "could not list enabled services on $project"
    echo "        Either this account lacks serviceusage.services.list, or it has no"
    echo "        access to this project. See the account note above."
  else
    for svc in "${required[@]}"; do
      if printf '%s\n' "$enabled" | grep -qx "$svc"; then
        pass "$svc"
      else
        fail "$svc is not enabled"
        echo "        gcloud services enable $svc --project=$project"
        echo "        A classroom project may answer UREQ_TOS_NOT_ACCEPTED. If so,"
        echo "        the lab administrator has to enable it."
      fi
    done
  fi

  # ----------------------------------------------------- 7. stale servers

  step "7. Running servers"

  # Only servers serving THIS package: another class's server is not ours to stop.
  local stale pid
  stale="$(pgrep -f "adk (web|api_server).*$root" 2>/dev/null)"

  if [ -z "$stale" ]; then
    pass "no stale ADK server"
  elif [ "$check" -eq 1 ]; then
    warn "ADK server running (PID: $(printf '%s' "$stale" | tr '\n' ' ')) — reads .env once, at startup"
  else
    while IFS= read -r pid; do
      [ -n "$pid" ] || continue
      if kill "$pid" 2>/dev/null; then
        did "stopped stale server (PID $pid) — it held the previous .env"
      else
        warn "could not stop PID $pid; stop it before starting a new server"
      fi
    done <<EOF
$stale
EOF
  fi

  C02C_FAILED="$failed"
  C02C_WARNED="$warned"
  C02C_PROJECT="$project"
  C02C_REGION="$region"
  C02C_ACCOUNT="$account"

  [ "$failed" -gt 0 ] && return 1
  return 0
}

# Resolve this file's path for --help and for the package-root fallback.
if [ -n "${BASH_SOURCE:-}" ]; then
  _c02c_self="${BASH_SOURCE[0]}"
elif [ -n "${ZSH_VERSION:-}" ]; then
  _c02c_self="${(%):-%x}"
else
  _c02c_self="$0"
fi

C02C_ROOT=""; C02C_FAILED=0; C02C_WARNED=0
C02C_PROJECT=""; C02C_REGION=""; C02C_ACCOUNT=""

_c02c_main "$@"
_c02c_rc=$?

# ----------------------------------------------------------- 8. venv + exit

if [ "$_c02c_rc" -eq 0 ] && [ -n "$C02C_ROOT" ]; then
  printf '\n8. Shell\n'
  if [ "$_c02c_sourced" -eq 1 ]; then
    if [ -n "${VIRTUAL_ENV:-}" ] && [ "$VIRTUAL_ENV" != "$C02C_ROOT/.venv" ]; then
      deactivate 2>/dev/null && printf '  DONE  deactivated %s\n' "$VIRTUAL_ENV"
    fi
    if [ -n "${VIRTUAL_ENV:-}" ] && [ "$VIRTUAL_ENV" = "$C02C_ROOT/.venv" ]; then
      printf '  PASS  .venv already active\n'
    elif [ -f "$C02C_ROOT/.venv/bin/activate" ]; then
      # shellcheck disable=SC1090,SC1091
      . "$C02C_ROOT/.venv/bin/activate" && printf '  DONE  activated %s/.venv\n' "$C02C_ROOT"
    fi
  else
    printf '  WARN  not sourced, so .venv is not active in your shell\n'
    printf '        Either:  source %s\n' "$_c02c_self"
    printf '        or:      source %s/.venv/bin/activate\n' "$C02C_ROOT"
  fi
fi

if [ "$_c02c_rc" -eq 2 ]; then
  # Usage error: the message is already printed, and no checks ran.
  unset -f _c02c_main 2>/dev/null
  if [ "$_c02c_sourced" -eq 1 ]; then
    return 2 2>/dev/null
  else
    exit 2
  fi
fi

printf '\n----------------------------------------\n'
if [ "$_c02c_rc" -ne 0 ]; then
  printf 'NOT READY: %d check(s) failed' "$C02C_FAILED"
  [ "$C02C_WARNED" -gt 0 ] && printf ', %d warning(s)' "$C02C_WARNED"
  printf '\n\nFix what is listed above and run it again.\n'
else
  printf 'READY'
  [ "$C02C_WARNED" -gt 0 ] && printf ' with %d warning(s)' "$C02C_WARNED"
  printf '\n\nProject: %s\nRegion:  %s\nAccount: %s\n\nStart the lab:\n  ./class-02C-work/start_web_server.sh\n' \
    "$C02C_PROJECT" "$C02C_REGION" "$C02C_ACCOUNT"
fi

unset -f _c02c_main 2>/dev/null
if [ "$_c02c_sourced" -eq 1 ]; then
  return "$_c02c_rc" 2>/dev/null
else
  exit "$_c02c_rc"
fi
