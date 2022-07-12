#!/bin/bash
set -e
BUILD_PATH=$(nix-build --option tarball-ttl 0  ./release.nix --no-out-link)
echo "Signing path " $BUILD_PATH
nix store sign -k /etc/nix/boro-priv.key  $(nix-store -qR $BUILD_PATH)
echo "Copying new path"
nix copy -v  $BUILD_PATH --to ssh://nixie
echo "The new maki is now on nixie at: $BUILD_PATH"
ssh nixie sudo -u makiblog nix-env -p /nix/var/nix/profiles/per-user/makiblog/profile -i $BUILD_PATH

