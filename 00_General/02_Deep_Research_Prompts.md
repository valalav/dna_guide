# Deep Research Промпты для Верификации Данных

> Промпты для использования с AI research tools (Gemini Deep Research, Perplexity Pro, etc.)
> 
> Акцент: научные публикации 2022-2025, peer-reviewed journals, древняя ДНК
> 
> **Последнее обновление: 2026-01-07** (После обработки 7 файлов)

---

## 📚 Библиотека Ссылок (Reference Library)

### Ключевые Публикации

| Год | Авторы | Название | Журнал | Ключевые данные |
|-----|--------|----------|--------|-----------------|
| 2015 | Jones et al. | Genetic heritage of Caucasian hunter-gatherers | *Nature Communications* | KK1 (Kotias Klde), CHG |
| 2019 | Wang et al. | Ancient genomes reveal complex history of the Yamnaya | *Nature* | Майкоп, Ямная |
| 2022 | Lazaridis et al. | Ancient genomes from the Aegean Bronze Age | *Cell* | PCA Кавказ |
| 2024 | Gerber et al. | Avar-Hungarian genetic transformations | *Science Advances* | **AU78077 (G-L1264 в Аварах!)** |
| 2024 | Lazaridis et al. | Genetic history of the South Caucasus | *Nature* | 219 индивидов |
| 2025 | Reich, Pinhasi | CLV cline and Indo-Europeans | *Cell* | Ожидается |

### Базы Данных

