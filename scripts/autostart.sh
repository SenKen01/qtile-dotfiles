#!/usr/bin/env bash

# 1. Композитор (прозрачность и скругления)
killall -q picom
while pgrep -u $UID -x picom >/dev/null; do sleep 0.2; done
picom --config ~/.config/qtile/scripts/picom.conf -b

# 2. Останавливаем предыдущий фоновый цикл обоев, если он был запущен
pkill -f "wallpaper_loop" || true

# 3. Запускаем фоновый процесс обновления обоев каждые 10 минут (600 сек)
(
    exec -a wallpaper_loop bash -c '
        ~/.config/qtile/scripts/collage_maker.py --sync
        while true; do
            sleep 600
            ~/.config/qtile/scripts/collage_maker.py --sync
        done
    '
) &