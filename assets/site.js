(() => {
const D=window.XNEWS_META,S=D.site,RAW=window.XNEWS_ARTICLES||[];
const EDITIONS={
"2026-08-01":["yen-intervention", "kioxia", "spider-man", "sore-snowman", "genshin", "ushijima", "chika", "kuramoto", "tif2026", "baseball", "tshirt-drama", "timelessman", "monthly-art", "mcdonalds-pokemon", "idolish7-simeji", "kurasushi-crab", "pokemon-masters", "ghana-ice", "line-manga-gacha", "lohaco-water", "miko-8th", "jurassic-world", "takai-rika", "premium-friday", "commemorative-days", "world-cup-boycott", "mie-survey", "tokai-kisen", "roirom-honda"],
"2026-08-02":["fgo-fes-2026-day1", "engei8-2026", "sakura-miko-8th-anniversary", "vnl-men-semifinal-2026", "koshien-draw-2026", "srw-35th-stream", "liella-tutorial-live-2026", "tif2026-august1"]
};
const EDITION_SUMMARIES={
"2026-08-01":"7月31日的日本X话题从汇率与企业消息延伸到电影、电视、游戏、职业棒球、角色生日和网络文化。本期保留29篇经过核验的独立报道，不再发布趋势简讯。",
"2026-08-02":"8月1日的日本X话题由大型游戏周年活动、长时间电视直播、VTuber周年、国际排球、高中棒球抽签、动漫音乐活动和偶像节共同推动。本期只收录能够由官方资料核验并可独立成文的事件。"
};
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
const card=(a,compact=false)=>{const d=DATE_BY_SLUG[a.slug];return `<article class="story${compact?" compact":""}"><div class="story-meta">${a.categories.map(esc).join(" / ")} · ${esc(labelForDate(d))}</div><h2><a href="${articleURL(a)}">${esc(a.title)}</a></h2><p>${esc(a.summary)}</p></article>`};
const app=document.getElementById("app");
function renderHome(){
 const E=editionArticles(latestDate),focus=E.filter(a=>a.level==="focus"),standard=E.filter(a=>a.level==="standard"),lead=focus[0]||E[0];
 if(!lead){app.innerHTML=header+nav+`<main class="wrap"><h1>暂无日报</h1></main>`+footer;return}
 app.innerHTML=header+nav+`<main class="wrap"><section class="home-lead"><div class="kicker">${esc(labelForDate(latestDate))} · 昨日新闻</div><div class="lead-layout"><div><h1><a href="${articleURL(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p><div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${esc(labelForDate(latestDate))}</div></div><div class="lead-side"><h2>本期日报</h2><p>${E.length}篇独立报道。所有文章均保留完整导语、正文与核验来源。</p><a class="button-link" href="${S.base}/${pathForDate(latestDate)}/">阅读完整日报</a></div></div></section><section class="homepage-section"><h2 class="section-title">焦点报道</h2><div class="feature-grid">${focus.slice(1).map(a=>card(a)).join("")}</div></section><section class="homepage-section"><h2 class="section-title">更多新闻</h2><div class="card-grid">${standard.map(a=>card(a,true)).join("")}</div></section></main>`+footer;
}
function renderEdition(){
 const E=editionArticles(pageDate),focus=E.filter(a=>a.level==="focus"),standard=E.filter(a=>a.level==="standard");
 const cats=[...new Set(E.flatMap(a=>a.categories))].sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero edition-hero"><div class="kicker">每日新闻归档</div><h1>${esc(labelForDate(pageDate))} 日本X热门新闻日报</h1><p class="lead">${esc(EDITION_SUMMARIES[pageDate]||"")}</p><div class="edition-stats"><span>${E.length}篇报道</span><span>${focus.length}篇焦点</span><span>${standard.length}篇其他新闻</span></div></section><div class="edition-layout"><section><h2 class="section-title">焦点报道</h2>${focus.map(a=>card(a)).join("")}<h2 class="section-title">更多新闻</h2><div class="card-grid">${standard.map(a=>card(a,true)).join("")}</div></section><aside class="side sticky-side"><h3>本期分类</h3><ul class="plain-list">${cats.map(c=>`<li><a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a></li>`).join("")}</ul><h3>日期</h3><p class="meta">${esc(labelForDate(pageDate))}</p></aside></div></main>`+footer;
}
function renderArticle(){
 const a=bySlug[document.body.dataset.slug];if(!a){app.innerHTML=header+nav+`<main class="article"><h1>文章不存在或已撤下</h1></main>`+footer;return}
 const d=DATE_BY_SLUG[a.slug],catLinks=a.categories.map(c=>`<a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a>`).join("、");
 const tagLinks=a.tags.map(t=>`<a class="tag" href="${S.base}/tags.html#${tagSlug(t)}">${esc(t)}</a>`).join("");
 app.innerHTML=header+nav+`<main class="article"><div class="breadcrumb"><a href="${S.base}/">首页</a><span>›</span><a href="${S.base}/${pathForDate(d)}/">${esc(labelForDate(d))}</a><span>›</span><span>${esc(a.title)}</span></div><div class="post-categories">${catLinks}</div><h1>${esc(a.title)}</h1><p class="dek">${esc(a.summary)}</p><div class="post-meta"><time datetime="${esc(d)}">${esc(labelForDate(d))}</time><span>作者：XNEWS编辑部</span></div>${a.body.map(p=>`<p>${esc(p)}</p>`).join("")}<div class="source-note"><strong>来源：</strong>${a.sources.map(([n,u])=>`<a href="${esc(u)}">${esc(n)}</a>`).join(" · ")}</div><section class="post-taxonomy"><div><strong>分类</strong><span>${catLinks}</span></div><div><strong>标签</strong><div class="tag-list">${tagLinks}</div></div></section><a class="back" href="${S.base}/${pathForDate(d)}/">← 返回当日新闻</a></main>`+footer;
}
function renderCategories(){const map={};A.forEach(a=>a.categories.forEach(c=>(map[c]??=[]).push(a)));const cats=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">分类归档</div><h1>新闻分类</h1></section>${cats.map(c=>`<section class="archive-section" id="${catSlug(c)}"><h2>${esc(c)} <span class="archive-count">${map[c].length}</span></h2><ul class="archive-list">${map[c].sort((a,b)=>DATE_BY_SLUG[b.slug].localeCompare(DATE_BY_SLUG[a.slug])).map(a=>`<li><time>${esc(labelForDate(DATE_BY_SLUG[a.slug]))}</time><a href="${articleURL(a)}">${esc(a.title)}</a></li>`).join("")}</ul></section>`).join("")}</main>`+footer}
function renderTags(){const map={};A.forEach(a=>a.tags.forEach(t=>(map[t]??=[]).push(a)));const tags=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">标签归档</div><h1>新闻标签</h1></section><div class="tag-cloud tag-cloud-large">${tags.map(t=>`<a id="${tagSlug(t)}" class="tag tag-index-link" href="${articleURL(map[t].sort((a,b)=>DATE_BY_SLUG[b.slug].localeCompare(DATE_BY_SLUG[a.slug]))[0])}">${esc(t)}${map[t].length>1?`（${map[t].length}篇）`:""}</a>`).join("")}</div></main>`+footer}
({home:renderHome,edition:renderEdition,article:renderArticle,categories:renderCategories,tags:renderTags}[document.body.dataset.page]||renderHome)();
})();