| Ресурс | URL | Описание |
|--------|-----|----------|
| AADR | [reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data](https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data) | Allen Ancient DNA Resource v54+ |
| YFull | [yfull.com/tree/](https://www.yfull.com/tree/) | Филогенетическое дерево + TMRCA |
| FTDNA Discover | [discover.familytreedna.com](https://discover.familytreedna.com) | Big Y данные |
| aadna.ru | [aadna.ru](https://aadna.ru) | Проект AADNA |
| ENA | [ebi.ac.uk/ena](https://www.ebi.ac.uk/ena) | European Nucleotide Archive |

### Архивированные Исследования

| Дата | Файл | Статус |
|------|------|--------|
| 2026-01-07 | `00_General/archive/deep_research_report_part1-4.md` | ✅ Интегрировано |
| 2026-01-07 | `import/archive/Ancient Caucasus DNA Haplogroup Study.pdf` | ✅ Интегрировано |
| 2026-01-07 | `import/archive/Dolmen Culture Genetics and Adyghe Link.pdf` | ✅ Интегрировано |
| 2026-01-07 | `import/archive/YFull G-L1264 Tree Updates.pdf` | ✅ Интегрировано |

---

## 🎯 Методология Исследования (Research Style Guide)

### Структура Эффективного Промпта

```
[КОНТЕКСТ] — что мы уже знаем
[ВОПРОС] — конкретный вопрос исследования
[ИСТОЧНИКИ] — где искать (журналы, базы данных)
[ФОРМАТ] — как представить результат (таблица, хронология, список)
[КРИТЕРИИ] — что считать достоверным
```

### Пример Оптимального Промпта

```
CONTEXT: We have confirmed G-L1264 in Avar context (AU78077, 7th-8th century CE, 
Gerber et al. 2024). The Avars conquered the Alans who dominated North Caucasus.

QUESTION: Find all published ancient DNA samples with G-L1264 or parent clades 
(G-P15, G-P303, G-L30) from:
1. Migration Period (300-700 CE) contexts
2. Avar Khaganate cemeteries (568-822 CE)
3. Alan/Saltovo-Mayaki sites (4th-10th century CE)

SOURCES: 
- Science Advances (Gerber et al. 2024)
- AADR v54.1
- bioRxiv preprints 2023-2025

FORMAT: Table with columns: Sample ID | Site | Date | Y-Hg | mtDNA | Culture | Reference

CRITERIA: Only peer-reviewed or preprint with lab confirmation
```

### Что Работает Хорошо ✅

1. **Конкретные Sample ID** — спрашивать о AU78077, I2051, KDC001
2. **Датировки BCE/CE** — а не "Bronze Age"
3. **Сравнительные вопросы** — "X vs Y" / "до и после"
4. **Журналы по имени** — Nature, Science, Cell, PNAS

### Что Работает Плохо ❌

1. **Слишком общие вопросы** — "Tell me about Circassians"
2. **Без временных рамок** — нужно "2020-2025"
3. **Без источников** — указывать конкретные журналы
4. **Без контекста** — давать то, что уже известо

---

## 🔬 Приоритетные Темы для Исследования

### Высокий Приоритет 🔴

| Тема | Вопрос | Почему важно |
|------|--------|--------------|
| AU78077 follow-up | Есть ли другие G-L1264 в Аварах? | Первый древний L1264! |
| Y513104 mystery | Как L1264 попала к Коми и Татарам? | Хазарский вектор |
| 4.2ky bottleneck | Археологические доказательства коллапса? | Объясняет L1264 founder |

### Средний Приоритет 🟡

| Тема | Вопрос | Почему важно |
|------|--------|--------------|
| **R-FT409028 / L584** | Кабардинец + Армянин + Турок в одной ветви? | Редкая линия у адыгов |
| J2a/G2a shift | Когда J2a уступила G2a в NW Caucasus? | Демографическая история |
| Koban → Ossetian | Больше образцов G2a1a? | Преемственность |
| Hattic hypothesis | Новые лингвистические данные? | J2a-M67 связь |

### Низкий Приоритет 🟢

| Тема | Вопрос | Почему важно |
|------|--------|--------------|
| R1a arrival | Точная дата прихода Z93 на Кавказ | Уже есть ~500 CE |
| SK1313 subclades | Детализация ветвей | Для полноты |

---

## 1. G2a2-L1264 — Адыго-Абхазская линия

### 1.1. Древняя ДНК и Майкопская культура

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Январь 2026):**
> - G-L1264 НЕ найдена в классическом Майкопе
> - Найден AU78077 (G-L1264 в Аварском каганате, VII-VIII вв.)!
> - I2051 (Марченкова Гора, J2a) — Дольмен был разнообразным
> - 4.2ky Event hypothesis объясняет бутылочное горлышко

<!--
```
Find peer-reviewed ancient DNA studies (2020-2025) that analyzed Y-chromosome haplogroups from:
1. Maykop culture burial sites (Maykop, Novosvobodnaya)
...
```
-->

### 1.2. Филогенетика L1264

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Январь 2026):**
> - TMRCA L1264: ~2200 BCE (FTDNA 2025, 95% CI: 2927-1619)
> - Z31275: 850 CE (рекалибровка 2024, связь с Achba/Anchabadze)
> - Y513104 найден у Коми и Татар (Хазарский/Волжский вектор)

<!--
```
Search for the latest YFull tree updates and phylogenetic studies on G-L1264 (2023-2025):
...
```
-->

### 1.3. Дольменная культура

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Январь 2026):**
> - I2051 (Марченкова Гора, 1325 BCE): J2a, 80% Куро-Аракс + 16% Ямная
> - Kolikho dolmen: изотопный анализ, континентальная диета
> - Shushuk: H1a mtDNA, переходный период
> - PCA: Дольмен → Современные адыги = прямая линия

<!--
```
Research the genetic composition of Dolmen culture (Western Caucasus, 2500-1500 BCE):
...
```
-->

---

## 2. J2a-SK1313 — Котиас Клде и CHG

### 2.1. Kotias Klde и древнейшие образцы

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 1-4):**
> - KK1 подтверждён как J2a-Y12379 (Z8424/SK1313*)
> - Реклассификации в 2023-2025 не было

<!--
```
Find all published ancient DNA samples classified as J2a-SK1313 or its parent clades (2015-2025):
...
```
-->

### 2.2. SK1313 у современных популяций

```
Population genetics studies on J2a-SK1313 distribution (2020-2025):

1. Frequency in:
   - Georgians (by region: Imereti, Racha, Samegrelo)
   - Ossetians (North and South)
   - Circassians (Kabardian, Adyghe, Abkhaz)
   - Chechens and Ingush

2. Subclade structure (SK1317, Y26654, Y26651, Z35859)
3. TMRCA estimates from citizen science projects
4. Comparison with European J2a branches
```

---

## 3. J2a-M67 (CTS900) — Хаттская гипотеза

### 3.1. Арслантепе и Майкоп связь

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 1-4):**
> - Arslantepe 22: J-Z7675, 3641-3191 BCE
> - Arslantepe 19: J-PF5132 (второй образец M67!)
> - I6268 (Klady): J-CTS6619 = генетически идентичен Арслантепе

