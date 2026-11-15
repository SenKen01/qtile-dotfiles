#!/usr/bin/env python3
import os
import sys
import re
import json
import random
import hashlib
import xml.etree.ElementTree as ET
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

sys.path.append(os.path.expanduser("~/.config/qtile"))
from core.wallpaper_config import (
    PINTEREST_BOARD_URL,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BASE_GAP,
    LARGE_GAP_X,
    LARGE_GAP_Y,
    CORNER_RADIUS,
    BG_COLOR,
    CACHE_DIR,
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


def resolve_board_urls(short_url):
    resp = requests.get(short_url, headers=HEADERS, allow_redirects=True, timeout=10)
    full_url = resp.url.split("?")[0].rstrip("/")
    return full_url, f"{full_url}.rss"


def fetch_image_links(full_url, rss_url):
    img_urls = set()
    try:
        r = requests.get(rss_url, headers=HEADERS, timeout=10)
        if r.status_code == 200 and "<rss" in r.text:
            root = ET.fromstring(r.text)
            for desc in root.findall(".//item/description"):
                if desc.text:
                    for u in re.findall(r'https://i\.pinimg\.com/[^\s"\'<>]+', desc.text):
                        img_urls.add(re.sub(r'/\d+x/', '/736x/', u))
    except Exception:
        pass

    try:
        r = requests.get(full_url, headers=HEADERS, timeout=10)
        for u in re.findall(r'https://i\.pinimg\.com/(?:originals|736x)/[a-zA-Z0-9/_-]+\.(?:jpg|jpeg|png|webp)', r.text):
            img_urls.add(u)
    except Exception:
        pass

    return list(img_urls)
def get_image_visual_hash(img_path):
    try:
        with Image.open(img_path) as img:
            small = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
            pixels = list(small.getdata())
            avg = sum(pixels) / len(pixels)
            return "".join("1" if p > avg else "0" for p in pixels)
    except Exception:
        return None


def sync_cache(cache_path, max_new=15):
    os.makedirs(cache_path, exist_ok=True)
    existing_content_hashes = set()

    for f in os.listdir(cache_path):
        if f.startswith("pin_"):
            try:
                with open(os.path.join(cache_path, f), "rb") as file_obj:
                    existing_content_hashes.add(hashlib.md5(file_obj.read()).hexdigest())
            except Exception:
                pass

    try:
        full_url, rss_url = resolve_board_urls(PINTEREST_BOARD_URL)
        links = fetch_image_links(full_url, rss_url)
        random.shuffle(links)
        downloaded = 0

        for url in links:
            if downloaded >= max_new:
                break
            try:
                data = requests.get(url, headers=HEADERS, timeout=8).content
                content_hash = hashlib.md5(data).hexdigest()
                if content_hash in existing_content_hashes:
                    continue

                ext = os.path.splitext(url) or ".jpg"
                filepath = os.path.join(cache_path, f"pin_{content_hash[:12]}{ext}")
                with open(filepath, "wb") as f:
                    f.write(data)
                existing_content_hashes.add(content_hash)
                downloaded += 1
            except Exception:
                pass
    except Exception as e:
        print(f"[!] Ошибка синхронизации Pinterest: {e}")

def get_valid_images_with_orientation(cache_path):
    if not os.path.exists(cache_path):
        return [], []

    portrait = []
    landscape = []

    for f in os.listdir(cache_path):
        if not (f.startswith("pin_") and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))):
            continue
        path = os.path.join(cache_path, f)
        try:
            with Image.open(path) as img:
                w, h = img.size
                if w < 450 or h < 450:
                    continue
                if h > w * 1.1:
                    portrait.append(path)
                else:
                    landscape.append(path)
        except Exception:
            pass

    return portrait, landscape


def pick_unique_by_orientation(portrait, landscape, cache_path):
    history_file = os.path.join(cache_path, "last_used.json")
    last_used = set()
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                last_used = set(json.load(f))
        except Exception:
            pass

    all_imgs = portrait + landscape
    if len(all_imgs) < 3:
        return []

    def filter_fresh(pool):
        fresh = [p for p in pool if p not in last_used]
        return fresh if fresh else pool

    p_pool = filter_fresh(portrait) if portrait else filter_fresh(all_imgs)
    l_pool = filter_fresh(landscape) if len(landscape) >= 2 else filter_fresh(all_imgs)

    random.shuffle(p_pool)
    random.shuffle(l_pool)

    selected = []
    seen_hashes = set()

    for img in p_pool:
        h = get_image_visual_hash(img)
        if h and h not in seen_hashes:
            seen_hashes.add(h)
            selected.append(img)
            break

    for img in l_pool:
        if len(selected) == 3:
            break
        h = get_image_visual_hash(img)
        if h and h not in seen_hashes:
            seen_hashes.add(h)
            selected.append(img)

    for img in all_imgs:
        if len(selected) == 3:
            break
        h = get_image_visual_hash(img)
        if h and h not in seen_hashes:
            seen_hashes.add(h)
            selected.append(img)

    try:
        with open(history_file, "w") as f:
            json.dump(selected, f)
    except Exception:
        pass

    return selected


