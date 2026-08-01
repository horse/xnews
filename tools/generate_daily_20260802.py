#!/usr/bin/env python3
from pathlib import Path
import json, shutil, re

ROOT=Path('.')
DATE='2026-08-02'; ZHDATE='2026年8月2日'; JADATE='2026年8月2日'; PUB='2026-08-02T06:00:00+09:00'
articles=[
{
'slug':'july-heat-low-rain','level':'focus','cats_zh':['社会','天气','防灾'],'cats_ja':['社会','気象','防災'],'tags_zh':['气象厅','高温','少雨','热中症','农业'],'tags_ja':['気象庁','高温','少雨','熱中症','農業'],
'zh_title':'气象厅总结7月高温少雨，进入8月后仍需防范热中暑与用水风险','ja_title':'気象庁、7月の高温・少雨を公表　8月も熱中症と水利用への警戒続く',
'zh_summary':'日本气象厅8月1日公布7月高温和少雨情况及后续展望，提醒进入8月后仍需警惕持续高温对健康、农业和水资源造成的影响。','ja_summary':'気象庁は8月1日、7月の高温・少雨の状況と今後の見通しを公表した。8月に入っても熱中症、農作物、水利用への影響を見据えた備えが必要になる。',
'zh_body':['日本气象厅8月1日发布了“7月的高温、少雨状况及今后展望”。这份资料把夏季天气从每日体感上升为全国性风险判断，关注重点包括持续高温、降水偏少以及这些现象对生活和生产活动的叠加影响。','进入8月后，高温并不会因为月份更替而自然缓解。对个人而言，风险集中在长时间户外活动、夜间降温不足和室内缺乏空调的环境；对地方政府和企业而言，则需要继续安排避暑空间、调整户外作业并关注电力和供水需求。','少雨的影响通常比一次强降雨更不容易被即时感知，却可能逐步反映在水库、河川流量、农作物生长和城市绿化上。农业地区若同时遭遇高温与降水不足，灌溉和作物品质的压力会进一步上升。','日本X上的相关讨论主要围绕“酷暑何时结束”、学校和活动的防暑安排、空调使用以及农产品价格展开。气象信息在这一阶段的意义，不只是预报当天温度，更在于帮助家庭和机构把防暑及节水措施延续到整个8月。'],
'ja_body':['気象庁は8月1日、「7月の高温・少雨の状況と今後の見通し」を公表した。日々の暑さを個別の天気として捉えるだけでなく、全国的な高温と降水不足が生活、農業、水利用に及ぼす影響をまとめて確認する資料となる。','8月に入っても、月が変わっただけで暑さの危険が解消するわけではない。長時間の屋外活動、夜間も気温が下がりにくい環境、冷房を十分に使えない室内では、引き続き熱中症への警戒が必要だ。自治体や事業者には、涼を取れる場所の確保や屋外作業時間の見直しが求められる。','少雨は豪雨ほど目立たない一方、水源、河川流量、農作物、都市の緑地に時間をかけて影響する。高温と降水不足が重なれば、灌漑用水の確保や作物の品質、電力需要にも負担が広がる可能性がある。','日本のXでは、猛暑の長期化、学校行事や屋外イベントの安全対策、冷房利用、農産物価格への影響が話題となった。今回の発表は、日々の最高気温を見るだけでなく、8月を通じて暑さと水不足への備えを続ける必要性を示している。'],
'sources':[('気象庁','https://www.jma.go.jp/jma/press/kako.html?t=0&y=07')]
},
{
'slug':'water-day-2026','level':'focus','cats_zh':['社会','环境'],'cats_ja':['社会','環境'],'tags_zh':['水之日','水之周','水资源','节水'],'tags_ja':['水の日','水の週間','水資源','節水'],
'zh_title':'日本迎来“水之日”，8月1日至7日开展水之周活动','ja_title':'8月1日は「水の日」　7日まで「水の週間」、水資源を考える機会に',
'zh_summary':'8月1日是日本“水之日”，同日起至7日为“水之周”。在高温和少雨受到关注的背景下，水资源、节水和河川环境成为本周公共宣传重点。','ja_summary':'8月1日は「水の日」で、同日から7日までは「水の週間」とされる。高温と少雨が注目される中、水資源、節水、河川環境を考える機会となる。',
'zh_body':['日本政府的月度行事资料将8月1日列为“水之日”，并把8月1日至7日定为“水之周”。这一安排旨在提醒公众重新认识水资源的有限性、供水设施的重要性以及河川和水环境与日常生活之间的联系。','水在日本城市生活中往往以稳定的自来水服务出现，因此容易被视为理所当然。但从水源涵养、净水、输送到污水处理，每一个环节都依赖长期基础设施投资和地方管理。极端高温、少雨和集中豪雨并存，也使水资源管理面临更复杂的条件。','家庭层面的节水并不意味着牺牲卫生，而是减少不必要的长流水、及时检查漏水、合理使用洗衣和洗浴设备。企业和公共设施则需要通过设备更新、循环利用和风险预案降低用水压力。','今年的“水之周”与气象厅对高温和少雨的提醒相互呼应。日本X上与“水の日”相关的投稿包括地方活动、河川照片、节水倡议和儿童教育内容，使纪念日成为理解基础设施与自然环境的入口。'],
'ja_body':['政府広報の8月行事では、8月1日が「水の日」、1日から7日までが「水の週間」と位置付けられている。水資源の有限性、安定した水道を支える施設、河川や水環境と暮らしの関係を見直すための期間だ。','都市では蛇口をひねれば水が出るため、その仕組みは意識されにくい。しかし、水源の保全、浄水、送水、下水処理までには継続的な設備投資と地域の管理が欠かせない。猛暑、少雨、局地的な豪雨が同時に起こり得る時代には、水の確保と災害対策を一体で考える必要がある。','家庭での節水は衛生を犠牲にすることではなく、流しっぱなしを避け、漏水を点検し、洗濯や入浴設備を効率的に使うことから始まる。企業や公共施設には、節水型設備、再利用、供給途絶に備えた計画が求められる。','今年の「水の週間」は、気象庁が示した高温・少雨への注意とも重なる。日本のXでは、自治体の催し、川の風景、節水の呼び掛け、子ども向け学習企画などが共有され、水を支える自然と社会基盤を考えるきっかけとなった。'],
'sources':[('政府広報オンライン','https://www.gov-online.go.jp/data_room/calendar/202608/')]
},
{
'slug':'tif2026-august1','level':'focus','cats_zh':['文化','偶像','娱乐'],'cats_ja':['文化','アイドル','エンタメ'],'tags_zh':['TOKYO IDOL FESTIVAL 2026','TIF2026','台场','偶像'],'tags_ja':['TOKYO IDOL FESTIVAL 2026','TIF2026','お台場','アイドル'],
'zh_title':'TOKYO IDOL FESTIVAL 2026进入第二日，台场多舞台演出持续','ja_title':'TIF2026が2日目　お台場・青海で多彩なアイドルステージ続く',
'zh_summary':'TOKYO IDOL FESTIVAL 2026于8月1日在东京台场、青海一带进入第二日。活动为期三天，现场设置多舞台演出、交流和联动企划。','ja_summary':'TOKYO IDOL FESTIVAL 2026は8月1日、お台場・青海周辺で2日目を迎えた。3日間の日程で、多数のステージや交流企画、コラボ企画が展開されている。',
'zh_body':['TOKYO IDOL FESTIVAL 2026于8月1日在东京台场、青海一带进入第二日。官方日程为7月31日至8月2日，活动通过多个舞台和场内区域，把大型团体、新人组合、地方偶像及相关文化企划集中在同一城市空间内。','今年活动除常规演出外，还安排了谈话、物贩、特典会、摄影企划和跨领域合作。TIF官网在8月1日更新了相关企划信息，显示现场节目仍在按日程不断调整和补充。','这种大型偶像节的意义不仅在于单场演出。不同规模的团体共享观众和媒体注意力，年轻组合可以接触新的受众，地方团队也能借东京活动扩大认知；对粉丝而言，多舞台结构则意味着需要在有限时间内选择观看路线。','日本X上的TIF讨论主要由演出报告、舞台照片、时间表提醒和成员感想构成。由于活动仍将持续到8月2日，本期报道只确认第二日的举行和官方公布的整体结构，不把未经官方确认的现场传闻写入事实部分。'],
'ja_body':['「TOKYO IDOL FESTIVAL 2026」は8月1日、東京・お台場と青海周辺で2日目を迎えた。公式日程は7月31日から8月2日までの3日間で、複数のステージと会場内エリアに、大規模グループ、新人、地域を拠点とするアイドル、関連企画が集まる。','通常のライブに加え、トーク、物販、特典会、撮影企画、他分野とのコラボレーションが組まれている。公式サイトは8月1日にも企画情報を更新しており、会期中も各プログラムの案内が続いている。','大規模なアイドルフェスは、一つの公演を楽しむだけの場ではない。異なる規模のグループが観客とメディアの関心を共有し、新人や地域発のグループが新しい層に触れる機会となる。観客側には、同時進行するステージから観覧ルートを組み立てる楽しさと難しさがある。','日本のXでは、出演報告、ステージ写真、タイムテーブルの共有、メンバーの感想が相次いだ。イベントは2日まで続くため、本稿では2日目の開催と公式に示された構成を中心に扱い、未確認の現場情報は事実として採用していない。'],
'sources':[('TOKYO IDOL FESTIVAL 2026','https://official.idolfes.com/s/tif2026/')]
},
{
'slug':'treasure-ig-arena','level':'standard','cats_zh':['音乐','娱乐'],'cats_ja':['音楽','エンタメ'],'tags_zh':['TREASURE','IG Arena','名古屋','巡回演出'],'tags_ja':['TREASURE','IGアリーナ','名古屋','ツアー'],
'zh_title':'TREASURE日本巡演抵达名古屋，IG Arena举行首日演出','ja_title':'TREASURE日本ツアーが名古屋へ　IGアリーナで初日公演',
'zh_summary':'韩国男子组合TREASURE的日本巡演8月1日在名古屋IG Arena举行首日演出，8月2日还将继续第二场，之后转往福井、福冈和东京。','ja_summary':'TREASUREの日本ツアーは8月1日、名古屋のIGアリーナで初日公演を迎えた。2日にも同会場で公演し、その後は福井、福岡、東京へ続く。',
'zh_body':['TREASURE的日本巡演“TREASURE THE STAGE 2026 IN JAPAN”8月1日在名古屋IG Arena举行首日演出。官方公布的时间为17时开场、18时开演，8月2日还将在同一场馆安排第二场。','本轮巡演7月从大阪开始，随后经过横滨和神户。名古屋站之后，日程还包括福井、福冈和东京有明Arena，形成横跨多个主要城市的大型巡回演出。','连续两日使用大型场馆，显示日本市场仍是TREASURE海外活动的重要部分。巡演也带动了交通、住宿、周边商品和粉丝交流等场馆外活动。','日本X上的相关投稿集中于入场、演出期待、会场交通和粉丝之间的信息交换。由于官方页面没有公开完整曲目和现场细节，本稿不对未经确认的表演内容作具体描述。'],
'ja_body':['TREASUREの日本ツアー「TREASURE THE STAGE 2026 IN JAPAN」は8月1日、名古屋のIGアリーナで初日公演を迎えた。公式日程では17時開場、18時開演で、2日にも同会場で2公演目が予定されている。','ツアーは7月の大阪公演から始まり、横浜、神戸を経て名古屋に到着した。今後は福井、福岡、東京・有明へ続き、日本の主要都市を結ぶ大規模な日程となっている。','大型会場で2日間公演を行うことは、日本市場がTREASUREの海外活動で重要な位置を占めていることを示す。公演は会場内だけでなく、交通、宿泊、グッズ購入、ファン同士の交流にも動きを生む。','日本のXでは、入場案内、公演への期待、会場までの移動、ファン間の情報共有が続いた。公式ページではセットリストや当日の詳細を公表していないため、本稿では未確認の演出内容を事実として記載していない。'],
'sources':[('TREASURE 日本公式','https://ygex.jp/treasure/news/detail.php?id=1132098')]
},
{
'slug':'metopoli-summer-festival','level':'standard','cats_zh':['社会','东京','文化'],'cats_ja':['社会','東京','文化'],'tags_zh':['警视厅','警察博物馆','Metopoli','五反田'],'tags_ja':['警視庁','ポリスミュージアム','メトポリ','五反田'],
'zh_title':'警视厅“Metopoli夏祭”开幕，警察博物馆展出频道道具和纪念资料','ja_title':'警視庁「メトポリ夏まつり」開幕　動画の小道具や記念資料を展示',
'zh_summary':'警视厅8月1日在五反田警察博物馆启动“2026大家的Metopoli夏祭”，纪念官方YouTube频道订阅人数达到10万，活动持续至8月30日。','ja_summary':'警視庁は8月1日、五反田のポリスミュージアムで「2026みんなのメトポリ夏まつり」を始めた。公式YouTube登録者10万人を記念し、30日まで開催する。',
'zh_body':['警视厅8月1日在东京五反田的警察博物馆启动“2026大家的Metopoli夏祭”。活动由博物馆与警视厅官方YouTube内容“Metopoli”合作举办，背景是频道订阅人数达到10万。','展览包括介绍“Metopoli”历史的面板、YouTube银色奖牌以及视频中使用过的道具，并设置摄影区。活动期间还将每天按先到顺序发放纪念品，数量有限。','活动持续至8月30日，星期一闭馆，开放时间为9时30分至16时，入馆和参加均免费。警视厅同时提示，活动可能因天气等情况取消。','警察机构近年来 increasingly 通过视频和社交平台解释工作内容、交通安全及防犯知识。此次活动把线上传播转化为线下展示，也为家庭和儿童提供了接触公共安全教育的入口。'],
'ja_body':['警視庁は8月1日、東京・五反田のポリスミュージアムで「2026みんなのメトポリ夏まつり」を始めた。警察博物館と警視庁公式YouTubeの人気コンテンツ「メトポリ」が連携し、チャンネル登録者10万人達成を記念する。','会場では「メトポリ」の歩みを紹介するパネル、YouTubeの「銀の盾」、動画で使用した小道具を展示する。写真撮影スポットも設け、開催期間中は毎日、先着順で数量限定の記念品を配布する。','開催は8月30日までの26日間で、月曜日は休館。開館時間は午前9時30分から午後4時までで、入館料と参加費は無料となる。天候などの事情で中止する場合がある。','警察機関は近年、動画やSNSを通じて業務、交通安全、防犯情報を発信している。今回の催しは、オンラインで育ったコンテンツを実物展示へ広げ、家族や子どもが公共安全に触れる場として位置付けられる。'],
'sources':[('警視庁','https://www.keishicho.metro.tokyo.lg.jp/about_mpd/welcome/welcome/event_metro.html')]
}
]