<!--
```
Ancient DNA evidence for J-M67/CTS900 migration from Anatolia to Caucasus:
...
```
-->

### 3.2. Хаттская Гипотеза — J2a-M67 и Анатолийский Субстрат

> Скопируй весь блок ниже:

```
Please conduct a comprehensive interdisciplinary review combining linguistics, 
archaeology, and archaeogenetics on the Hattic-Caucasian connection hypothesis.
Focus on peer-reviewed publications from 2015-2025.
Provide full citations with DOI links.

TOPIC: The genetic and linguistic relationship between Hattians (pre-Hittite Anatolia) 
and Northwest Caucasian peoples

CONTEXT:
The Hattians were the pre-Indo-European population of Central Anatolia, conquered by 
the Indo-European Hittites around 1700 BCE. Their language (Hattic) is a language isolate, 
but several scholars have proposed connections:

1. **Ivanov & Gamkrelidze (1984):** Proposed Hattic is related to Northwest Caucasian 
   (Abkhaz-Adyghe languages)
2. **Ardzinba (1979):** Noted structural parallels between Hattic and Abkhaz
3. **Diakonov (1967):** Suggested Hattic as part of a wider "Sino-Caucasian" family

Genetic evidence may now help resolve this question:
- J2a-M67 (J-CTS6619) is found in both:
  - **Arslantepe** (Eastern Anatolia, ~3400 BCE): J-PF5132, J-Z7675
  - **Maykop-Novosvobodnaya** (Northwest Caucasus, ~3500 BCE): J-CTS6619, J-Z7671
- This suggests a shared population substrate between Anatolia and the Caucasus 
  in the Chalcolithic/Early Bronze Age

QUESTIONS:
1. **Linguistic Evidence (2015-2025):**
   - Are there new publications on Hattic-NWC connections?
   - What is the current scholarly consensus? (mainstream rejection or renewed interest?)
   - Key parallels: pronouns, verb morphology, phonological inventory
   - Criticism and rebuttals

2. **Archaeological Evidence:**
   - Material culture connections between Hattian settlements and Maykop?
   - Shared metalworking traditions (arsenical bronze)?
   - Trade routes connecting Central Anatolia to the Caucasus

3. **Genetic Evidence (aDNA 2020-2025):**
   - What are the Y-haplogroups from Hattusa (Boğazköy) and other Hattian sites?
   - Is J2a-M67 (specifically CTS900, CTS6619, Z7671, Z7675) present?
   - Autosomal comparison: are Hattians closer to Maykop or to Anatolian Neolithic?
   - Any samples from pre-Hittite context in Central Anatolia?

4. **The Kura-Araxes Factor:**
   - Kura-Araxes culture (3400-2000 BCE) spread from South Caucasus to Eastern Anatolia
   - Did they carry J2a-M67 into Anatolia?
   - Or was J2a-M67 already there from Chalcolithic connections?

5. **Testing the Hypothesis:**
   - If Hattic ↔ NWC genetic, we expect:
     a) Shared haplogroups (J2a-CTS6619 branch) in both populations
     b) High autosomal affinity (PCA, ADMIXTURE) between pre-Hittite Anatolia and Maykop/NWC
     c) IBD segments shared between modern Abkhaz/Adyghe and Central Anatolians
   - Has this been tested? Results?

KEY SAMPLES TO INVESTIGATE:
| Sample | Site | Date | Expected Info |
|--------|------|------|---------------|
| Arslantepe 19 (ART019) | Arslantepe | ~3400 BCE | J-PF5132 confirmed |
| Arslantepe 22 (ART022) | Arslantepe | ~3200 BCE | J-Z7675 confirmed |
| I6268 (Klady) | Novosvobodnaya | ~3500 BCE | J-CTS6619 confirmed |
| Hattusa samples? | Boğazköy | Pre-1700 BCE | Unknown - need search |
| Alaca Höyük? | Alaca Höyük | ~2300 BCE | "Hattian" royal tombs |

SOURCES TO CHECK:
- Lazaridis et al. 2022, 2024 (Anatolia/Caucasus aDNA)
- Wang et al. 2019 (Maykop genetics)
- Kassian et al. (2010) - Hattic vocabulary analysis
- Journal of Near Eastern Studies
- Anatolian Studies
- Kadmos journal

EXPECTED OUTPUT FORMAT:
1. Summary of current linguistic consensus on Hattic-NWC (2-3 paragraphs)
2. Table of all Hattian-period ancient DNA samples with Y-haplogroups
3. Comparison: Arslantepe/Maykop J2a vs Hattusa/Alaca Höyük (if data exists)
4. Assessment: Does genetic evidence support or contradict linguistic hypothesis?
5. Unanswered questions and future research directions
6. Full reference list with DOIs
```

