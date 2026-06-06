#!/usr/bin/env python3
"""screenshot-resize MCP Server.

Self-contained MCP server providing two tools for generating portfolio thumbnails:

- screenshot_website: render a URL in headless Chromium and save as 600x450 PNG
- resize_image: resize any image to specified dimensions

Designed to be dropped into any project (e.g. card-personal-portfolio) as a
self-contained folder. No imports from a parent project.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from PIL import Image
from mcp.server.fastmcp import FastMCP

from screenshot import capture as _capture

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("screenshot-resize")

mcp = FastMCP("screenshot-resize")


@mcp.tool()
async def screenshot_website(
    url: str,
    output_dir: str = "./images",
    filename: Optional[str] = None,
    wait_seconds: float = 2.0,
) -> str:
    """Capture a website and save as 600x450 PNG.

    Renders the page in headless Chromium at a 1200x900 viewport (4:3) and
    downscales to 600x450 — matching the convention used at
    https://jacobhsu.github.io/card-personal-portfolio/.
    """
    return await _capture(url, output_dir, filename, wait_seconds)


@mcp.tool()
async def resize_image(
    image_path: str,
    width: int,
    height: int,
    output_path: Optional[str] = None,
    maintain_aspect: bool = False,
) -> str:
    """Resize an image to specified dimensions."""
    if not os.path.exists(image_path):
        return f"Error: Image file not found: {image_path}"

    try:
        with Image.open(image_path) as img:
            original_size = img.size
            if maintain_aspect:
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
                resized_img = img
            else:
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

            if not output_path:
                name, ext = os.path.splitext(image_path)
                output_path = f"{name}_resized{ext}"

            resized_img.save(output_path, quality=95)
            return (
                f"Image resized successfully!\n"
                f"Original size: {original_size[0]}x{original_size[1]}\n"
                f"New size: {resized_img.size[0]}x{resized_img.size[1]}\n"
                f"Saved to: {output_path}"
            )
    except Exception as e:
        logger.exception("resize failed")
        return f"Error resizing image: {e}"


if __name__ == "__main__":
    mcp.run()
