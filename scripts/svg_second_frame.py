"""Render the second frame of an fMRIPrep before/after animated SVG.

fMRIPrep reportlets stack two <g> layers (class "background-svg" and
"foreground-svg"); the CSS animation toggles them. Removing the first layer
leaves the second one visible for a static render.
Usage: python svg_second_frame.py IN.svg OUT.svg
"""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
# Drop CSS animations so nothing toggles visibility.
src = re.sub(r"<style.*?</style>", "", src, flags=re.S)
classes = re.findall(r'class="([^"]*(?:background|foreground)-svg[^"]*)"', src)
drop = sys.argv[3] if len(sys.argv) > 3 else "background"
target = next((c for c in classes if drop in c), None)
if target is None:
    sys.exit(f"no background layer found; classes seen: {classes[:5]}")
start = src.index(f'class="{target}"')
g_open = src.rfind("<g", 0, start)
depth, i = 0, g_open
while True:
    nxt_open = src.find("<g", i + 1)
    nxt_close = src.find("</g>", i + 1)
    if nxt_open != -1 and nxt_open < nxt_close:
        depth += 1
        i = nxt_open
    else:
        if depth == 0:
            end = nxt_close + len("</g>")
            break
        depth -= 1
        i = nxt_close
open(sys.argv[2], "w", encoding="utf-8").write(src[:g_open] + src[end:])
print("removed layer", target)
