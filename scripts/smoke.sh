#!/usr/bin/env bash
# Smoke test against a running dev server (see README for the dev setup).
# Usage: scripts/smoke.sh [host] [user:password]
set -u
HOST=${1:-http://127.0.0.1:8080}
CREDS=${2:-joe:samplepasswd}
fail=0

check() { # label url expected_code [curl extra args...]
    local label=$1 url=$2 expected=$3
    shift 3
    local code
    code=$(curl -s -o /dev/null -w '%{http_code}' "$@" "$HOST$url")
    if [ "$code" = "$expected" ]; then
        echo "ok   $label ($code)"
    else
        echo "FAIL $label (got $code, want $expected)"
        fail=1
    fi
}

check "frontpage         " "/" 200
check "lang switch       " "/lang/es" 303
check "404 page          " "/definitely-not-here" 404
check "atom feed         " "/feed/" 200
check "json get by id    " "/posts/1" 200 --digest -u "$CREDS" -H 'Accept: application/json'

if command -v xmllint > /dev/null; then
    if curl -s "$HOST/feed/" | xmllint --noout -; then
        echo "ok   atom feed is well-formed XML"
    else
        echo "FAIL atom feed is not well-formed XML"
        fail=1
    fi
fi

# First public post slug from the feed, then check its page renders.
slug=$(curl -s "$HOST/feed/" |
    grep -o '/posts/[a-z0-9-]*' | head -1 | sed 's|/posts/||')
if [ -n "$slug" ]; then
    check "post page         " "/posts/$slug" 200
else
    echo "FAIL could not extract a post slug from the feed"
    fail=1
fi

exit $fail
