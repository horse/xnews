(() => {
const EDITIONS={
"2026-08-01":["yen-intervention","kioxia","spider-man","sore-snowman","genshin","ushijima","chika","kuramoto","tif2026","baseball","tshirt-drama","timelessman","monthly-art","mcdonalds-pokemon","idolish7-simeji","kurasushi-crab","pokemon-masters","ghana-ice","line-manga-gacha","lohaco-water","miko-8th","jurassic-world","takai-rika","premium-friday","commemorative-days","world-cup-boycott","mie-survey","tokai-kisen","roirom-honda"],
"2026-08-02":["fgo-fes-2026-day1","engei8-2026","sakura-miko-8th-anniversary","vnl-men-semifinal-2026","koshien-draw-2026","srw-35th-stream","liella-tutorial-live-2026","tif2026-august1"]
};
const EDITION_SUMMARIES={
"2026-08-01":"7月31日的日本X话题从汇率与企业消息延伸到电影、电视、游戏、职业棒球、角色生日和网络文化。本期保留29篇经过核验的独立报道，不再发布趋势简讯。",
"2026-08-02":"8月1日的日本X话题由大型游戏周年活动、长时间电视直播、VTuber周年、国际排球、高中棒球抽签、动漫音乐活动和偶像节共同推动。本期只收录能够由官方资料核验并可独立成文的事件。"
};
const GROUP_RULES=[
{key:"sports",title:"体育",categories:["体育","职业棒球","棒球","排球","足球"]},
{key:"anime",title:"动漫、游戏与圈层文化",categories:["动漫","游戏","漫画","VTuber","二次元","平台"]},
{key:"entertainment",title:"影视、娱乐与大众文化",categories:["电视","电影","音乐","偶像","日剧","艺能","文化"]},
{key:"commercial",title:"商业、消费与网络现象",categories:["商业","科技","消费","食品","纪念日","网络文化","网络","生活"]},
{key:"public",title:"社会、政治、经济与公共事务",categories:["社会","政治","国际","金融","日本经济","经济","地方文化","调查","交通","公共事务"]}
];
function classifyArticle(article){
 const categories=new Set(article.categories||[]);
 for(const rule of GROUP_RULES){
  if(rule.categories.some(category=>categories.has(category))) return rule.key;
 }
 return "other";
}
function arrangeEdition(articles){
 const unique=[];
 const seen=new Set();
 for(const article of articles||[]){
  if(!article||!article.slug||seen.has(article.slug)) continue;
  seen.add(article.slug);
  unique.push(article);
 }
 const focus=unique.filter(article=>article.level==="focus");
 const lead=focus[0]||unique[0]||null;
 const used=new Set(lead?[lead.slug]:[]);
 const featured=[];
 for(const article of focus.concat(unique)){
  if(featured.length>=4) break;
  if(used.has(article.slug)) continue;
  featured.push(article);
  used.add(article.slug);
 }
 const groups=GROUP_RULES.map(rule=>({key:rule.key,title:rule.title,items:[]}));
 const other={key:"other",title:"其他话题",items:[]};
 const groupByKey=Object.fromEntries(groups.map(group=>[group.key,group]));
 for(const article of unique){
  if(used.has(article.slug)) continue;
  const key=classifyArticle(article);
  (groupByKey[key]||other).items.push(article);
  used.add(article.slug);
 }
 if(other.items.length) groups.push(other);
 return {lead,featured,groups};
}
const exported={EDITIONS,GROUP_RULES,classifyArticle,arrangeEdition};
if(typeof module!=="undefined"&&module.exports) module.exports=exported;
if(typeof window==="undefined"||typeof document==="undefined") return;

const D=window.XNEWS_META,S=D.site,RAW=window.XNEWS_ARTICLES||[];
const DATE_BY_SLUG={};Object.entries(EDITIONS).forEach(([date,slugs])=>slugs.forEach(slug=>DATE_BY_SLUG[slug]=date));
const active=new Set(Object.values(EDITIONS).flat());
const dedup=new Map();RAW.forEach(article=>{if(active.has(article.slug))dedup.set(article.slug,article)});
const A=[...dedup.values()],bySlug=Object.fromEntries(A.map(article=>[article.slug,article]));
const esc=value=>String(value??"").replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
const pathForDate=date=>{const [year,month,day]=date.split("-");return `${year}/${month}/${day}`};
const labelForDate=date=>{const [year,month,day]=date.split("-").map(Number);return `${year}年${month}月${day}日`};
const pageMatch=location.pathname.match(/\/(\d{4})\/(\d{2})\/(\d{2})(?:\/|$)/);
const pageDate=document.body.dataset.editionDate||(pageMatch?`${pageMatch[1]}-${pageMatch[2]}-${pageMatch[3]}`:S.dateISO);
const editionArticles=date=>(EDITIONS[date]||[]).map(slug=>bySlug[slug]).filter(Boolean);
const articleURL=article=>`${S.base}/${pathForDate(DATE_BY_SLUG[article.slug]||S.dateISO)}/reports/${article.slug}.html`;
const catSlug=category=>D.categorySlugs[category]||encodeURIComponent(category);
const tagSlug=tag=>D.tagSlugs[tag]||encodeURIComponent(tag);
const latestDate=S.dateISO;
const nav=`<nav class="nav wrap"><a href="${S.base}/">首页</a><a href="${S.base}/${pathForDate(latestDate)}/">${labelForDate(latestDate).replace(/^\d{4}年/,"")}日报</a><a href="${S.base}/${pathForDate("2026-08-01")}/">8月1日日报</a><a href="${S.base}/categories.html">分类</a><a href="${S.base}/tags.html">标签</a><a href="${S.base}/about.html">关于</a></nav>`;
const header=`<header class="masthead"><div class="wrap"><div class="brand"><a href="${S.base}/">XNEWS</a></div><div class="tagline">${esc(S.tagline)}</div></div></header>`;
const footer=`<footer class="footer"><div class="wrap">XNEWS · 报道日本X上受到集中关注、并经公开资料核实的新闻与文化现象。</div></footer>`;
const card=(article,compact=false)=>{const date=DATE_BY_SLUG[article.slug];return `<article class="story${compact?" compact":""}"><div class="story-meta">${article.categories.map(esc).join(" / ")} · ${esc(labelForDate(date))}</div><h2><a href="${articleURL(article)}">${esc(article.title)}</a></h2><p>${esc(article.summary)}</p></article>`};
const groupedSection=group=>`<section class="homepage-section"><h2 class="section-title">${esc(group.title)} <span class="archive-count">${group.items.length}</span></h2><div class="card-grid">${group.items.map(article=>card(article,true)).join("")}</div></section>`;
const app=document.getElementById("app");
function renderHome(){
 const edition=editionArticles(latestDate),focus=edition.filter(article=>article.level==="focus"),standard=edition.filter(article=>article.level==="standard"),lead=focus[0]||edition[0];
 if(!lead){app.innerHTML=header+nav+`<main class="wrap"><h1>暂无日报</h1></main>`+footer;return}
 app.innerHTML=header+nav+`<main class="wrap"><section class="home-lead"><div class="kicker">${esc(labelForDate(latestDate))} · 昨日新闻</div><div class="lead-layout"><div><h1><a href="${articleURL(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p><div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${esc(labelForDate(latestDate))}</div></div><div class="lead-side"><h2>本期日报</h2><p>${edition.length}篇独立报道。所有文章均保留完整导语、正文与核验来源。</p><a class="button-link" href="${S.base}/${pathForDate(latestDate)}/">阅读完整日报</a></div></div></section><section class="homepage-section"><h2 class="section-title">焦点报道</h2><div class="feature-grid">${focus.slice(1).map(article=>card(article)).join("")}</div></section><section class="homepage-section"><h2 class="section-title">更多新闻</h2><div class="card-grid">${standard.map(article=>card(article,true)).join("")}</div></section></main>`+footer;
}
function renderEdition(){
 const edition=editionArticles(pageDate);
 const arranged=arrangeEdition(edition);
 if(!arranged.lead){app.innerHTML=header+nav+`<main class="wrap"><h1>本期暂无报道</h1></main>`+footer;return}
 const nonEmptyGroups=arranged.groups.filter(group=>group.items.length);
 const lead=arranged.lead;
 app.innerHTML=header+nav+`<main class="wrap"><section class="home-lead"><div class="kicker">${esc(labelForDate(pageDate))} · 每日新闻归档</div><div class="lead-layout"><div><h1><a href="${articleURL(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p><div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${esc(labelForDate(pageDate))}</div></div><div class="lead-side"><h2>本期日报</h2><p>${esc(EDITION_SUMMARIES[pageDate]||"")}</p><div class="edition-stats"><span>${edition.length}篇报道</span><span>${nonEmptyGroups.length}个主题板块</span></div></div></div></section><section class="homepage-section"><h2 class="section-title">焦点报道</h2><div class="feature-grid">${arranged.featured.map(article=>card(article)).join("")}</div></section>${nonEmptyGroups.map(groupedSection).join("")}<section class="homepage-section"><h2 class="section-title">继续浏览</h2><div class="link-panels"><a href="${S.base}/categories.html">新闻分类</a><a href="${S.base}/tags.html">新闻标签</a><a href="${S.base}/">返回最新日报</a></div></section></main>`+footer;
}
function renderArticle(){
 const article=bySlug[document.body.dataset.slug];if(!article){app.innerHTML=header+nav+`<main class="article"><h1>文章不存在或已撤下</h1></main>`+footer;return}
 const date=DATE_BY_SLUG[article.slug],catLinks=article.categories.map(category=>`<a href="${S.base}/categories.html#${catSlug(category)}">${esc(category)}</a>`).join("、");
 const tagLinks=article.tags.map(tag=>`<a class="tag" href="${S.base}/tags.html#${tagSlug(tag)}">${esc(tag)}</a>`).join("");
 app.innerHTML=header+nav+`<main class="article"><div class="breadcrumb"><a href="${S.base}/">首页</a><span>›</span><a href="${S.base}/${pathForDate(date)}/">${esc(labelForDate(date))}</a><span>›</span><span>${esc(article.title)}</span></div><div class="post-categories">${catLinks}</div><h1>${esc(article.title)}</h1><p class="dek">${esc(article.summary)}</p><div class="post-meta"><time datetime="${esc(date)}">${esc(labelForDate(date))}</time><span>作者：XNEWS编辑部</span></div>${article.body.map(paragraph=>`<p>${esc(paragraph)}</p>`).join("")}<div class="source-note"><strong>来源：</strong>${article.sources.map(([name,url])=>`<a href="${esc(url)}">${esc(name)}</a>`).join(" · ")}</div><section class="post-taxonomy"><div><strong>分类</strong><span>${catLinks}</span></div><div><strong>标签</strong><div class="tag-list">${tagLinks}</div></div></section><a class="back" href="${S.base}/${pathForDate(date)}/">← 返回当日新闻</a></main>`+footer;
}
function renderCategories(){const map={};A.forEach(article=>article.categories.forEach(category=>(map[category]??=[]).push(article)));const categories=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">分类归档</div><h1>新闻分类</h1></section>${categories.map(category=>`<section class="archive-section" id="${catSlug(category)}"><h2>${esc(category)} <span class="archive-count">${map[category].length}</span></h2><ul class="archive-list">${map[category].sort((a,b)=>DATE_BY_SLUG[b.slug].localeCompare(DATE_BY_SLUG[a.slug])).map(article=>`<li><time>${esc(labelForDate(DATE_BY_SLUG[article.slug]))}</time><a href="${articleURL(article)}">${esc(article.title)}</a></li>`).join("")}</ul></section>`).join("")}</main>`+footer}
function renderTags(){const map={};A.forEach(article=>article.tags.forEach(tag=>(map[tag]??=[]).push(article)));const tags=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">标签归档</div><h1>新闻标签</h1></section><div class="tag-cloud tag-cloud-large">${tags.map(tag=>`<a id="${tagSlug(tag)}" class="tag tag-index-link" href="${articleURL(map[tag].sort((a,b)=>DATE_BY_SLUG[b.slug].localeCompare(DATE_BY_SLUG[a.slug]))[0])}">${esc(tag)}${map[tag].length>1?`（${map[tag].length}篇）`:""}</a>`).join("")}</div></main>`+footer}
({home:renderHome,edition:renderEdition,article:renderArticle,categories:renderCategories,tags:renderTags}[document.body.dataset.page]||renderHome)();
})();
