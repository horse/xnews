(() => {
const EDITIONS={
"2026-08-01":["yen-intervention","kioxia","spider-man","sore-snowman","genshin","ushijima","chika","kuramoto","tif2026","baseball","tshirt-drama","timelessman","monthly-art","mcdonalds-pokemon","idolish7-simeji","kurasushi-crab","pokemon-masters","ghana-ice","line-manga-gacha","lohaco-water","miko-8th","jurassic-world","takai-rika","premium-friday","commemorative-days","world-cup-boycott","mie-survey","tokai-kisen","roirom-honda"],
"2026-08-02":["fgo-fes-2026-day1","liella-tutorial-live-2026","acees-arena-tour-2026","sakura-miko-8th-anniversary","srw-35th-stream","nanoha-exgv-episode5","knivesout-kimetsu-collab2","ultraman-teo-episode5","onsen-shark-sequel","engei8-2026","tsugikuru-geinin-2026","kokuhaku-episode4","do-nani-aug1","venue101-aug1","sixtones-ann-aug1","tif2026-august1","bmsg-trainee-summer-stage","takarazuka-poe-clan","vnl-men-semifinal-2026","koshien-draw-2026","koshien-school-reactions-2026","baystars-aug1-win","marines-aug1-win","ohtani-redsox-aug1","chibagin-cup-2026","high-cost-medical-cap-2026","fifa-world-cup-stake-sale","yen-intervention-followup","kumamoto-disaster-response","edogawa-fireworks-2026","august2-wordplay-tags"]
};
const EDITION_SUMMARIES={
"2026-08-01":"7月31日的日本X话题从汇率与企业消息延伸到电影、电视、游戏、职业棒球、角色生日和网络文化。本期保留29篇经过核验的独立报道。",
"2026-08-02":"8月1日10时至8月2日2时，日本X的持续热点覆盖公共事务、国际体育、职业棒球、电视广播、现场演出、动漫游戏和日期型网络文化。本期按当天新增进展整理为31篇完整报道。"
};
const GROUP_RULES=[
{key:"public",title:"社会、政治、经济与公共事务",categories:["社会、政治、经济与公共事务","社会","国际","金融","日本经济","医疗","社会保障","灾害","地方活动","东京"]},
{key:"sports",title:"体育",categories:["体育","职业棒球","高中棒球","排球","足球","美国职棒"]},
{key:"entertainment",title:"影视、娱乐与大众文化",categories:["娱乐与大众文化","电视","电视剧","广播","音乐","偶像","舞台","电影","特摄"]},
{key:"anime",title:"动漫、游戏与圈层文化",categories:["动漫、游戏与圈层文化","动漫","游戏","VTuber","联动","直播"]},
{key:"commercial",title:"商业、消费与网络现象",categories:["商业、消费与网络现象","网络文化","纪念日","消费","商业"]}
];
function classifyArticle(article){
 const cats=new Set(article.categories||[]);
 for(const rule of GROUP_RULES) if(rule.categories.some(c=>cats.has(c))) return rule.key;
 return "other";
}
function arrangeEdition(articles){
 const unique=[],seen=new Set();
 for(const article of articles||[]) {
  if(!article||!article.slug||seen.has(article.slug)) continue;
  seen.add(article.slug); unique.push(article);
 }
 const focus=unique.filter(a=>a.level==="focus");
 const lead=focus[0]||unique[0]||null;
 const used=new Set(lead?[lead.slug]:[]);
 const featured=[];
 for(const article of focus.concat(unique)) {
  if(featured.length>=4) break;
  if(used.has(article.slug)) continue;
  featured.push(article); used.add(article.slug);
 }
 const groups=GROUP_RULES.map(r=>({key:r.key,title:r.title,items:[]}));
 const other={key:"other",title:"其他话题",items:[]};
 const byKey=Object.fromEntries(groups.map(g=>[g.key,g]));
 for(const article of unique) {
  if(used.has(article.slug)) continue;
  (byKey[classifyArticle(article)]||other).items.push(article); used.add(article.slug);
 }
 if(other.items.length) groups.push(other);
 return {lead,featured,groups};
}
const exported={EDITIONS,GROUP_RULES,classifyArticle,arrangeEdition};
if(typeof module!=="undefined"&&module.exports) module.exports=exported;
if(typeof window==="undefined"||typeof document==="undefined") return;

const D=window.XNEWS_META,S=D.site,RAW=window.XNEWS_ARTICLES||[];
const DATE_BY_SLUG={};Object.entries(EDITIONS).forEach(([d,slugs])=>slugs.forEach(s=>DATE_BY_SLUG[s]=d));
const active=new Set(Object.values(EDITIONS).flat());
const dedup=new Map();RAW.forEach(a=>{if(active.has(a.slug))dedup.set(a.slug,a)});
const A=[...dedup.values()],bySlug=Object.fromEntries(A.map(a=>[a.slug,a]));
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const pathForDate=d=>{const [y,m,day]=d.split("-");return `${y}/${m}/${day}`};
const labelForDate=d=>{const [y,m,day]=d.split("-").map(Number);return `${y}年${m}月${day}日`};
const pageMatch=location.pathname.match(/\/(\d{4})\/(\d{2})\/(\d{2})(?:\/|$)/);
const pageDate=document.body.dataset.editionDate||(pageMatch?`${pageMatch[1]}-${pageMatch[2]}-${pageMatch[3]}`:S.dateISO);
const editionArticles=d=>(EDITIONS[d]||[]).map(s=>bySlug[s]).filter(Boolean);
const articleURL=a=>`${S.base}/${pathForDate(DATE_BY_SLUG[a.slug]||S.dateISO)}/reports/${a.slug}.html`;
const catSlug=c=>D.categorySlugs[c]||encodeURIComponent(c);
const tagSlug=t=>D.tagSlugs[t]||encodeURIComponent(t);
const latestDate=S.dateISO;
const nav=`<nav class="nav wrap"><a href="${S.base}/">首页</a><a href="${S.base}/${pathForDate(latestDate)}/">${labelForDate(latestDate).replace(/^\d{4}年/,"")}日报</a><a href="${S.base}/${pathForDate("2026-08-01")}/">8月1日日报</a><a href="${S.base}/categories.html">分类</a><a href="${S.base}/tags.html">标签</a><a href="${S.base}/about.html">关于</a></nav>`;
const header=`<header class="masthead"><div class="wrap"><div class="brand"><a href="${S.base}/">XNEWS</a></div><div class="tagline">${esc(S.tagline)}</div></div></header>`;
const footer=`<footer class="footer"><div class="wrap">XNEWS · 报道日本X上受到集中关注、并经公开资料核实的新闻与文化现象。</div></footer>`;
const card=(a,compact=false)=>{const d=DATE_BY_SLUG[a.slug];return `<article class="story${compact?" compact":""}"><div class="story-meta">${(a.categories||[]).map(esc).join(" / ")} · ${esc(labelForDate(d))}</div><h2><a href="${articleURL(a)}">${esc(a.title)}</a></h2><p>${esc(a.summary)}</p></article>`};
const groupedSection=g=>`<section class="homepage-section"><h2 class="section-title">${esc(g.title)} <span class="archive-count">${g.items.length}</span></h2><div class="card-grid">${g.items.map(a=>card(a,true)).join("")}</div></section>`;
const app=document.getElementById("app");
function renderGrouped(date,isHome){
 const E=editionArticles(date),arranged=arrangeEdition(E);
 if(!arranged.lead){app.innerHTML=header+nav+`<main class="wrap"><h1>本期暂无报道</h1></main>`+footer;return}
 const lead=arranged.lead,groups=arranged.groups.filter(g=>g.items.length);
 const kicker=isHome?`${esc(labelForDate(date))} · 昨日新闻`:`${esc(labelForDate(date))} · 每日新闻归档`;
 app.innerHTML=header+nav+`<main class="wrap"><section class="home-lead"><div class="kicker">${kicker}</div><div class="lead-layout"><div><h1><a href="${articleURL(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p><div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${esc(labelForDate(date))}</div></div><div class="lead-side"><h2>本期日报</h2><p>${esc(EDITION_SUMMARIES[date]||"")}</p><div class="edition-stats"><span>${E.length}篇报道</span><span>${groups.length}个主题板块</span></div></div></div></section><section class="homepage-section"><h2 class="section-title">焦点报道</h2><div class="feature-grid">${arranged.featured.map(a=>card(a)).join("")}</div></section>${groups.map(groupedSection).join("")}<section class="homepage-section"><h2 class="section-title">继续浏览</h2><div class="link-panels"><a href="${S.base}/categories.html">新闻分类</a><a href="${S.base}/tags.html">新闻标签</a>${isHome?`<a href="${S.base}/${pathForDate(date)}/">当日完整归档</a>`:`<a href="${S.base}/">返回最新日报</a>`}</div></section></main>`+footer;
}
function renderHome(){renderGrouped(latestDate,true)}
function renderEdition(){renderGrouped(pageDate,false)}
function renderArticle(){
 const a=bySlug[document.body.dataset.slug];if(!a){app.innerHTML=header+nav+`<main class="article"><h1>文章不存在或已撤下</h1></main>`+footer;return}
 const d=DATE_BY_SLUG[a.slug],catLinks=(a.categories||[]).map(c=>`<a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a>`).join("、");
 const tagLinks=(a.tags||[]).map(t=>`<a class="tag" href="${S.base}/tags.html#${tagSlug(t)}">${esc(t)}</a>`).join("");
 app.innerHTML=header+nav+`<main class="article"><div class="breadcrumb"><a href="${S.base}/">首页</a><span>›</span><a href="${S.base}/${pathForDate(d)}/">${esc(labelForDate(d))}</a><span>›</span><span>${esc(a.title)}</span></div><div class="post-categories">${catLinks}</div><h1>${esc(a.title)}</h1><p class="dek">${esc(a.summary)}</p><div class="post-meta"><time datetime="${esc(d)}">${esc(labelForDate(d))}</time><span>作者：XNEWS编辑部</span></div>${(a.body||[]).map(p=>`<p>${esc(p)}</p>`).join("")}<div class="source-note"><strong>来源：</strong>${(a.sources||[]).map(([n,u])=>`<a href="${esc(u)}">${esc(n)}</a>`).join(" · ")}</div><section class="post-taxonomy"><div><strong>分类</strong><span>${catLinks}</span></div><div><strong>标签</strong><div class="tag-list">${tagLinks}</div></div></section><a class="back" href="${S.base}/${pathForDate(d)}/">← 返回当日新闻</a></main>`+footer;
}
function renderCategories(){
 const map={};A.forEach(a=>(a.categories||[]).forEach(c=>(map[c]??=[]).push(a)));
 const cats=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">分类归档</div><h1>新闻分类</h1><p class="lead">按领域浏览全部日期的完整报道。</p></section>${cats.map(c=>`<section class="archive-section" id="${catSlug(c)}"><h2>${esc(c)} <span class="archive-count">${map[c].length}</span></h2><ul class="archive-list">${map[c].sort((a,b)=>DATE_BY_SLUG[b.slug].localeCompare(DATE_BY_SLUG[a.slug])).map(a=>`<li><time>${esc(labelForDate(DATE_BY_SLUG[a.slug]))}</time><a href="${articleURL(a)}">${esc(a.title)}</a></li>`).join("")}</ul></section>`).join("")}</main>`+footer;
}
function renderTags(){
 const map={};A.forEach(a=>(a.tags||[]).forEach(t=>(map[t]??=[]).push(a)));
 const tags=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">标签归档</div><h1>新闻标签</h1><p class="lead">标签记录人物、机构、作品、地点和议题。</p></section><div class="tag-cloud tag-cloud-large">${tags.map(t=>`<a id="${tagSlug(t)}" class="tag tag-index-link" href="${articleURL(map[t].sort((a,b)=>DATE_BY_SLUG[b.slug].localeCompare(DATE_BY_SLUG[a.slug]))[0])}">${esc(t)}${map[t].length>1?`（${map[t].length}篇）`:""}</a>`).join("")}</div></main>`+footer;
}
({home:renderHome,edition:renderEdition,article:renderArticle,categories:renderCategories,tags:renderTags}[document.body.dataset.page]||renderHome)();
})();
