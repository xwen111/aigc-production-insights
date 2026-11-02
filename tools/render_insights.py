from pathlib import Path
from html import escape as E
import json
from notes import NOTES,FIGURES
from topics import TOPICS,NETWORK_MD
from render_notes import figure
from diagrams import build as build_diagrams

ROOT=Path(__file__).resolve().parents[1]

def extra(nid):
    if nid=='N17':
        return '''<figure class="overlap-explanation"><h4>先看示意：为什么重复一部分剧情，会多出剪辑空间？</h4><p class="diagram-hint">窄屏可左右滑动图解，查看全部剧情范围与选段。</p><div class="diagram-scroll"><img src="assets/diagrams/overlap.svg" width="1000" height="445" alt="A 生成一二三，B 生成二三四，C 生成三四五。同一剧情重演多次，最终分别取用，不重复讲述。" loading="lazy"></div><figcaption>绿色格子是生成的剧情范围，底下一行是可能的选用方式。这是方法示意，不是实际素材时长或固定滑窗规则。</figcaption></figure><p class="example-lead">再看实测截图：同一包剧情有多个版本，相邻包又可以重叠。最终切在哪里，要看表演、动作与节奏能不能接。</p>'''
    if nid=='N24':
        return '<p class="local-loop"><strong>这一例的完整回路：</strong>选中视频 → 截出问题帧 → 图片只改尺面 → 再生成 / 合成局部视频 → 接回原片 → 连前后一起看。接不上时，回到修复或选段，不默认整条重做。</p>'
    return ''

