"""只裁掉无关画布，保留原始截图；不重绘、修饰内容。"""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'reading'
OUT.mkdir(exist_ok=True)
# 坐标以原始像素记录，可追溯。
CROPS={
'phone-states':('12-entities',(850,925,1370,1310)),
'takes-pair':('13-takes',(113,33,697,347)),
'summer-top':('01-aesthetic',(665,242,1152,531)),
'summer-bottom':('01-aesthetic',(674,940,1161,1227)),
'character-faces':('02-characters',(250,105,1335,365)),
'character-sheets':('02-characters',(785,575,1595,1010)),
'entities':('12-entities',(60,70,1365,1355)),
'brand':('07-brand',(15,176,1597,735)),
'owl-wide':('06-owl',(48,1012,551,1295)),
'owl-close':('06-owl',(1215,95,1717,378)),
'tennis-player':('08-tennis',(452,529,667,891)),
'tennis-ball':('08-tennis',(778,520,991,904)),
'handshake':('09-handshake',(551,113,855,660)),
'overlap':('03-overlap',(1370,93,2115,1185)),
'takes':('13-takes',(113,33,1505,347)),
'tape-before':('04-tape',(68,807,827,1234)),
'tape-after':('04-tape',(68,112,827,539)),
'notebook-before':('05-notebook',(564,478,1009,729)),
'notebook-after':('05-notebook',(46,70,491,322)),
'clocks-room':('10-clocks',(89,45,719,402)),
'clocks-detail':('10-clocks',(1092,946,1721,1303)),
'bag-frame':('11-emergent',(51,536,380,709)),
'bag-reference':('11-emergent',(545,565,779,737)),
}
records=[]
for name,(source,box) in CROPS.items():
    p=ROOT/'assets'/(source+'.png')
    im=Image.open(p)
    assert box[0]>=0 and box[1]>=0 and box[2]<=im.width and box[3]<=im.height,(name,im.size)
    im.crop(box).convert('RGB').save(OUT/(name+'.webp'),quality=92)
    records.append(dict(file='assets/reading/'+name+'.webp',source='assets/'+source+'.png',crop_pixels=box,operation='crop_only'))
(OUT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('Prepared',len(records),'reading crops')