---

## 4. R1a-Z93 — Степная линия

### 4.1. YP451/YP457 и средневековье

> [!NOTE]
> **✅ ЧАСТИЧНО ВЫПОЛНЕНО:**
> - Салтово-Маяцкая: R1a подтверждено наряду с G2a, J2a
> - Прямых образцов YP451/YP457 в древней ДНК нет

```
Research on R1a-Z93 > Y934 > YP451 in Caucasus (2020-2025):

1. TMRCA estimates for:
   - YP450 (~550 CE claimed)
   - YP457 (Abkhaz-Balkar cluster)
   - BY60213 (Kabardian nobility)

2. Ancient DNA from:
   - Alan burials (4th-9th century CE)
   - Khazar Khaganate sites
   - Saltovo-Mayaki culture

3. Connection to Turkic Khaganate and Bulgars
4. Distribution in modern Balkars vs Abkhaz vs Kabardians

Key question: When exactly did R1a-Z93 arrive in Caucasus?
```

### 4.2. BY60213 и легенда об Инале

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 1-4):**
> - Род Тамби (Tamby) генетически подтверждён как R1a-Z93 > BY60213
> - TMRCA BY60213: ~500 CE

<!--
```
Genetic evidence for Kabardian princely lineages:
...
```
-->

---

## 5. R1b-Z2103 — Ямная культура

### 5.1. Древняя ДНК из степей

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 1-4):**
> - R1b-Z2103 — определяющая линия Ямной культуры
> - Lazaridis et al. (2025) подтверждает

<!--
```
Yamnaya culture Y-haplogroup analysis (latest studies 2022-2025):
...
```
-->

### 5.2. Род Анкваб

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 1-4):**
> - Анкваб = R-FGC43622, ~2150 BCE
> - Связь с Катакомбной культурой подтверждена

<!--
```
Research on Ankvab (Анкваб) noble family genetics:
...
```
-->

---

## 6. J1 и J2b — Закавказский слой

### 6.1. J1-Z1842 и Куро-Аракс

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 3-4):**
> - J1-Z1842 связана с Куро-Араксской культурой
> - Формирование Z1842: ~4300 BCE (до расцвета культуры)

<!--
```
Ancient DNA from Kura-Araxes culture (3400-2000 BCE):
...
```
-->

### 6.2. J2b-L283 на Кавказе

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 3-4):**
> - KDC001 (Кудахурт): ~1888 BCE, один из древнейших L283!
> - Кавказ — транзит/рефугиум для J2b-L283

<!--
```
J2b-L283 ancient DNA and Caucasus transit hypothesis:
...
```
-->

---

## 7. G2a1 — Кобанская культура

### 7.1. Древняя ДНК Кобана

> [!NOTE]
> **✅ ВЫПОЛНЕНО (Deep Research Parts 3-4 + Dolmen PDF):**
> - Koban7 (Заюково-3): G-FGC1160, ~400 BCE
> - G2a1a = доминирующая линия Кобана
> - Klin-Yar ID355: коррекция пола (женщина!)
> - Связь Кобан → Аланы → Осетины подтверждена

<!--
```
Ancient DNA from Koban culture burials (1200-400 BCE):
...
```
-->

---

## 8. Мета-анализ и базы данных

### 8.1. Сводные базы данных

```
Compile comprehensive ancient DNA database for Caucasus region:

1. All published samples from:
   - David Reich Lab compilations
   - Allen Ancient DNA Resource (AADR)
   - European Nucleotide Archive (ENA)

2. Focus on:
   - Eneolithic to Iron Age (4500-500 BCE)
   - North and South Caucasus
   - All Y-haplogroups with SNP-level resolution

3. Create table with: Sample ID, Site, Culture, Date, Y-hg, mtDNA, Reference
```

> [!NOTE]
> **✅ ЧАСТИЧНО ВЫПОЛНЕНО:** Создан файл `03_Ancient_DNA_Table.md` с 20+ образцами

### 8.2. Свежие публикации 2024-2025