def build():
    build_diagrams()
    by_id={n['id']:n for n in NOTES};order=[nid for t in TOPICS for nid in t['notes']]
    assert len(order)==len(set(order))==len(NOTES)==34 and set(order)==set(by_id)
    nav=''.join(f'<a href="#topic-{t["id"]}"><span>{t["id"]}</span>{E(t["short"])}</a>' for t in TOPICS)
    quick=''.join(f'<a href="#topic-{t["id"]}">{E(t["short"])}</a>' for t in TOPICS)
    sections=[]
    for t in TOPICS:
        items=[]
        for i,nid in enumerate(t['notes'],1):
            n=by_id[nid];num=int(nid[1:]);origin=n.get('origin','实测复盘')
            badge=f'<span class="origin-badge">{E(origin)}</span>' if origin=='补充建议' else ''
            # 重叠示意紧贴相应洞察，其余截图保留原来的直接阅读方式。
            items.append(f'''<article class="note" id="note-{num:02}"><header><p class="note-number">洞察 {int(t['id'])}.{i} <span>· {E(n['stage'])}</span>{badge}</p><h3>{E(n['title'])}</h3></header><p>{E(n['story'])}</p>{extra(nid) if nid=='N17' else ''}{figure(n)}{extra(nid) if nid=='N24' else ''}<p>{E(n['why'])}</p><p>{E(n['how'])}</p><p class="takeaway">{E(n['insight'])}</p><p class="engine"><strong>如果做成自动化：</strong>{E(n['engine'])}</p></article>''')
        sections.append(f'''<section class="insight-topic" id="topic-{t['id']}"><header class="topic-header"><p class="stage-kicker">一类问题 · {E(t['short'])}</p><h2>{E(t['title'])}</h2><p>{E(t['intro'])}</p></header>{''.join(items)}</section>''')
    html=(ROOT/'tools/insights_template.html').read_text()
    for k,v in {'__NAV__':nav,'__QUICK_NAV__':quick,'__ARTICLES__':''.join(sections)}.items():html=html.replace(k,v)
    (ROOT/'index.html').write_text(html)
    md='''# AIGC 视频制作里的摩擦与洞察

版本 4.0 · 2026-11-02。按六类问题组织 34 条洞察：原有 32 条实测复盘完整保留，N33、N34 是明确标记的实施补充。原始 F01–F39 均有对应。

## 使用方法

以具体摩擦点和例子为主体，不将这些类别读成固定制作阶段。先了解素材关系，再逐条读情境、卡点、做法与判断。N 编号保持稳定，分类重排不改变来源。

第一人称是口述整理，不是逐字引用。“比如”“如果”“可能”不应改写成已发生的事实。新增建议不能冒充创作者已经验证的故障。不同项目的截图不构成同一影片的连续故事。

'''+NETWORK_MD
    for t in TOPICS:
        md+=f"## 分类 {t['id']}：{t['title']}\n\n{t['intro']}\n\n"
        for i,nid in enumerate(t['notes'],1):
            n=by_id[nid]
            md+=f"### 洞察 {int(t['id'])}.{i} · {n['title']}（{nid}）\n\n来源：{n.get('origin','创作者实测复盘')}。\n\n"
            for label,key in [('具体情境','story'),('卡在哪里','why'),('实际做法','how'),('这条经验说明什么','insight'),('自动化要帮什么','engine')]:md+=f"**{label}**\n\n{n[key]}\n\n"
            if nid=='N17':md+='重叠示意：[图解](assets/diagrams/overlap.svg)。同一剧情多演几次，给版本比较和接点选择留余量；最终不重复讲述重叠剧情。\n\n'
            if n['figure']:
                fig=FIGURES[n['figure']];md+='**对应截图**\n\n'
                for filename,label,desc in fig['parts']:md+=f'- [{label}](assets/reading/{filename}.webp)：{desc}\n'
                md+=f"\n{fig['caption']} [原图](assets/{fig['source']}.png)。\n\n"
            else:md+='没有专门截图的口述例子，不补无关图。\n\n'
            md+='**AI 应执行的规则**\n\n'+''.join('- '+r+'\n' for r in n['rules'])+'\n**不要误读**\n\n'+n['avoid']+'\n\n'
    md+=(ROOT/'tools/ai_contract.md').read_text()
    md+='''\n## 引擎必须能记录的回路与网状关系

除了保存“完成了哪一步”，还要保存素材之间的实际关系：

1. `video → extracted_frame`：源视频、时间点、用途（修复或提取参考）。
2. `frame → edited_image`：只改什么、保留什么、依据什么真值修改。
3. `edited_image → replacement_video`：采用再生成、跟踪贴图或合成中的哪种方法；替换哪个区间。
4. `replacement_video → timeline`：接回原序列的版本、区间和验收状态；静帧、全区间、前后接点分别检查。
5. `video → extracted_reference → later_generation`：提取什么对象、哪里是补全猜测、何时被人选中、适用哪些后续镜头。
6. `take → selected_range → edit_segment`：多个 take 可贡献同一段成片，一条 take 可贡献多个局部。保留源与入出点。
7. `generation_group ↔ overlapping_beats`：共同剧情、重演范围、场景/事件边界。重叠不等于自动继承上一条输出。
8. `selected_take_state → next_generation`：在实际模型支持范围内提供已选帧/视频/状态；上游改版则标记相关接点待检查。

这些关系构成版本来源网。生成、修改、提取、组合均产生新版本，保留原素材，不覆盖。自动化可以串行执行低风险操作，但必须允许分叉、局部汇合和回退。
'''
    md+='\n## 旧要点覆盖索引\n\n'
    for t in TOPICS:
        for nid in t['notes']:
            n=by_id[nid];md+=f"- {nid} · {n['title']} ← {', '.join(n['old_ids']) if n['old_ids'] else '新增补充建议'}\n"
    md+='\n原始截图来源：assets/manifest.json；裁切坐标：assets/reading/manifest.json；两张 SVG 为本次根据讨论绘制的方法示意，不是视频模型实测输出。没有原始视频，未验证动态成片。\n'
    (ROOT/'AI_PLAYBOOK.md').write_text(md)
    (ROOT/'frictions.json').write_text(json.dumps(dict(version='4.0',topics=TOPICS,notes=NOTES,figures=FIGURES),ensure_ascii=False,indent=2))
    print(json.dumps(dict(version='4.0',topics=6,notes=len(order),original_points=len({x for n in NOTES for x in n['old_ids']}),md_characters=len(md))))

if __name__=='__main__':build()
