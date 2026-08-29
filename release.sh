#!/usr/bin/env bash
set -euo pipefail

# Deploy by building the flake ON the target host, from the GitHub
# master branch. Building on the target means:
#   - the right platform (dev machines may be a different arch/OS)
#   - no store signing needed (local builds are trusted)
# Remember to push to GitHub first: the build uses github:cyraxjoe/maki.
#
# First deploy of >= 0.5.0 (psycopg2 -> psycopg 3): update the sqlalchemy
# url scheme in the server's site.cfg from 'postgresql://' to
# 'postgresql+psycopg://'.
#
# The host specifics are intentionally not committed; they live in an
# untracked .release.env file next to this script:
#
#   DEPLOY_HOST=...      # ssh destination of the server
#   DEPLOY_USER=...      # user that owns the app profile
#   DEPLOY_PROFILE=...   # nix profile path to install into
#   DEPLOY_SERVICE=...   # systemd unit that runs the blog

cd "$(dirname "$0")"
if [ -f .release.env ]; then
    . ./.release.env
fi
: "${DEPLOY_HOST:?set DEPLOY_HOST in .release.env}"
: "${DEPLOY_USER:?set DEPLOY_USER in .release.env}"
: "${DEPLOY_PROFILE:?set DEPLOY_PROFILE in .release.env}"
: "${DEPLOY_SERVICE:?set DEPLOY_SERVICE in .release.env}"

FLAKE='github:cyraxjoe/maki'
NIX="nix --extra-experimental-features 'nix-command flakes'"

echo "Building $FLAKE on $DEPLOY_HOST..."
BUILD_PATH=$(ssh "$DEPLOY_HOST" "$NIX build --refresh --no-link --print-out-paths '$FLAKE'")
echo "Built: $BUILD_PATH"
ssh "$DEPLOY_HOST" "sudo -u $DEPLOY_USER nix-env -p $DEPLOY_PROFILE -i $BUILD_PATH"
echo "Installed into the profile, restarting the service..."
ssh "$DEPLOY_HOST" "sudo systemctl restart $DEPLOY_SERVICE && systemctl --no-pager -l status $DEPLOY_SERVICE | head -8"
echo "The new maki is now live on $DEPLOY_HOST at: $BUILD_PATH"