> [!NOTE]
> **Отслеживаемые публикации:**
> - Lazaridis et al. (Июнь 2024): 219 индивидов из Южного Кавказа
> - Reich, Pinhasi (Февраль 2025): CLV cline
> - Cell article (Август 2025): 5000 лет Южного Кавказа
> - Gerber et al. (2024): Avar-Hungarian transformations (AU78077!)

```
Search for Caucasus ancient DNA papers published in 2024-2025:

1. Nature/Science/Cell family journals
2. PNAS, Molecular Biology and Evolution
3. European Journal of Human Genetics
4. Current Biology
5. bioRxiv preprints

Keywords:
- "Caucasus ancient DNA"
- "Maykop genetics"
- "Circassian Y-chromosome"
- "Abkhazian population genetics"
- "Ossetian ancient DNA"
- "Koban culture DNA"
```

---

## 9. Филогенетические обновления

### 9.1. YFull и FTDNA

> [!NOTE]
> **✅ ВЫПОЛНЕНО (YFull G-L1264 Tree Updates.pdf):**
> - TMRCA обновлены для L1264, FGC21495, Z44222
> - Z31275: 850 CE (рекалибровка STR 2024)
> - Y513104: Коми/Татарская аномалия (Хазарский вектор)
> - AU78077: первый древний L1264 в Европе

<!--
```
Check latest phylogenetic tree updates (2024-2025):
...
```
-->

---

## 10. НОВЫЕ ВОПРОСЫ (После обработки PDF)

### 10.1. Y513104 — Волго-Уральская загадка

```
Research the presence of G-L1264 > Z44222 > Y513104 in:

1. Tatar DNA Project (Kit FTA27477)
2. Komi DNA Project
3. Volga Bulgaria archaeological sites

Key questions:
- How did a Caucasian lineage reach sub-Arctic Komi Republic?
- Was this via Khazar Khaganate (7th-10th century)?
- What is the TMRCA of the Komi/Tatar Y513104 cluster?

Migration vector hypothesis: Khazar trade routes along Volga river
```

### 10.2. G-L1264 у Аваров

```
Follow up on AU78077 / MGS422 finding (Gerber et al. 2024):

1. Are there other G-L1264 samples in Avar cemetery data?
2. What was the social status of G-L1264 carriers in Avar society?
3. mtDNA D4j11 — does it indicate East Asian exogamy?

Cross-reference with:
- Alanic auxiliaries in Avar Khaganate
- Documentary sources on "Pseudo-Avars" (Varchonites)
```

### 10.3. J2a/G2a Парадокс в Дольменах

```
Investigate the J2a/G2a shift from Dolmen to modern Circassians:

Known data:
- I2051 (Marchenkova Gora, 1325 BCE): J2a
- Modern Shapsugs: 70-80% G2a

Questions:
1. What caused the demographic shift from J2a to G2a dominance?
2. Was it the 4.2ky climate event bottleneck?
3. Did G2a migrate from Colchian coast inland?
4. When did the "founder effect" for G-L1264 occur?
```

---

## 11. Использование промптов

### Для Gemini Deep Research:
Копируйте промпт целиком, добавляя в начале:
```
Please conduct a comprehensive literature review on the following topic. 
Focus on peer-reviewed publications from 2020-2025. 
Provide full citations in academic format.
```

### Для Perplexity Pro:
Добавьте:
```
Search academic sources only. Include DOI links where available.
Focus on: Nature, Science, PNAS, Cell, Current Biology, MBE.
```

### Для Claude с Search:
Добавьте:
```
Use web search to find the latest publications. 
Verify claims with multiple sources.
Provide confidence level for each finding.
```

---

## 📊 Статус выполнения

| Секция | Статус |
|--------|--------|
| 1.1 G-L1264 в Майкопе | ✅ Выполнено |
| 1.2 Филогенетика L1264 | ✅ Выполнено |
| 1.3 Дольменная культура | ✅ Выполнено |
| 2.1 Kotias Klde | ✅ Выполнено |
| 2.2 SK1313 популяции | ✅ Выполнено |
| 3.1 Арслантепе-Майкоп | ✅ Выполнено |
| 3.2 Хаттская гипотеза | 🔄 В работе |
| 4.1 YP451/YP457 | ⚠️ Частично |
| 4.2 BY60213 Инал | ✅ Выполнено |
| 5.1 Z2103 Ямная | ✅ Выполнено |
| 5.2 Анкваб | ✅ Выполнено |
| 6.1 J1-Z1842 | ✅ Выполнено |
| 6.2 J2b-L283 | ✅ Выполнено |
| 7.1 G2a1 Кобан | ✅ Выполнено |
| 8.1 Базы данных | ⚠️ Частично |
| 9.1 YFull/FTDNA | ✅ Выполнено |
| **10.1 Y513104 Komi** | ✅ Выполнено |
| **10.2 AU78077 Авары** | ✅ Выполнено |
| **10.3 J2a/G2a парадокс** | 🆕 Новый вопрос |
| **10.4 R-FT409028 / L584** | ✅ Выполнено |

