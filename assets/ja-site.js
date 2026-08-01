(() => {
const M=window.XNEWS_JA_META,S=M.site,A=window.XNEWS_JA_ARTICLES||[];
const bySlug=Object.fromEntries(A.map(a=>[a.slug,a]));
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const nav=`<nav class="nav wrap"><a href="${S.jaBase}/">ホーム</a><a href="${S.jaBase}/2026/08/02/">8月2日の日報</a><a href="${S.jaBase}/categories.html">カテゴリー</a><a href="${S.jaBase}/tags.html">タグ</a><a href="${S.base}/">简体中文</a></nav>`;
const header=`<header class="masthead"><div class="wrap"><div class="brand"><a href="${S.jaBase}/">XNEWS</a></div><div class="tagline">日本のXで注目されたニュースと文化</div></div></header>`;
const footer=`<footer class="footer"><div class="wrap">XNEWS · 日本のXで注目されたニュースを記録する。</div></footer>`;
const url=a=>`${S.jaBase}/2026/08/02/${a.slug}/`;
const zh=a=>`${S.base}/2026/08/02/reports/${a.slug}.html`;
const card=(a,compact=false)=>`<article class="story${compact?" compact":""}"><div class="story-meta">${a.categories.map(esc).join(" / ")} · ${esc(S.date)}</div><h2><a href="${url(a)}">${esc(a.title)}</a></h2><p>${esc(a.summary)}</p></article>`;
const app=document.getElementById("app");
function home(){
 const f=A.filter(a=>a.level==="focus"),s=A.filter(a=>a.level==="standard"),lead=f[0];
 app.innerHTML=header+nav+`<main class="wrap"><section class="home-lead"><div class="kicker">${S.date} · 前日のニュース</div><div class="lead-layout"><div><h1><a href="${url(lead)}">${esc(lead.title)}</a></h1><p class="lead">${esc(lead.summary)}</p><div class="home-meta">${lead.categories.map(esc).join(" / ")} · ${S.date}</div></div><div class="lead-side"><h2>8月2日の日報</h2><p>主要ニュース3本、その他2本。</p><a class="button-link" href="${S.jaBase}/2026/08/02/">日報を読む</a></div></div></section><section class="homepage-section"><h2 class="section-title">主要ニュース</h2><div class="feature-grid">${f.slice(1,5).map(a=>card(a)).join("")}</div></section><section class="homepage-section"><h2 class="section-title">最新記事</h2><div class="card-grid">${f.slice(5).concat(s.slice(0,8)).map(a=>card(a,true)).join("")}</div></section><section class="homepage-section"><h2 class="section-title">すべての記事</h2><div class="card-grid">${s.slice(8).map(a=>card(a,true)).join("")}</div></section></main>`+footer;
}
function edition(){
 const f=A.filter(a=>a.level==="focus"),s=A.filter(a=>a.level==="standard");
 app.innerHTML=header+nav+`<main class="wrap"><section class="hero edition-hero"><div class="kicker">デイリーアーカイブ</div><h1>${S.date} 日本Xニュース日報</h1><p class="lead">8月1日は円相場と企業決算から、夜のテレビ、映画、ゲーム、プロ野球、深夜の誕生日・周年投稿へ関心が移った。</p><div class="edition-stats"><span>記事5本</span><span>主要3本</span><span>その他2本</span></div></section><div class="edition-layout"><section><h2 class="section-title">主要ニュース</h2>${f.map(a=>card(a)).join("")}<h2 class="section-title">その他のニュース</h2><div class="card-grid">${s.map(a=>card(a,true)).join("")}</div></section><aside class="side sticky-side"><h3>WordPress原稿</h3><p class="meta"><a href="https://github.com/horse/xnews/tree/main/content/ja/2026-08-01">Markdownを開く</a></p><h3>言語</h3><p class="meta"><a href="${S.base}/2026/08/02/">简体中文版</a></p></aside></div></main>`+footer;
}
function article(){
 const a=bySlug[document.body.dataset.slug]; if(!a)return;
 app.innerHTML=header+nav+`<main class="article"><div class="breadcrumb"><a href="${S.jaBase}/">ホーム</a><span>›</span><a href="${S.jaBase}/2026/08/02/">${S.date}</a><span>›</span><span>${esc(a.title)}</span></div><div class="post-categories">${a.categories.map(esc).join("、")}</div><h1>${esc(a.title)}</h1><p class="dek">${esc(a.summary)}</p><div class="post-meta"><time>${S.date}</time><span>執筆：XNEWS編集部</span><span><a href="${zh(a)}">简体中文</a></span></div>${a.body.map(p=>`<p>${esc(p)}</p>`).join("")}<div class="source-note"><strong>出典：</strong>${a.sources.map(([n,u])=>`<a href="${esc(u)}">${esc(n)}</a>`).join(" · ")}</div><section class="post-taxonomy"><div><strong>カテゴリー</strong><span>${a.categories.map(esc).join("、")}</span></div><div><strong>タグ</strong><div class="tag-list">${a.tags.map(t=>`<a class="tag" href="${S.jaBase}/tags.html">${esc(t)}</a>`).join("")}</div></div></section><a class="back" href="${S.jaBase}/2026/08/02/">← 日報に戻る</a></main>`+footer;
}
function cats(){const m={};A.forEach(a=>a.categories.forEach(c=>(m[c]??=[]).push(a)));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">カテゴリー</div><h1>ニュースカテゴリー</h1></section>${Object.keys(m).sort().map(c=>`<section class="archive-section"><h2>${esc(c)} <span class="archive-count">${m[c].length}</span></h2><ul class="archive-list">${m[c].map(a=>`<li><time>${S.date}</time><a href="${url(a)}">${esc(a.title)}</a></li>`).join("")}</ul></section>`).join("")}</main>`+footer;}
function tags(){const m={};A.forEach(a=>a.tags.forEach(t=>(m[t]??=[]).push(a)));app.innerHTML=header+nav+`<main class="wrap"><section class="hero"><div class="kicker">タグ</div><h1>ニュースタグ</h1></section><div class="tag-cloud tag-cloud-large">${Object.keys(m).sort().map(t=>`<a class="tag tag-index-link" href="${url(m[t][0])}">${esc(t)}${m[t].length>1?`（${m[t].length}本）`:""}</a>`).join("")}</div></main>`+footer;}
({home,edition,article,categories:cats,tags}[document.body.dataset.page]||home)();
})();