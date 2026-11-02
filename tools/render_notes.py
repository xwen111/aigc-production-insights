from pathlib import Path
from html import escape as E
import json
from notes import NOTES, FIGURES

ROOT=Path(__file__).resolve().parents[1]
CROP_META={x['file']:x for x in json.loads((ROOT/'assets/reading/manifest.json').read_text())}

def figure(n):
    if not n['show_figure']:return ''
    fig=FIGURES[n['figure']]
    cells=[]
    for filename,label,description in fig['parts']:
        crop=CROP_META['assets/reading/'+filename+'.webp']['crop_pixels']
        width,height=crop[2]-crop[0],crop[3]-crop[1]
        max_width=round(width/height*500)
        cells.append(f'<div class="figure-part" style="width:100%;max-width:{max_width}px;margin-inline:auto"><p class="image-label">{E(label)}</p><img src="assets/reading/{filename}.webp" alt="{E(label+"："+description,quote=True)}" width="{width}" height="{height}" style="aspect-ratio:{width}/{height}" loading="lazy"><p class="image-description">{E(description)}</p></div>')
    cls=' paired' if len(cells)>1 else ' single'
    if n['figure'] in ('character','entities'):cls+=' wide'
    return f'<figure class="example{cls}"><div class="figure-images">'+''.join(cells)+f'</div><figcaption>{E(fig["caption"])} <a href="assets/{fig["source"]}.png" target="_blank" rel="noopener">完整原始截图 ↗</a></figcaption></figure>'