def create_ambient_background(bg_img_path):
    base = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), BG_COLOR)
    try:
        with Image.open(bg_img_path) as img:
            img = img.convert("RGB")
            target_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
            img_ratio = img.width / img.height
            if img_ratio > target_ratio:
                new_w = int(img.height * target_ratio)
                offset = (img.width - new_w) // 2
                img = img.crop((offset, 0, offset + new_w, img.height))
            else:
                new_h = int(img.width / target_ratio)
                offset = (img.height - new_h) // 2
                img = img.crop((0, offset, img.width, offset + new_h))

            img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.Resampling.LANCZOS)
            img = img.filter(ImageFilter.GaussianBlur(radius=45))
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.24)
            base = img.convert("RGBA")
    except Exception:
        pass

    overlay = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    step = 40
    for x in range(0, SCREEN_WIDTH, step):
        for y in range(0, SCREEN_HEIGHT, step):
            draw.point((x, y), fill=(122, 162, 247, 35))

    return Image.alpha_composite(base, overlay)

def fit_contain_clean(img_path, max_w, max_h, radius):
    with Image.open(img_path) as img:
        img = img.convert("RGBA")
        scale = min(max_w / img.width, max_h / img.height)
        new_w = int(img.width * scale)
        new_h = int(img.height * scale)

        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        mask = Image.new("L", (new_w, new_h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (new_w, new_h)], radius=radius, fill=255)
        img.putalpha(mask)

        border_layer = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(border_layer)
        b_draw.rounded_rectangle(
            [(0, 0), (new_w - 1, new_h - 1)],
            radius=radius,
            outline=(122, 162, 247, 140),
            width=2,
        )
        img = Image.alpha_composite(img, border_layer)
        return img


def generate_air_slots():
    W, H = SCREEN_WIDTH, SCREEN_HEIGHT
    TOP_OFFSET = 38
    usable_h = H - TOP_OFFSET - BASE_GAP

    hero_w = int((W - 3 * BASE_GAP) * 0.45)
    side_area_w = W - hero_w - 2 * BASE_GAP

    hero_on_left = random.choice([True, False])

    if hero_on_left:
        hero_x = BASE_GAP
        side_start_x = hero_x + hero_w
    else:
        side_start_x = 0
        hero_x = side_area_w + BASE_GAP

    slots = []
    slots.append((hero_x, TOP_OFFSET, hero_w, usable_h))

    inner_h = H - TOP_OFFSET - 3 * LARGE_GAP_Y
    card1_h = int(inner_h * 0.48)
    card2_h = inner_h - card1_h

    card1_w = int((side_area_w - 2 * LARGE_GAP_X) * 0.85)
    card2_w = int((side_area_w - 2 * LARGE_GAP_X) * 0.90)

    if random.choice([True, False]):
        card1_x = side_start_x + LARGE_GAP_X
        card2_x = side_start_x + side_area_w - card2_w - LARGE_GAP_X
    else:
        card1_x = side_start_x + side_area_w - card1_w - LARGE_GAP_X
        card2_x = side_start_x + LARGE_GAP_X

    card1_y = TOP_OFFSET + LARGE_GAP_Y
    card2_y = card1_y + card1_h + LARGE_GAP_Y

    slots.append((card1_x, card1_y, card1_w, card1_h))
    slots.append((card2_x, card2_y, card2_w, card2_h))

    return slots


def main():
    cache_path = os.path.expanduser(CACHE_DIR)
    output_wallpaper = os.path.join(cache_path, "current_collage.png")

    if not os.path.exists(cache_path) or len(os.listdir(cache_path)) < 5 or "--sync" in sys.argv:
        sync_cache(cache_path)

    portrait, landscape = get_valid_images_with_orientation(cache_path)
    selected = pick_unique_by_orientation(portrait, landscape, cache_path)

    if len(selected) < 3:
        print("[!] Недостаточно качественных уникальных картинок в кэше.")
        return

    canvas = create_ambient_background(selected[0])
    slots = generate_air_slots()

    for img_path, (slot_x, slot_y, slot_w, slot_h) in zip(selected, slots):
        try:
            tile = fit_contain_clean(img_path, slot_w, slot_h, CORNER_RADIUS)
            paste_x = slot_x + (slot_w - tile.width) // 2
            paste_y = slot_y + (slot_h - tile.height) // 2
            canvas.paste(tile, (paste_x, paste_y), tile)
        except Exception as e:
            print(f"[!] Ошибка обработки {img_path}: {e}")

    canvas.convert("RGB").save(output_wallpaper, "PNG", quality=95)
    os.system(f"feh --bg-fill {output_wallpaper}")


if __name__ == "__main__":
    main()