def js_write(path,var,items):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(f'window.{var}=(window.{var}||[]).concat('+json.dumps(items,ensure_ascii=False,separators=(',',':'))+');',encoding='utf-8')

zh=[]; ja=[]
for a in articles:
    zh.append({'slug':a['slug'],'level':a['level'],'title':a['zh_title'],'summary':a['zh_summary'],'body':a['zh_body'],'categories':a['cats_zh'],'tags':a['tags_zh'],'sources':a['sources']})
    ja.append({'slug':a['slug'],'level':a['level'],'title':a['ja_title'],'summary':a['ja_summary'],'body':a['ja_body'],'categories':a['cats_ja'],'tags':a['tags_ja'],'sources':a['sources']})
for i in range(1,6):
    js_write(ROOT/f'assets/data-{i}.js','XNEWS_ARTICLES',zh[i-1:i])
    js_write(ROOT/f'assets/ja-data-{i}.js','XNEWS_JA_ARTICLES',ja[i-1:i])
meta={'site':{'name':'XNEWS','tagline':'日本 X 热门新闻日报','date':ZHDATE,'dateISO':DATE,'published':PUB,'modified':PUB,'base':'/xnews'},'categorySlugs':{},'tagSlugs':{}}
(ROOT/'assets/data-meta.js').write_text('window.XNEWS_META='+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
(ROOT/'assets/ja-meta.js').write_text('window.XNEWS_JA_META='+json.dumps({'site':{'date':JADATE,'dateISO':DATE,'published':PUB,'base':'/xnews','jaBase':'/xnews/ja'}},ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
# adapt renderers to current date and flexible categories/tags
for p in ['assets/site.js','assets/ja-site.js']:
    t=(ROOT/p).read_text(encoding='utf-8').replace('2026/08/01','2026/08/02').replace('8月1日','8月2日').replace('7月31日','8月1日')
    t=t.replace('29篇独立报道','5篇独立报道').replace('主要ニュース10本、その他19本。','主要ニュース3本、その他2本。').replace('記事29本','記事5本').replace('主要10本','主要3本').replace('その他19本','その他2本')
    t=t.replace('const catSlug=c=>D.categorySlugs[c];','const catSlug=c=>D.categorySlugs[c]||encodeURIComponent(c);').replace('const tagSlug=t=>D.tagSlugs[t];','const tagSlug=t=>D.tagSlugs[t]||encodeURIComponent(t);')
    (ROOT/p).write_text(t,encoding='utf-8')
# pages
scripts='<script src="/xnews/assets/data-meta.js"></script>'+''.join(f'<script src="/xnews/assets/data-{i}.js"></script>' for i in range(1,6))+'<script src="/xnews/assets/site.js"></script>'
jascripts='<script src="/xnews/assets/ja-meta.js"></script>'+''.join(f'<script src="/xnews/assets/ja-data-{i}.js"></script>' for i in range(1,6))+'<script src="/xnews/assets/ja-site.js"></script>'
def html(lang,title,page,slug='',ja=False):
    attr=f' data-slug="{slug}"' if slug else ''
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}｜XNEWS</title><link rel="stylesheet" href="/xnews/assets/style.css"></head><body data-page="{page}"{attr}><div id="app"></div>{jascripts if ja else scripts}</body></html>'
(ROOT/'2026/08/02').mkdir(parents=True,exist_ok=True); (ROOT/'2026/08/02/index.html').write_text(html('zh-CN',f'{ZHDATE} 日本X热门新闻日报','edition'),encoding='utf-8')
(ROOT/'2026/08/02/reports').mkdir(parents=True,exist_ok=True)
(ROOT/'ja/2026/08/02').mkdir(parents=True,exist_ok=True); (ROOT/'ja/2026/08/02/index.html').write_text(html('ja',f'{JADATE} 日本Xニュース日報','edition',ja=True),encoding='utf-8')
for a in articles:
    (ROOT/f'2026/08/02/reports/{a["slug"]}.html').write_text(html('zh-CN',a['zh_title'],'article',a['slug']),encoding='utf-8')
    d=ROOT/f'ja/2026/08/02/{a["slug"]}'; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(html('ja',a['ja_title'],'article',a['slug'],True),encoding='utf-8')
# home points to new edition via renderer; create WP markdown
cdir=ROOT/f'content/ja/{DATE}'; cdir.mkdir(parents=True,exist_ok=True)
for a in articles:
    fm=['---',f'title: "{a["ja_title"]}"',f'slug: {a["slug"]}',f'date: {PUB}','status: publish','post_type: post','author: XNEWS編集部','lang: ja',f'excerpt: "{a["ja_summary"]}"','categories:']+[f'  - "{x}"' for x in a['cats_ja']]+['tags:']+[f'  - "{x}"' for x in a['tags_ja']]+['sources:']+[f'  - name: "{n}"\n    url: "{u}"' for n,u in a['sources']]+['---','']
    body='\n\n'.join(a['ja_body'])+'\n\n## 出典\n\n'+'\n'.join(f'- [{n}]({u})' for n,u in a['sources'])+'\n'
    (cdir/f'{a["slug"]}.md').write_text('\n'.join(fm)+body,encoding='utf-8')
links='\n'.join(f'- [{a["ja_title"]}](./{a["slug"]}.md)' for a in articles)
index='---\ntitle: "2026年8月2日 日本Xニュース日報"\nslug: 2026-08-02-daily\ndate: '+PUB+'\nstatus: publish\npost_type: post\nauthor: XNEWS編集部\nlang: ja\nexcerpt: "8月1日の日本Xで注目された話題から、気象、水資源、アイドルフェス、音楽公演、公共広報の5件を確認し、公式情報に基づいて整理した。"\ncategories:\n  - "日報"\ntags:\n  - "日本X"\n  - "2026年8月2日"\nsources: []\n---\n\n8月1日の日本Xで注目された話題から、公式発表で確認できた5件をまとめた。未確認のトレンド語や短報は掲載していない。\n\n'+links+'\n'
(cdir/'index.md').write_text(index,encoding='utf-8')
wdir=ROOT/f'wordpress/ja/{DATE}'; wdir.mkdir(parents=True,exist_ok=True)
manifest='version: 1\nlocale: ja\ntimezone: Asia/Tokyo\ncontent_dir: content/ja/'+DATE+'\npublish_at: '+PUB+'\nstatus: publish\ncomment_status: closed\nping_status: closed\nauthor: authenticated_user\nposts:\n'+''.join(f'  - {a["slug"]}.md\n' for a in articles)+'  - index.md\n'
(wdir/'wordpress.yml').write_text(manifest,encoding='utf-8')
# validation
assert len(zh)==len(ja)==5 and {x['slug'] for x in zh}=={x['slug'] for x in ja}
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in {'.js','.md','.yml','.html'} and '2026-08-02' in str(p):
        assert 'briefs' not in p.read_text(encoding='utf-8').lower()
print('generated 5 bilingual articles and WordPress edition')
