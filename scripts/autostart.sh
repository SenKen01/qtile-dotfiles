#!/usr/bin/env bash

# Перезапускаем picom с нашим конфигом из репозитория
killall -q picom
while pgrep -u $UID -x picom >/dev/null; do sleep 0.2; done
picom --config ~/.config/qtile/scripts/picom.conf -b