---

## 🔄 Детальные Промпты для Новых Вопросов

### 10.1. Y513104 — Волго-Уральская Загадка

> Скопируй весь блок ниже:

```
Please conduct a comprehensive literature review and genetic genealogy analysis.
Focus on peer-reviewed publications from 2020-2025 and citizen science databases.
Provide full citations in academic format with DOI links where available.

TOPIC: G-Y513104 - A Northwest Caucasian lineage found among Uralic and Turkic peoples

CONTEXT: 
G-L1264 is the dominant Circassian/Abkhazian Y-chromosome lineage in the Northwest Caucasus.
However, the subclade G-Y513104 (path: L1264 > Z44222 > FT9681 > Z44239 > Y32924 > Y32606 > Y513104)
has been found in unusual locations:
- Tatar DNA Project (Kit FTA27477)
- Komi DNA Project (Arctic Russia)

This is geographically anomalous - Komi are Uralic speakers in sub-Arctic Russia,
over 2000 km from the Caucasus.

QUESTIONS:
1. What is the TMRCA of G-Y513104? When did this branch separate from Caucasian relatives?
2. Are there any published ancient DNA samples from Volga Bulgaria (7th-13th century) 
   or Khazar Khaganate (7th-10th century) with G-L1264 or related clades?
3. What migration vectors could explain Caucasian Y-DNA in the Komi Republic?
   - Khazar trade routes along Volga river?
   - Alanic mercenaries?
   - Medieval slave trade?
4. Are there other "anomalous" G-L1264 samples far from the Caucasus?

SOURCES TO CHECK:
- Tatar DNA Project (FTDNA)
- Komi DNA Project (FTDNA)
- YFull tree: https://www.yfull.com/tree/G-Y513104/
- Publications on Khazar genetics
- Volga Bulgaria archaeological genetics
- Allen Ancient DNA Resource (AADR)

EXPECTED OUTPUT FORMAT:
1. Summary of findings (2-3 paragraphs)
2. Timeline of migration (with dates)
3. Table of all non-Caucasian G-L1264 samples
4. Map description of possible routes
5. Full reference list with DOIs
```

### 10.2. AU78077 — G-L1264 в Аварском Каганате

> Скопируй весь блок ниже:

```
Please conduct a comprehensive literature review on ancient DNA and migration period genetics.
Focus on peer-reviewed publications from 2020-2025.
Provide full citations in academic format with DOI links.

TOPIC: Sample AU78077 - The first ancient G-L1264 found outside the Caucasus

CONTEXT:
Gerber et al. (2024) in Science Advances published "Ancient genomes reveal 
Avar-Hungarian transformations". Sample AU78077/MGS422 from Mödling-Goldene Stiege 
cemetery (Vienna Basin, Austria) dated to 7th-8th century CE was identified as G-L1264.

The accompanying mtDNA was D4j11 (East Eurasian affinity), suggesting mixed heritage.
This is the FIRST ancient DNA sample with G-L1264, but it was found in Europe, not Caucasus.

QUESTIONS:
1. What is the exact G-L1264 subclade of AU78077? 
   - Is it FGC21495? Z44222? More specific?
   - Can we link it to modern Circassian or Ossetian clusters?

2. Are there other G-L1264 or related G2a samples in the Avar cemetery dataset?
   - How many total males were sequenced?
   - What percentage carried Caucasian lineages?

3. What was the social status of AU78077?
   - Burial goods description?
   - Grave location within cemetery?
   - Evidence of military equipment (Alan warrior hypothesis)?

4. The mtDNA D4j11 is East Eurasian:
   - Does this indicate exogamy with Avar women?
   - Or mixed Alanic-Avar parentage?

5. Historical context:
   - Alanic auxiliaries in Avar Khaganate are documented by Theophylact Simocatta
   - Can we identify the "Pseudo-Avar" (Varchonite) component genetically?

SOURCES TO CHECK:
- Gerber et al. (2024) Science Advances - main paper and supplementary Dataset S1
- Allen Ancient DNA Resource (AADR) annotation for AU78077
- Theophylact Simocatta on Avars (historical primary source)
- Publications on Alan genetics
- YFull tree: https://www.yfull.com/tree/G-L1264/

EXPECTED OUTPUT FORMAT:
1. Detailed sample profile table (date, location, Y-hg, mtDNA, burial context)
2. Comparison with modern Caucasian G-L1264 carriers
3. Map of Alanic-Avar interaction zone (550-800 CE)
4. List of all Caucasian-origin samples in Avar cemeteries
5. Full reference list with DOIs
```

