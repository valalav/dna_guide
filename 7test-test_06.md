<h1>Гаплогруппа O-K13</h1>

<style>
/* Стили для спойлеров */
details.dna-spoiler {
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    margin-bottom: 12px;
    background-color: #fff;
    overflow: hidden;
}
details.dna-spoiler summary {
    list-style: none;
    padding: 12px 16px;
    background-color: #f6f8fa;
    cursor: pointer;
    font-weight: 600;
    font-size: 15px;
    color: #24292e;
    display: flex;
    align-items: center;
    transition: background 0.2s;
    outline: none;
}
details.dna-spoiler summary:hover {
    background-color: #eef1f4;
}
details.dna-spoiler summary::-webkit-details-marker {
    display: none;
}
details.dna-spoiler summary::before {
    content: '▶';
    font-size: 10px;
    margin-right: 12px;
    display: inline-block;
    transition: transform 0.2s;
    color: #586069;
}
details.dna-spoiler[open] summary::before {
    transform: rotate(90deg);
}
details.dna-spoiler[open] summary {
    border-bottom: 1px solid #e1e4e8;
    margin-bottom: 0;
}
.dna-spoiler-content {
    padding: 20px;
    background-color: #fff;
}
.dna-spoiler-content a {
    color: #0366d6;
    text-decoration: none;
}
.dna-spoiler-content a:hover {
    text-decoration: underline;
}
.dna-spoiler-content h1, 
.dna-spoiler-content h2, 
.dna-spoiler-content h3 {
    font-size: 1.15em !important;
    border-bottom: none !important;
    margin-top: 1em !important;
}
/* Timeline styles - diagonal layout */
.tmrca-timeline {
    position: relative;
    padding: 20px 10px;
    margin: 15px 0;
    /* Clean background */
    background: transparent;
}
/* Removed misaligned background line */
.tmrca-item {
    position: relative;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 1;
    background: white;
    border-radius: 8px;
    margin-bottom: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.tmrca-item:hover {
    transform: translateX(5px);
}
.tmrca-item:hover {
    transform: translateX(5px);
}
/* Removed legacy ::before pseudo-elements to avoid double-dot issue */
.tmrca-branch {
    font-weight: 600;
    color: #1f2937;
    min-width: 100px;
}
.tmrca-branch {
    font-weight: 600;
    color: #1f2937;
    min-width: 100px;
}
.tmrca-item.major .tmrca-branch {
    color: #d97706;
    font-size: 1.1em;
}
.tmrca-item.current .tmrca-branch {
    color: #22c55e;
}
.tmrca-years {
    color: #6b7280;
    font-size: 0.85em;
    font-family: monospace;
}
.tmrca-label {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75em;
    margin-left: auto;
}
.tmrca-item.major .tmrca-label {
    background: #fef3c7;
    color: #92400e;
}
.tmrca-item.current .tmrca-label {
    background: #dcfce7;
    color: #166534;
}
/* Pre-major horizontal table styles */
.tmrca-pre-major {
    margin-bottom: 20px;
    overflow-x: auto;
}
.tmrca-table {
    border-collapse: collapse;
    width: 100%;
    font-size: 13px;
}
.tmrca-cell {
    border: 1px solid #e1e4e8;
    padding: 8px 12px;
    text-align: center;
    background: #f9fafb;
    min-width: 60px;
}
.tmrca-branch-name {
    font-weight: 600;
    color: #1f2937;
}
.tmrca-age {
    color: #6b7280;
    font-size: 0.85em;
    font-family: monospace;
    margin-top: 4px;
}
/* Post-major diagonal with vertical scale */
.tmrca-post-major {
    position: relative;
    display: flex;
    margin-top: 20px;
    min-height: 450px; /* Increased height again for better spacing */
}
.tmrca-scale {
    width: 60px;
    position: relative;
    border-right: 2px solid #e1e4e8;
    margin-right: 20px;
}
.tmrca-tick {
    position: absolute;
    right: 8px;
    font-size: 11px;
    color: #6b7280;
    font-family: monospace;
    transform: translateY(-50%);
}
.tmrca-tick::after {
    content: '';
    position: absolute;
    right: -10px;
    top: 50%;
    width: 8px;
    height: 1px;
    background: #e1e4e8;
}
.tmrca-timeline-diagonal {
    flex: 1;
    position: relative;
    padding: 10px 0;
}
.tmrca-item.current {
    /* Flush right for the deepest branch - strictly at bottom */
    position: absolute !important;
    right: 0 !important;
    bottom: 0 !important;
    margin: 0 !important;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 12px;
}
.tmrca-item {
    display: flex;
    align-items: center;
    gap: 8px; /* Gap between age and branch name */
}
.tmrca-age-inline {
    font-size: 13px; /* Larger font */
    color: #059669; /* Greenish tint */
    background: #ecfdf5;
    padding: 1px 6px;
    border-radius: 4px;
    font-family: monospace;
    white-space: nowrap;
    border: 1px solid #d1fae5;
}
.tmrca-deepest-age-inline {
    font-size: 15px; /* Even larger for deepest */
    font-weight: 700;
    color: #16a34a;
    background: #f0fdf4;
    padding: 3px 10px;
    border-radius: 4px;
    border: 1px solid #bbf7d0;
    white-space: nowrap;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
</style>



<p><strong>Фамилия:</strong> Кушбоков<br>
<strong>Kit Number:</strong> YF143329<br>
<strong>Субэтнос:</strong> Кабардинец<br>
<strong>Населенный пункт:</strong> Нартан<br>
<strong>Тест:</strong> WGS</p>

<h2>Краткое резюме</h2>

<p>&nbsp;</p>

<br>


[github_md path="00_General/00_wgs.md"]


<p><strong>Возраст ветки (TMRCA):</strong> 3100 лет<br>
<strong>Путь:</strong>  > A0-T > A1 > A1b > BT > CT > CF > F > GHIJK > HIJK > IJK > K > K2 > K-M2308 > K-M2335 > NO > O > O-F265 > O-M268 > O-P49 > O-F1658 > O-CTS9259 > O-K10 > O-47Z > O-CTS10674 > O-K2 > O-K13</p>

<details class="dna-spoiler">
<summary>⏱️ Путь с датировками TMRCA</summary>
<div class="dna-spoiler-content">


<!-- Pre-major: horizontal table -->
<div class="tmrca-pre-major">
<table class="tmrca-table">
<tr>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">A0-T</div>
    <div class="tmrca-age">~161 300</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">A1</div>
    <div class="tmrca-age">~133 400</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">A1b</div>
    <div class="tmrca-age">~130 700</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">BT</div>
    <div class="tmrca-age">~88 000</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">CT</div>
    <div class="tmrca-age">~68 500</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">CF</div>
    <div class="tmrca-age">~65 900</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">F</div>
    <div class="tmrca-age">~48 800</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">GHIJK</div>
    <div class="tmrca-age">~48 500</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">HIJK</div>
    <div class="tmrca-age">~48 500</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">IJK</div>
    <div class="tmrca-age">~47 200</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">K</div>
    <div class="tmrca-age">~45 400</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">K2</div>
    <div class="tmrca-age">~45 400</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">K-M2308</div>
    <div class="tmrca-age">~45 400</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">K-M2335</div>
    <div class="tmrca-age">~41 500</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">NO</div>
    <div class="tmrca-age">~36 800</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O</div>
    <div class="tmrca-age">~30 500</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-F265</div>
    <div class="tmrca-age">~30 000</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-M268</div>
    <div class="tmrca-age">~28 100</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-P49</div>
    <div class="tmrca-age">~25 700</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-F1658</div>
    <div class="tmrca-age">~11 400</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-CTS9259</div>
    <div class="tmrca-age">~11 000</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-K10</div>
    <div class="tmrca-age">~7 000</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-47Z</div>
    <div class="tmrca-age">~5 700</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-CTS10674</div>
    <div class="tmrca-age">~4 600</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-K2</div>
    <div class="tmrca-age">~3 100</div>
</td>

<td class="tmrca-cell">
    <div class="tmrca-branch-name">O-K13</div>
    <div class="tmrca-age">~3 100</div>
</td>

</tr>
</table>
</div>




</div>
</details>

<p><a href="https://github.com/valalav/dna_guide/blob/main/02_Practical/01_YFull_Guide.md">Как читать YFull — экскурсия по интерфейсу</a></p>

<p>&nbsp;</p>

<h2>История</h2>

<p></p>

<p>&nbsp;</p>

<h2>Справочная информация</h2>

[github_md path="00_General/00_inf.md"]



<!-- Список представителей (Spoiler) -->

<details class="dna-spoiler">
<summary>👥 Список представителей (1)</summary>
<div class="dna-spoiler-content">
<table>
<thead>
<tr><th>Фамилия</th><th>Имя</th><th>Kit</th><th>Субэтнос</th><th>Населенный пункт</th></tr>
</thead>
<tbody>

<tr><td>Кушбоков</td><td></td><td>YF143329</td><td>Кабардинец</td><td>Нартан</td></tr>

</tbody>
</table>
</div>
</details>


<!-- Соседние ветви (Spoiler) -->


<!-- STR Matches (для всех типов тестов) -->
<details class="dna-spoiler">
<summary>🔗 STR Совпадения</summary>
<div class="dna-spoiler-content">
[github_md path="00_General/00_strmf.md"]
</div>
</details>


<!-- Митохондриальная ДНК (Spoiler) -->
<details class="dna-spoiler">
<summary>🧬 Митохондриальная ДНК</summary>
<div class="dna-spoiler-content">
<ul>
<li><a href="https://github.com/valalav/dna_guide/blob/main/04_Women/02_mtDNA_Guide.md">02_mtDNA_Guide.md</a> (Справочник по mtDNA)</li>
</ul>
</div>
</details>

<!-- Аутосомный портрет (Spoiler) -->
<details class="dna-spoiler">
<summary>📊 Аутосомный портрет</summary>
<div class="dna-spoiler-content">
<ul>
<li><a href="https://github.com/valalav/dna_guide/blob/main/05_Autosomal/01_Autosomal_Guide.md">01_Autosomal_Guide.md</a> (Справочник по аутосомам)</li>
</ul>
</div>
</details>




<h2>Внешние ссылки</h2>
<ul>
<li><a href="https://www.yfull.com/tree/O-K13/">YFull Tree</a></li>
<li><a href="https://aadna.ru/">Проект AADNA</a></li>
</ul>