#!/bin/bash
mkdir -p ~/.local/bin
for skill in */bin/*; do
  ln -sf "$(pwd)/$skill" ~/.local/bin/$(basename "$skill")
done
echo "Installed: $(ls */bin/* | xargs -I{} basename {})"
