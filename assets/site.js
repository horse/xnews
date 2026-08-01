(() => {
const D=window.XNEWS_META, S=D.site, A=window.XNEWS_ARTICLES||[], B=D.briefs;
const bySlug=Object.fromEntries(A.map(a=>[a.slug,a]));
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const nav=`<nav class="nav wrap"><a href="${S.base}/">首页</a><a href="${S.base}/2026/08/01/">8月1日日报</a><a href="${S.base}/categories.html">分类</a><a href="${S.base}/tags.html">标签</a><a href="${S.base}/about.html">关于</a></nav>`;
const header=`<header class="masthead"><div class="wrap"><div class="brand"><a href="${S.base}/">XNEWS</a></div><div class="tagline">${esc(S.tagline)}</div></div></header>`;
const footer=`<footer class="footer"><div class="wrap">XNEWS · 报道日本 X 上受到集中关注的新闻与文化现象。</div></footer>`;
const articleURL=a=>`${S.base}/2026/08/01/reports/${a.slug}.html`;
const catSlug=c=>D.categorySlugs[c];
const tagSlug=t=>D.tagSlugs[t];
const catLinks=a=>a.categories.map(c=>`<a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a>`).join("、");
const tagLinks=a=>a.tags.map(t=>`<a class="tag" href="${S.base}/tags.html#${tagSlug(t)}">${esc(t)}</a>`).join("");
const card=(a,compact=false)=>`<article class="story${compact?" compact":""}"><div class="story-meta">${a.categories.map(esc).join(" / ")} · ${esc(S.date)}</div><h2><a href="${articleURL(a)}">${esc(a.title)}</a></h2><p>${esc(a.summary)}</p></article>`;
const section=(title,items)=>`<section class="homepage-section"><h2 class="section-title">${esc(title)}</h2><div class="card-grid">${items.map(a=>card(a,true)).join("")}</div></section>`;
const app=document.getElementById("app");
function renderHome(){
 const focus=A.filter(a=>a.level==="focus"), standard=A.filter(a=>a.level==="standard"), lead=focus[0];
 const groups=[
  ["国际与经济",["yen-intervention","kioxia","world-cup-boycott","mie-survey"]],
  ["影视与娱乐",["spider-man","sore-snowman","tshirt-drama","timelessman","jurassic-world"]],
  ["游戏与动漫",["genshin","chika","kuramoto","pokemon-masters","idolish7-simeji"]],
  ["社会与消费",["tokai-kisen","mcdonalds-pokemon","kurasushi-crab","premium-friday"]]
 ];
 app.innerHTML=header+nav+`<main class="wrap">
 <section class="home-lead"><div class="kicker">${esc(S.date)} · 昨日新闻</div><div class="lead-layout"><div>
 <h1><a href="${articleURL(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p>
 <div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${esc(S.date)}</div></div>
 <div class="lead-side"><h2>本期日报</h2><p>${A.length}篇独立报道与${B.length}条简讯，覆盖金融、科技、影视、游戏、体育、消费与网络文化。</p>
 <a class="button-link" href="${S.base}/2026/08/01/">阅读完整日报</a></div></div></section>
 <section class="homepage-section"><h2 class="section-title">焦点报道</h2><div class="feature-grid">${focus.slice(1,5).map(a=>card(a)).join("")}</div></section>
 <section class="homepage-section"><h2 class="section-title">最新报道</h2><div class="card-grid">${focus.slice(5).concat(standard.slice(0,5)).map(a=>card(a,true)).join("")}</div></section>
 ${groups.map(([t,slugs])=>section(t,slugs.map(s=>bySlug[s]))).join("")}
 <section class="homepage-section"><h2 class="section-title">更多内容</h2><div class="link-panels">
 <a href="${S.base}/2026/08/01/">8月1日完整日报</a><a href="${S.base}/2026/08/01/briefs.html">趋势简讯</a>
 <a href="${S.base}/categories.html">新闻分类</a><a href="${S.base}/tags.html">新闻标签</a></div></section>
 </main>`+footer;
}
function renderEdition(){
 const focus=A.filter(a=>a.level==="focus"), standard=A.filter(a=>a.level==="standard");
 const cats=[...new Set(A.flatMap(a=>a.categories))].sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero edition-hero"><div class="kicker">每日新闻归档</div>
 <h1>${esc(S.date)} 日本X热门新闻日报</h1><p class="lead">7月31日的日本X热点从白天的汇率与企业消息，转向晚间的电视、电影、游戏和职业棒球，零点后又由角色生日、偶像与网络文化接续。以下日报将能够核实的事件整理为独立新闻，并把较分散的话题集中列入简讯。</p>
 <div class="edition-stats"><span>${A.length}篇报道</span><span>${focus.length}篇焦点</span><span>${standard.length}篇其他新闻</span><span>${B.length}条简讯</span></div></section>
 <div class="edition-layout"><section><h2 class="section-title">焦点报道</h2>${focus.map(a=>card(a)).join("")}
 <h2 class="section-title">更多新闻</h2><div class="card-grid">${standard.map(a=>card(a,true)).join("")}</div>
 <h2 class="section-title">趋势简讯</h2><article class="story"><h2><a href="${S.base}/2026/08/01/briefs.html">${B.length}条趋势简讯</a></h2>
 <p>汇集当天受到关注、但适合以短篇形式记录的作品、人名、活动和社群话题。</p></article></section>
 <aside class="side sticky-side"><h3>本期分类</h3><ul class="plain-list">${cats.map(c=>`<li><a href="${S.base}/categories.html#${catSlug(c)}">${esc(c)}</a></li>`).join("")}</ul>
 <h3>日期</h3><p class="meta">${esc(S.date)}</p><h3>归档</h3><p class="meta"><a href="${S.base}/categories.html">按分类浏览</a><br><a href="${S.base}/tags.html">按标签浏览</a></p></aside></div></main>`+footer;
}
function renderArticle(){
 const a=bySlug[document.body.dataset.slug]; if(!a){app.innerHTML=header+nav+`<main class="article"><h1>文章不存在</h1></main>`+footer;return;}
 const schema={"@context":"https://schema.org","@type":"NewsArticle","headline":a.title,"description":a.summary,"datePublished":S.published,
 "dateModified":S.modified,"mainEntityOfPage":location.href,"url":location.href,"inLanguage":"zh-CN","articleSection":a.categories,
 "keywords":a.tags,"identifier":a.slug,"author":{"@type":"Organization","name":"XNEWS编辑部"},"publisher":{"@type":"Organization","name":"XNEWS","url":"https://horse.github.io/xnews/"}};
 const ld=document.createElement("script");ld.type="application/ld+json";ld.textContent=JSON.stringify(schema);document.head.appendChild(ld);
 app.innerHTML=header+nav+`<main class="article"><div class="breadcrumb"><a href="${S.base}/">首页</a><span>›</span><a href="${S.base}/2026/08/01/">${esc(S.date)}</a><span>›</span><span>${esc(a.title)}</span></div>
 <div class="post-categories">${catLinks(a)}</div><h1>${esc(a.title)}</h1><p class="dek">${esc(a.summary)}</p>
 <div class="post-meta"><time datetime="${esc(S.published)}">${esc(S.date)}</time><span>作者：XNEWS编辑部</span></div>
 ${a.body.map(p=>`<p>${esc(p)}</p>`).join("")}
 <div class="source-note"><strong>来源：</strong>${a.sources.map(([n,u])=>`<a href="${esc(u)}">${esc(n)}</a>`).join(" · ")}</div>
 <section class="post-taxonomy"><div><strong>分类</strong><span>${catLinks(a)}</span></div><div><strong>标签</strong><div class="tag-list">${tagLinks(a)}</div></div></section>
 <a class="back" href="${S.base}/2026/08/01/">← 返回当日新闻</a></main>`+footer;
}
function renderBriefs(){
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">趋势简讯</div><h1>${esc(S.date)} 简讯</h1>
 <p class="lead">以下内容记录当天集中出现的人物、作品、活动与社群话题。</p></section>
 <section class="brief-list">${B.map(b=>`<article class="brief"><h2>${esc(b.title)}</h2><p>${esc(b.text)}</p></article>`).join("")}</section>
 <a class="back" href="${S.base}/2026/08/01/">← 返回当日日报</a></main>`+footer;
}
function renderCategories(){
 const map={};A.forEach(a=>a.categories.forEach(c=>(map[c]??=[]).push(a)));
 const cats=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">分类归档</div><h1>新闻分类</h1>
 <p class="lead">按领域浏览XNEWS报道；一篇新闻可以同时属于多个分类。</p></section>
 <div class="archive-nav">${cats.map(c=>`<a href="#${catSlug(c)}">${esc(c)} <span>${map[c].length}</span></a>`).join("")}</div>
 ${cats.map(c=>`<section class="archive-section" id="${catSlug(c)}"><h2>${esc(c)} <span class="archive-count">${map[c].length}</span></h2>
 <ul class="archive-list">${map[c].map(a=>`<li><time>${esc(S.date)}</time><a href="${articleURL(a)}">${esc(a.title)}</a></li>`).join("")}</ul></section>`).join("")}
 </main>`+footer;
}
function renderTags(){
 const map={};A.forEach(a=>a.tags.forEach(t=>(map[t]??=[]).push(a)));
 const tags=Object.keys(map).sort((a,b)=>a.localeCompare(b,"zh-CN"));
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">标签归档</div><h1>新闻标签</h1>
 <p class="lead">标签记录报道中的重要人物、机构、作品、平台、地点和主题。点击标签可进入相关报道。</p></section>
 <div class="tag-cloud tag-cloud-large">${tags.map(t=>`<a id="${tagSlug(t)}" class="tag tag-index-link" href="${articleURL(map[t][0])}" title="${esc(t)}">${esc(t)}${map[t].length>1?`（${map[t].length}篇）`:""}</a>`).join("")}</div>
 </main>`+footer;
}
const page=document.body.dataset.page;
({home:renderHome,edition:renderEdition,article:renderArticle,briefs:renderBriefs,categories:renderCategories,tags:renderTags}[page]||renderHome)();
})();