"""Website screenshot implementation.

Captures a webpage at a 4:3 viewport (1200x900) and downscales to 600x450 PNG —
matching the project card dimension convention used at
https://jacobhsu.github.io/card-personal-portfolio/.
"""

from __future__ import annotations

import logging
import os
from io import BytesIO
from typing import Optional
from urllib.parse import urlparse

from PIL import Image
from playwright.async_api import async_playwright

logger = logging.getLogger("screenshot-resize.screenshot")

VIEWPORT_W = 1200
VIEWPORT_H = 900
OUTPUT_W = 600
OUTPUT_H = 450


def _derive_filename(url: str) -> str:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    slug = parts[-1] if parts else parsed.netloc.split(".")[0]
    slug = slug.replace(".", "_").replace("-", "_")
    return f"{slug or 'screenshot'}.png"


async def capture(
    url: str,
    output_dir: str = "./images",
    filename: Optional[str] = None,
    wait_seconds: float = 2.0,
) -> str:
    """Capture URL and save as 600x450 PNG."""
    os.makedirs(output_dir, exist_ok=True)
    out_name = filename or _derive_filename(url)
    if not out_name.lower().endswith(".png"):
        out_name = f"{os.path.splitext(out_name)[0]}.png"
    out_path = os.path.join(output_dir, out_name)

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            context = await browser.new_context(
                viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
                device_scale_factor=1,
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30_000)
            if wait_seconds > 0:
                await page.wait_for_timeout(int(wait_seconds * 1000))
            png_bytes = await page.screenshot(type="png", full_page=False)
            await browser.close()
    except Exception as e:
        logger.exception("screenshot failed")
        return f"Error capturing {url}: {e}"

    try:
        with Image.open(BytesIO(png_bytes)) as im:
            captured_size = im.size
            resized = im.resize((OUTPUT_W, OUTPUT_H), Image.Resampling.LANCZOS)
            resized.save(out_path, format="PNG", optimize=True)
    except Exception as e:
        logger.exception("resize failed")
        return f"Error resizing screenshot: {e}"

    return (
        f"Screenshot captured successfully!\n"
        f"URL: {url}\n"
        f"Viewport: {captured_size[0]}x{captured_size[1]}\n"
        f"Output: {OUTPUT_W}x{OUTPUT_H}\n"
        f"Saved to: {out_path}"
    )
