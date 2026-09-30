"""Assemble a scene fragment + engine + fonts into one self-contained HTML page.

usage: python3 build.py <out_dir> scenes/film.html [scenes/other.html ...]

A fragment has <title>, <style>, a <div data-slot="stage"> … </div><!--/stage-->
and <script>. Assets (screenshots, logos, soundtrack) are referenced relative
to the built page; build.py copies the fragment's `assets/` folder next to it.
One page serves every format: open it with ?fmt=16x9 | 9x16 | 1x1 | 4x5.
"""
import base64, re, sys, shutil, pathlib

E = pathlib.Path(__file__).resolve().parent
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
CURSOR = ('<svg id="cursor" viewBox="0 0 40 56"><path d="M3 3 L3 41 L12.5 32 L19 47 L25.5 44.2 '
          'L19.2 29.8 L32 29.8 Z" fill="#0B0B0B" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>')


def build(src: pathlib.Path, out: pathlib.Path) -> pathlib.Path:
    frag = src.read_text(encoding='utf-8')
    m = re.search(r'<title>(.*?)</title>', frag)
    title = m.group(1) if m else src.stem
    css = ''.join(re.findall(r'<style>(.*?)</style>', frag, re.S))
    stage = (re.search(r'<div data-slot="stage">(.*?)</div><!--/stage-->', frag, re.S) or [None, ''])[1]
    js = ''.join(re.findall(r'<script>(.*?)</script>', frag, re.S))
    base = (open(E / 'base.css').read()
            .replace('__GEIST__', b64(E / 'fonts/Geist-Variable.woff2'))
            .replace('__GEISTMONO__', b64(E / 'fonts/GeistMono-Medium.woff2'))
            .replace('__DMSANS__', b64(E / 'fonts/DMSans-Variable.woff2')))
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{base}{css}</style></head><body>\n'
            f'<div id="wrap"><div id="stage">{stage}{CURSOR}</div></div>\n'
            f'<script>{open(E / "motion.js").read()}</script>'
            f'<script>{open(E / "lev.js").read()}</script>'
            f'<script>{js}</script></body></html>')
    dst = out / (src.stem + '.html')
    dst.write_text(html, encoding='utf-8')
    assets = src.parent / 'assets'
    if assets.is_dir():
        shutil.copytree(assets, out / 'assets', dirs_exist_ok=True)
    return dst


if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for s in sys.argv[2:]:
        print('built', build(pathlib.Path(s), out))