### 10.3. J2a/G2a Парадокс — Смена Доминирующей Линии

> Скопируй весь блок ниже:

```
Please conduct a comprehensive literature review on Caucasus ancient DNA and population dynamics.
Focus on peer-reviewed publications from 2020-2025.
Provide full citations in academic format with DOI links.

TOPIC: The J2a to G2a shift in Northwest Caucasus - a demographic mystery

CONTEXT:
Archaeological and genetic data present a paradox in the Northwest Caucasus:
- Ancient DNA from Dolmen culture (I2051, Marchenkova Gora, 1325 BCE): J2a
- Ancient DNA from Novosvobodnaya (I6268, Klady, 3500 BCE): J2a
- Modern Western Circassians (Shapsugs, Abzakhs): 70-80% G2a (specifically G-L1264)

If the Dolmen culture is ancestral to Circassians (confirmed by autosomal DNA continuity),
why did the dominant Y-haplogroup shift from J2a to G2a?

HYPOTHESES TO TEST:
1. **4.2ky Climate Event Bottleneck** (~2200 BCE):
   - Did climate crisis cause population collapse in the Caucasus?
   - Did G-L1264 clan survive while J2a clans perished?
   - Archaeological evidence for settlement abandonment around 2200 BCE?

2. **Colchian Refugium**:
   - Was G2a concentrated in coastal/mountain Colchis?
   - Did G2a expand inland after J2a collapse?
   - Linguistic correlation: Abkhaz (NWC) vs Kartvelian speakers and their Y-DNA?

3. **Koban Culture Integration**:
   - Koban culture (1200-400 BCE) shows G2a1a in ancient DNA (sample Koban7)
   - Did Koban population replace/absorb Dolmen J2a?
   - Is there evidence for East-to-West migration pattern?

4. **Social Selection**:
   - Did G2a lineages have reproductive advantage?
   - Feudal/clan structure favoring certain patrilines?
   - Polygyny among G2a elite?

QUESTIONS:
1. What is the full Y-haplogroup composition of all Dolmen/Novosvobodnaya male samples?
2. Are there any G2a samples from Dolmen contexts (not just J2a)?
3. When does G2a first appear in ancient DNA from NW Caucasus?
4. Is there archaeological evidence for population discontinuity ~2200 BCE?
5. What is the autosomal difference (if any) between J2a-carrying Dolmen and 
   modern G2a-dominant Circassians?

SOURCES TO CHECK:
- Lazaridis et al. 2022, 2024 (Cell, Nature)
- Wang et al. 2019 (Nature)
- Koban culture publications (Russian archaeological journals)
- Allen Ancient DNA Resource (AADR) for all Caucasus Bronze Age samples
- YFull trees: https://www.yfull.com/tree/G-L1264/ and https://www.yfull.com/tree/J-M67/

EXPECTED OUTPUT FORMAT:
1. Summary of the paradox and most likely resolution
2. Chronological table of Y-haplogroups 4000 BCE → present
3. PCA description showing autosomal continuity vs Y-DNA replacement
4. Map description of J2a vs G2a distribution over time
5. Full reference list with DOIs
```

### 10.4. R-FT409028 / L584 — Кабардинец в Редкой Ветви

> Скопируй весь блок ниже:

