(() => {
const D=window.XNEWS_META,S=D.site,A=window.XNEWS_ARTICLES||[];
const bySlug=Object.fromEntries(A.map(a=>[a.slug,a]));
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const articleURL=a=>`${S.base}/2026/08/02/reports/${a.slug}.html`;
const catSlug=c=>D.categorySlugs[c]||encodeURIComponent(c);
const tagSlug=t=>D.tagSlugs[t]||encodeURIComponent(t);
const nav=`<nav class="nav wrap"><a href="${S.base}/">首页</a><a href="${S.base}/2026/08/02/">8月2日日报</a><a href="${S.base}/categories.html">分类</a><a href="${S.base}/tags.html">标签</a><a href="${S.base}/about.html">关于</a></nav>`;
const header=`<header class="masthead"><div class="wrap"><div class="brand"><a href="${S.base}/">XNEWS</a></div><div class="tagline">${esc(S.tagline)}</div></div></header>`;
const footer=`<footer class="footer"><div class="wrap">XNEWS · 报道日本X上受到集中关注的新闻与文化现象。</div></footer>`;
const card=(a,compact=false)=>`<article class="story${compact?" compact":""}"><div class="story-meta">${a.categories.map(esc).join(" / ")} · ${esc(S.date)}</div><h2><a href="${articleURL(a)}">${esc(a.title)}</a></h2><p>${esc(a.summary)}</p></article>`;
const app=document.getElementById("app");
function renderHome(){
 const focus=A.filter(a=>a.level==="focus"),standard=A.filter(a=>a.level==="standard"),lead=focus[0]||A[0];
 app.innerHTML=header+nav+`<main class="wrap"><section class="home-lead"><div class="kicker">${esc(S.date)} · 昨日新闻</div><div class="lead-layout"><div><h1><a href="${articleURL(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p><div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${esc(S.date)}</div></div><div class="lead-side"><h2>本期日报</h2><p>${A.length}篇独立报道，覆盖天气与防灾、水资源、文化活动、音乐和公共传播。</p><a class="button-link" href="${S.base}/2026/08/02/">阅读完整日报</a></div></div></section><section class="homepage-section"><h2 class="section-title">焦点报道</h2><div class="feature-grid">${focus.slice(1).map(a=>card(a)).join("")}</div></section><section class="homepage-section"><h2 class="section-title">更多新闻</h2><div class="card-grid">${standard.map(a=>card(a,true)).join("")}</div></section></main>`+footer;
}
function renderEdition(){
 const focus=A.filter(a=>a.level==="focus"),standard=A.filter(a=>a.level==="standard");
 const cats=[...new Set(A.flatMap(a=>a.categories))].sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero edition-hero"><div class="kicker">每日新闻归档</div><h1>${esc(S.date)} 日本X热门新闻日报</h1><p class="lead">8月1日的日本X话题中，能够由官方资料核实的重点集中在高温少雨、水资源、台场偶像节、名古屋大型演出和警视厅公共传播活动。本期只收录可独立成文的事件，不发布未确认趋势词或短报。</p><div class="edition-stats"><span>${A.length}篇报道</span><span>${focus.length}篇焦点</span><span>${standard.length}篇其他新闻</span></div></section><div class="edition-layout"><section><h2 class="section-title">焦点报道</h2>${focus.map(a=>card(a)).join("")}<h2 class="section-title">更多新闻</h2><div class="card-grid">${standard.map(a=>card(a,true)).join("")}</div></section><aside class="side sticky-side"><h3>本期分类</h3><ul class="plain-list">${cats.map(c=>`<li><a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a></li>`).join("")}</ul><h3>日期</h3><p class="meta">${esc(S.date)}</p></aside></div></main>`+footer;
}
function renderArticle(){
 const a=bySlug[document.body.dataset.slug];if(!a){app.innerHTML=header+nav+`<main class="article"><h1>文章不存在</h1></main>`+footer;return;}
 const catLinks=a.categories.map(c=>`<a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a>`).join("、");
 const tagLinks=a.tags.map(t=>`<a class="tag" href="${S.base}/tags.html#${tagSlug(t)}">${esc(t)}</a>`).join("");
 app.innerHTML=header+nav+`<main class="article"><div class="breadcrumb"><a href="${S.base}/">首页</a><span>›</span><a href="${S.base}/2026/08/02/">${esc(S.date)}</a><span>›</span><span>${esc(a.title)}</span></div><div class="post-categories">${catLinks}</div><h1>${esc(a.title)}</h1><p class="dek">${esc(a.summary)}</p><div class="post-meta"><time datetime="${esc(S.published)}">${esc(S.date)}</time><span>作者：XNEWS编辑部</span></div>${a.body.map(p=>`<p>${esc(p)}</p>`).join("")}<div class="source-note"><strong>来源：</strong>${a.sources.map(([n,u])=>`<a href="${esc(u)}">${esc(n)}</a>`).join(" · ")}</div><section class="post-taxonomy"><div><strong>分类</strong><span>${catLinks}</span></div><div><strong>标签</strong><div class="tag-list">${tagLinks}</div></div></section><a class="back" href="${S.base}/2026/08/02/">← 返回当日新闻</a></main>`+footer;
}
function renderCategories(){const map={};A.forEach(a=>a.categories.forEach(c=>(map[c]??=[]).push(a)));const cats=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">分类归档</div><h1>新闻分类</h1></section>${cats.map(c=>`<section class="archive-section" id="${catSlug(c)}"><h2>${esc(c)} <span class="archive-count">${map[c].length}</span></h2><ul class="archive-list">${map[c].map(a=>`<li><time>${esc(S.date)}</time><a href="${articleURL(a)}">${esc(a.title)}</a></li>`).join("")}</ul></section>`).join("")}</main>`+footer;}
function renderTags(){const map={};A.forEach(a=>a.tags.forEach(t=>(map[t]??=[]).push(a)));const tags=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">标签归档</div><h1>新闻标签</h1></section><div class="tag-cloud tag-cloud-large">${tags.map(t=>`<a id="${tagSlug(t)}" class="tag tag-index-link" href="${articleURL(map[t][0])}">${esc(t)}${map[t].length>1?`（${map[t].length}篇）`:""}</a>`).join("")}</div></main>`+footer;}
({home:renderHome,edition:renderEdition,article:renderArticle,categories:renderCategories,tags:renderTags}[document.body.dataset.page]||renderHome)();
})();