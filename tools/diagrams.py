from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def wrap(body,w,h,title,desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{desc}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs><style>text{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;fill:#29372d}}.small{{font-size:13px;fill:#697567}}.label{{font-size:17px;font-weight:600}}.wire{{fill:none;stroke:#687d65;stroke-width:2;marker-end:url(#arrow)}}.repair{{stroke:#b47644}}.discover{{stroke:#427e86;stroke-dasharray:7 4}}</style><rect width="100%" height="100%" fill="#fafbf8"/>{body}</svg>'''

def node(x,y,title,line,w=190,h=76,color='#f2f5ee'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{color}" stroke="#c7d2c2"/><text class="label" x="{x+14}" y="{y+29}">{title}</text><text class="small" x="{x+14}" y="{y+54}">{line}</text>'

def build():
    out=ROOT/'assets/diagrams';out.mkdir(exist_ok=True)
    b=''
    for x,t,s in [(30,'故事、情绪与要求','保留可以再改的方向'),(300,'图片探索','选中有感觉的实际图'),(600,'选图后精确修改','个性、文字、必要角度'),(900,'这一段用的参考','角色 / 环境 / 关键细节')]:b+=node(x,35,t,s)
    for a,z in [(220,300),(490,600),(790,900)]:b+=f'<path class="wire" d="M{a} 73H{z}"/>'
    b+='<path class="wire" d="M995 111V245"/><text class="small" x="1006" y="180">带剧情生成</text>'
    b+='<rect x="910" y="233" width="190" height="115" rx="5" fill="#dde5d7"/><rect x="905" y="239" width="190" height="115" rx="5" fill="#e9eee3"/>'
    b+=node(900,245,'同一段戏，几种演法','A / B / C 都是素材',h=115)
    b+='<text class="small" x="915" y="328">每条都可能只有局部好</text>'
    b+=node(600,260,'从每条里挑几秒','A 的前段 + B 的反应',h=95)
    for y in [278,304,337]:b+=f'<path class="wire" d="M900 {y}H790"/>'
    b+=node(300,260,'组合、试剪','放到前后镜头里看',h=95)
    b+=node(30,260,'连着看整片','表达成立、素材够用',h=95)
    b+='<path class="wire" d="M600 307H490"/><path class="wire" d="M300 307H220"/>'
    b+='<path class="wire repair" d="M995 360V425"/><text class="small" x="1006" y="397">取一帧出来</text>'
    b+=node(900,425,'视频抽帧','视频输出 → 图片输入',color='#fbf0e5')
    b+=node(600,425,'图片精修','保住构图，修字或细节',color='#fbf0e5')
    b+=node(300,425,'局部再生成 / 合成','修好的图 → 替换视频',color='#fbf0e5')
    b+='<path class="wire repair" d="M900 463H790"/><path class="wire repair" d="M600 463H490"/><path class="wire repair" d="M395 425V355"/>'
    b+='<text class="small" x="407" y="392">接回试剪，检查动作与文字稳定</text>'
    b+='<path class="wire repair" d="M490 330H540V535H695V501"/><text class="small" x="365" y="553">接回仍不自然 → 回到图片修改</text>'
    b+='<path class="wire" d="M600 280C565 280 565 185 700 185H865V270H900"/><text class="small" x="620" y="170">缺一个动作 / 表情 → 定向补拍</text>'
    b+='<path class="wire discover" d="M995 501V555"/>'
    b+=node(900,555,'提取新道具参考','袋子、手表先在视频出现',h=76,color='#eaf3f3')
    b+='<path class="wire discover" d="M1090 593H1125V73H1090"/><text class="small" x="600" y="581">新发现回到参考库，供后续镜头延续</text>'
    b+='<text class="small" x="30" y="565">绿色：生成、选择与组合</text><text class="small" x="30" y="590">棕色：抽帧 → 改图 → 替换视频 → 接回</text><text class="small" x="30" y="615">蓝色虚线：从视频发现并提取新参考</text>'
    (out/'network.svg').write_text(wrap(b,1150,655,'AIGC 素材怎样分叉、汇合与回流','视频既能进入选片剪辑，也能抽帧给图片模型修改；修好的图片再生成或合成为替换视频，接回剪辑。视频中的新道具也能提取为后续参考。多个候选可以分别贡献局部片段。'))
    b='<text class="label" x="24" y="32">同一场景里，给相邻剧情留下重演的部分</text>'
    for i in range(5):b+=f'<text class="small" x="{200+i*155}" y="73">剧情 {i+1}</text>'
    colors=['#edf2e7','#dbe8d4','#c7dcbc']
    for r,(name,start) in enumerate([('生成组 A',0),('生成组 B',1),('生成组 C',2)]):
        y=95+r*76;b+=f'<text class="label" x="24" y="{y+35}">{name}</text>'
        for i in range(start,start+3):
            x=175+i*155;b+=f'<rect x="{x}" y="{y}" width="140" height="56" fill="{colors[r]}" stroke="#9fb694"/><text x="{x+25}" y="{y+35}" font-size="16">剧情 {i+1}</text>'
    b+='<text class="small" x="24" y="337">剪辑时：</text>'
    for i,group in enumerate(['A','B','B','C','C']):
        x=175+i*155;b+=f'<rect x="{x}" y="308" width="140" height="48" fill="#526d49"/><text x="{x+15}" y="338" style="fill:white;font-size:14px">从 {group} 选这一段</text>'
    b+='<text class="small" x="175" y="388">重复剧情不重复讲：从不同演法里找更好的瞬间与接点。</text><text class="small" x="175" y="414">这只是示意，窗口大小、候选数量和切点按实际剧情决定。</text>'
    (out/'overlap.svg').write_text(wrap(b,1000,445,'重叠生成怎样变成剪辑余量','组 A 生成剧情一二三，B 生成二三四，C 生成三四五。相同剧情有多个演法，最终剪辑分别选用局部，不重复播放相同剧情。'))
    print('Generated 2 explanatory diagrams')

if __name__=='__main__':build()