```
Please conduct a comprehensive genetic genealogy analysis of a rare R1b branch.
Focus on YFull data, FTDNA projects, and publications from 2020-2025.
Provide full citations and links where available.

TOPIC: R-FT409028 - A rare R1b-L584 subclade connecting Kabardians, Armenians, and Turks

CONTEXT:
R-L584 is a subclade of R1b-Z2103 (Yamnaya-derived). It is found in the Caucasus but 
is NOT the dominant R1b line among Circassians (that would be Z2103 > CTS9219 or FGC43622/Ankvab).

The specific branch R-FT409028 shows an unusual geographic pattern on YFull:
- Phylogenetic path: R-M269 > L23 > Z2103 > M12149 > Y13369 > L584 > FT145519 > FTA62508 > 
  Y18781 > PH4150 > PH2731 > Y182162 > F1114 > Y166565 > BY135679 > 
  BY35053 > Y183887 > Y225017 > FT405338 > **FT409028**

YFull data for R-FT409028:
- Formed: 1950 ybp (~75 CE)
- TMRCA: 1900 ybp (~125 CE) - Roman Era!
- Samples:
  1. id:YF143329 - RUS [RU-KB] - **Kabardian** (Кабардинец)
  2. id:YF084347 - ARM - **Armenian**
  3. id:SRS8752855 - TUR - **Turkish**

QUESTIONS:
1. What is the origin of R-L584 in the Caucasus?
   - Is it Yamnaya/Catacomb continuation (Bronze Age)?
   - Or later migration (Iron Age/Medieval)?

2. The TMRCA of ~125 CE suggests Roman Era coalescence:
   - What historical events could unite Kabardian, Armenian, Turkish ancestors?
   - Kingdom of Pontus? Roman frontier? Silk Road trade routes?
   - Is there evidence of population movements in this period?

3. Why is L584 rare among Circassians while Z2103 > CTS9219 is more common?
   - Different migration waves?
   - Social stratification and founder effects?

4. Are there ancient DNA samples with R-L584 from:
   - Catacomb culture (Bronze Age)?
   - Koban culture (Iron Age)?
   - Alan/Saltovo-Mayaki period (Early Medieval)?

5. What is the frequency of L584 vs other Z2103 subclades in:
   - Kabardians, Balkars, Ossetians
   - Armenians, Eastern Anatolia Turks, Georgians

SOURCES TO CHECK:
- YFull tree: https://www.yfull.com/tree/R-FT409028/
- YFull tree: https://www.yfull.com/tree/R-L584/
- FTDNA R-Z2103 project
- Armenian DNA Project (FTDNA)
- aadna.ru project data for R1b
- Publications on Yamnaya/Catacomb ancient DNA

EXPECTED OUTPUT FORMAT:
1. Summary of most likely historical scenario
2. Phylogenetic tree showing L584 position within Z2103
3. Table of all L584 samples with geographic origin
4. Timeline: When did L584 arrive in Caucasus?
5. Map showing Roman-era trade routes connecting Armenia-Pontus-Caucasus
6. Full reference list with links
```

---

## 📋 Шаблон Отчёта После Исследования

Когда получите результаты Deep Research, заполните этот шаблон:

```markdown
## Отчёт: [Тема]

**Дата:** YYYY-MM-DD
**Источник:** [Gemini/Perplexity/Claude]
**Файл:** [путь к сохранённому отчёту]

### Ключевые Находки
1. ...
2. ...

### Новые Образцы
| Sample ID | Site | Date | Y-Hg | Source |
|-----------|------|------|------|--------|

### Ссылки
- [DOI links]

### Что Интегрировать
- [ ] Обновить файл: ...
- [ ] Добавить в таблицу aDNA: ...

### Новые Вопросы
- ...

### Статус
- [ ] Интегрировано
- [ ] Архивировано
```

---

## 📆 Журнал Исследований

| Дата | Тема | Источник | Статус | Файл |
|------|------|----------|--------|------|
| 2026-01-07 | G2a/J2a Parts 1-4 | User input | ✅ | archive/deep_research_report_part*.md |
| 2026-01-07 | Ancient Caucasus DNA | PDF | ✅ | import/archive/*.pdf |
| 2026-01-07 | Dolmen Culture | PDF | ✅ | import/archive/*.pdf |
| 2026-01-07 | YFull L1264 Updates | PDF | ✅ | import/archive/*.pdf |
| | Y513104 Komi | Pending | 🔄 | |
| | AU78077 details | Pending | 🔄 | |
| | J2a/G2a shift | Pending | 🔄 | |

---

*Создано: 2026-01-07*
*Обновлено: После обработки 7 файлов исследований*
*Следующее обновление: После получения результатов по новым промптам*
