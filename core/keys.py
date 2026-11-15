from libqtile.config import Key, Drag, Click
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"  # Клавиша Super (Win)
terminal = guess_terminal()

keys = [
    # Запуск Rofi (меню приложений)
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    
    #обновление обоевS
    Key([mod, "shift"], "w", lazy.spawn("/home/master/.config/qtile/scripts/collage_maker.py"), desc="Обновить Pinterest-коллаж"),

    #Переключение расскладки клавиатуры на Alt+Space
    #Key([mod], "space", lazy.widget["KeyboardLayout"].next_keyboard(), desc="Сменить расскладку(win+Space)"),
    Key(["mod1"], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Сменить раскладку"),    
    # Переключение фокуса между окнами
    Key([mod], "h", lazy.layout.left(), desc="Фокус влево"),
    Key([mod], "l", lazy.layout.right(), desc="Фокус вправо"),
    Key([mod], "j", lazy.layout.down(), desc="Фокус вниз"),
    Key([mod], "k", lazy.layout.up(), desc="Фокус вверх"),
    Key([mod], "space", lazy.layout.next(), desc="Следующее окно"),

    # Перемещение окон
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Сдвинуть окно влево"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Сдвинуть окно вправо"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Сдвинуть окно вниз"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Сдвинуть окно вверх"),

    # Изменение размера окон
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Расширить влево"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Расширить вправо"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Расширить вниз"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Расширить вверх"),
    Key([mod], "n", lazy.layout.normalize(), desc="Сбросить размеры окон"),

    # Базовые действия с окнами и Qtile
    Key([mod], "Return", lazy.spawn(terminal), desc="Открыть терминал"),
    Key([mod], "Tab", lazy.next_layout(), desc="Сменить раскладку"),
    Key([mod], "w", lazy.window.kill(), desc="Закрыть активное окно"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Полноэкранный режим"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Плавающий режим"),
    Key([mod], "r", lazy.spawncmd(), desc="Быстрый запуск команды на панели"),

    # Управление самой сессией Qtile
    Key([mod, "control"], "r", lazy.reload_config(), desc="Перезагрузить конфиг"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Выйти из Qtile"),
]

# Управление плавающими окнами мышью (Super + ЛКМ / ПКМ)
# mouse = [
#     Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
#     Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
#     Click([mod], "Button2", lazy.window.bring_to_front()),
# ]
