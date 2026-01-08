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

## ⚠️ КРИТИЧЕСКИ ВАЖНО: Правила Интерпретации Гаплогрупп

> [!CAUTION]
> **НИКОГДА не делайте глубокие выводы по поверхностным данным!**

### Главная Ошибка

Нельзя утверждать, что популяция A "идентична" популяции B на основании совпадения 
**верхнеуровневых гаплогрупп** (G2a1a, R1a-Z93, J2a и т.д.)!

**Пример НЕПРАВИЛЬНОГО вывода:**
> ❌ "G2a1a у Сванов = идентичен Осетинам, значит они родственники"

**Почему это ошибка:**
1. G2a1a — это **зонтичная гаплогруппа**, объединяющая МНОЖЕСТВО разных ветвей
2. У Осетин G2a1a представлена **одной неглубокой линией** (founder effect)
3. У других народов G2a1a может быть представлена **совершенно другими субкладами**
4. Совпадение на уровне G2a1a может означать **общего предка 10,000+ лет назад**

### TMRCA из YFull (current_tree.json) — Источник Истины

**Для всех TMRCA данных используйте `current_tree.json` в корне проекта!**

| SNP | Formed (ybp) | TMRCA (ybp) | Возраст |
|-----|--------------|-------------|---------|
| L1264 | 4900 | 4400 | ~2400 BCE — ДРЕВНЯЯ ЛИНИЯ! |
| FGC21495 | 4400 | 3900 | ~1900 BCE — всё ещё ДРЕВНЯЯ! |
| Y142023 | 3900 | 3600 | ~1600 BCE |

> [!WARNING]
> **FGC21495 = 3900 лет TMRCA!** Это НЕ "терминальный" SNP для выводов о родстве!
> Даже "глубокие" субклады могут иметь древних предков.

### Правильный Подход

| Уровень | Пример | TMRCA | Вывод |
|---------|--------|-------|-------|
| Поверхностный | G2a | ~25000 лет | ❌ Никакой |
| Средний | G2a1a/G2a2b | ~10000 лет | ❌ Слишком древний |
| Субклад | L1264 | ~4400 лет | ⚠️ Древний — нужны подветви |
| Подветвь | FGC21495 | ~3900 лет | ⚠️ Всё ещё древний! |
| Терминальный | **Смотреть TMRCA <500 лет** | <500 лет | ✅ Можно делать выводы |

### Что НУЖНО проверять:

1. **`current_tree.json`** — источник истины для TMRCA
2. **Терминальные SNP** — но проверять их TMRCA!
3. **Подветви/Субклады** — какие именно нижележащие ветки
4. **STR-маркеры** — для групп с близким TMRCA
5. **Распределение субкладов** — разнообразие внутри популяции

### Примеры Различий

| Популяция A | Популяция B | Общий SNP | TMRCA | Реальность |
|-------------|-------------|-----------|-------|------------|
| Осетины | Балкарцы | G2a1a | >10000 лет | ❌ Разные древние ветви |
| Сваны | Осетины | G2a1a | >10000 лет | ❌ Требует глубокого анализа |
| Адыги | Абхазы | L1264 | 4400 лет | ⚠️ Разные ветви: Z44222 vs FGC21495 |
| Внутри клана | Внутри клана | Терминальный | <500 лет | ✅ Родство |

### Правило

> [!IMPORTANT]
> **При любом сравнении популяций:**
> 1. Проверьте TMRCA в `current_tree.json`!
> 2. TMRCA >1000 лет = НЕ делать выводов о "родстве"
> 3. TMRCA <500 лет = можно рассматривать генеалогическое родство
> 4. Big Y данные, а не устаревшие SNP-панели

Поверхностные данные (G2a, R1a, J2) = **только отправная точка**, 
НЕ основание для выводов о родстве народов!

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

### 4.1. YP451/YP457 — Тюркско-Аланское Наследие R1a-Z93

> [!NOTE]
> **✅ ЧАСТИЧНО ВЫПОЛНЕНО:**
> - Салтово-Маяцкая: R1a подтверждено наряду с G2a, J2a
> - Прямых образцов YP451/YP457 в древней ДНК нет

> Скопируй весь блок ниже:

```
Please conduct a comprehensive phylogeographic and historical analysis of R1a-Z93 
subclades in the Caucasus, focusing on medieval steppe connections.
Focus on peer-reviewed publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: R1a-Z93 > Y934 > YP451/YP457 — When and how did steppe R1a arrive in the Caucasus?

CONTEXT:
R1a-Z93 is the defining Y-haplogroup of the Indo-Iranian steppe migrations (Sintashta, 
Andronovo, Scythians). It is NOT indigenous to the Caucasus. Yet today, specific 
subclades of R1a-Z93 are found among Caucasian ethnic groups:

- **YP451 (TMRCA ~550 CE):** Found in Balkars, Karachays, Ossetians
- **YP457:** An Abkhaz-Balkar specific cluster
- **BY60213 (TMRCA ~500 CE):** Linked to Kabardian nobility (Tamby/Тамби family)

The timing (~500-600 CE) suggests arrival during the **Migration Period**, not the 
Bronze Age Scythians. This coincides with:
- Collapse of the Hunnic Empire (~453 CE)
- Rise of the Turkic Khaganate (552 CE)
- Avar conquest (568 CE)
- Khazar Khaganate formation (~650 CE)

QUESTIONS:
1. **Phylogenetic Position:**
   - What is the exact path: Z93 > Z94 > Z2124 > Y934 > YP451 > YP457?
   - TMRCA of each node? (YFull, FTDNA)
   - Which branch is BY60213? (parallel to YP457 or under it?)

2. **Ancient DNA Search:**
   - Are there any R1a-Z93 samples from:
     a) Saltovo-Mayaki culture (8th-10th c. CE)?
     b) Khazar burial sites (Don, Volga)?
     c) Alan cemeteries (Kislovodsk basin, 4th-9th c.)?
     d) Hunnic-period burials in the Caucasus?
   - If yes, what subclades? Y934+? YP451+?

3. **Turkic Connection:**
   - YP451 is found in Tuvans, Yakuts, and other Siberian Turkic peoples
   - Did it arrive to the Caucasus via:
     a) Turkic Khaganate mercenaries?
     b) Bulgar tribes?
     c) Proto-Hungarian/Onogur groups?
   - Or did Caucasian carriers migrate east (Alan diaspora)?

4. **The Inal Legend:**
   - Kabardian oral tradition names Inal (~XV c.) as founding prince
   - BY60213 (TMRCA ~500 CE) is 1000 years OLDER than Inal
   - How to reconcile genetic and oral history?
   - Were pre-Inal carriers of BY60213 royal, or was there later adoption?

5. **Modern Distribution:**
   - Frequency of YP451 in: Balkars, Karachays, Ossetians, Kabardians, Abkhaz
   - Compare with: Volga Tatars, Bashkirs, Chuvash
   - Is there a "Steppe Corridor" signature (continuous cline vs discrete clusters)?

KEY SAMPLES TO FIND:
| Sample | Site | Period | Expected |
|--------|------|--------|----------|
| Saltovo-Mayaki males | Don basin | 8th-10th c. | R1a expected |
| Kislovodsk Alans | N. Ossetia | 4th-9th c. | R1a? G2a? |
| Khazar warriors | Volga | 7th-10th c. | Mixed package |

SOURCES TO CHECK:
- YFull: https://www.yfull.com/tree/R-YP451/
- FTDNA R1a project
- Unterländer et al. (2017) - Scythian aDNA
- Damgaard et al. (2018) - Steppe aDNA
- Publications on Alan genetics (Russian journals)
- Khazar archaeological genetics

EXPECTED OUTPUT FORMAT:
1. Summary of YP451/YP457 phylogeny with TMRCA dates
2. Table of all relevant ancient DNA samples with R1a from Caucasus/Steppe
3. Map of YP451 distribution (modern + ancient if available)
4. Historical scenario: most likely vector of R1a-Z93 arrival to Caucasus
5. Resolution of Inal legend vs. genetic dating discrepancy
6. Full reference list with DOIs
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
| 3.2 Хаттская гипотеза | ✅ Выполнено |
| 4.1 YP451/YP457 | ✅ Выполнено |
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
| **10.3 J2a/G2a парадокс** | ✅ Выполнено |
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
Please conduct a comprehensive interdisciplinary analysis of Y-DNA turnover in the 
Northwest Caucasus, combining ancient DNA, archaeology, and demographic modeling.
Focus on peer-reviewed publications from 2018-2025.
Provide full citations in academic format with DOI links.

TOPIC: The J2a to G2a shift in Northwest Caucasus - a demographic mystery

CONTEXT:
Archaeological and genetic data present a fundamental paradox in the Northwest Caucasus.
The Y-chromosomal composition of the ancient population differs dramatically from 
modern inhabitants, despite clear autosomal continuity:

ANCIENT DNA (3500-1300 BCE):
| Sample | Site | Date | Y-Hg | Culture |
|--------|------|------|------|---------|
| I6268 | Klady | 3516-3370 BCE | **J2a-Z7671** | Novosvobodnaya |
| I6266 | Maykop | ~3300 BCE | J2a | Maykop |
| OSS002 | Unakozovskaya | ~3100 BCE | J2a-M410 | Late Maykop |
| I2051 | Marchenkova Gora | ~1325 BCE | **J2a-L283** | Late Dolmen / Pre-Koban |
| MK5001 | Maykop | Late Maykop | L (L1b2) | Late Maykop |

MODERN Y-DNA (Western Circassians):
- **Shapsugs:** 70-80% G2a (mostly G-L1264)
- **Abzakhs:** 60-75% G2a
- **Abkhazians:** 50-70% G2a
- J2a: now only 5-15%!

THE PARADOX:
If autosomal DNA shows continuity (Lazaridis 2022 confirms Dolmen→Circassian), 
why did the Y-chromosomal signature completely change from J2a to G2a?

HYPOTHESES TO TEST:
1. **4.2 Kiloyear Bottleneck (~2200 BCE):**
   - Global climate crisis (drought, aridification)
   - Collapse of complex societies (Akkad, Egypt Old Kingdom, Maykop)
   - Did J2a clans in open valleys perish while G2a in mountain refugia survived?
   - Archaeological evidence for settlement abandonment around 2200 BCE?
   - CRITICAL: G-L1264 TMRCA = ~2200 BCE perfectly coincides with the event!

2. **Colchian Refugium Hypothesis:**
   - G2a concentrated in humid Black Sea coast (Colchis)?
   - Post-crisis expansion from coast into depopulated interior?
   - Linguistic test: Are NWC languages (Abkhaz-Adyghe) linked to Colchian origin?
   - G2a subclades in Mingrelians/Svans vs Circassians?

3. **Female Continuity / Y-DNA Replacement:**
   - mtDNA haplogroups: H, U5, T2 show direct Dolmen→Circassian continuity
   - Model: G2a males married into surviving J2a families
   - Over generations, patrilocal drift eliminated J2a lineages
   - Similar pattern to Bell Beaker replacement in Spain

4. **Social Selection / Reproductive Skew:**
   - Koban/Meotian cultures were stratified warrior societies
   - Did G2a lineages become the new military aristocracy?
   - Polygyny amplifying G2a at expense of other lineages?
   - "Star burst" expansion pattern in G-L1264 phylogeny?

KOBAN MISSING LINK:
| Sample | Site | Date | Y-Hg | Significance |
|--------|------|------|------|--------------|
| Koban7 | Zayukovo-3 | Iron Age | **G-FGC1160** (G2a1a) | G2a in central Caucasus! |
| Koban9 | Zayukovo-3 | Iron Age | **G-Z6554** (G2a1a) | Confirms G2a expansion |

BUT: G2a1a (Koban samples) ≠ G2a2b/L1264 (Western Circassians)!
This suggests multiple G2a populations in different regions.

QUESTIONS:
1. **Complete Y-DNA inventory:**
   - List ALL Y-haplogroups from Dolmen/Novosvobodnaya/Maykop
   - Are there ANY G2a samples from Dolmen contexts?
   - First appearance of G2a in NW Caucasus ancient DNA?

2. **Chronology of shift:**
   - At what point (date range) does G2a emerge in ancient DNA?
   - Gap between last J2a-dominant sample and first G2a-dominant sample?

3. **Autosomal analysis:**
   - PCA/ADMIXTURE of J2a-carrying ancients vs G2a-carrying moderns
   - Any measurable autosomal differences?
   - Evidence for external admixture with G2a arrival?

4. **Meotian connection:**
   - Meotians (ancestors of Adyghe) lived in Kuban, 600 BCE - 400 CE
   - ANY ancient DNA from Meotian burials?
   - Was Meotian population G2a or J2a?

5. **Simulation/modeling:**
   - Has anyone modeled the demographic scenario numerically?
   - What bottleneck size + reproductive skew explains observed shift?

KEY SOURCES TO CHECK:
- Lazaridis et al. (2022) - Cell - Caucasus continuity
- Wang et al. (2019) - Nature - Maykop genetics
- Koban culture publications (Russian journals)
- Gerber et al. (2024) - AU78077 G-L1264 in Avar context
- Allen Ancient DNA Resource (AADR) - complete Caucasus dataset
- Harney et al. (2021) - Koban samples
- Reich lab supplementary datasets

EXPECTED OUTPUT FORMAT:
1. Summary of paradox with most likely resolution (2-3 paragraphs)
2. **Complete Y-hg chronology table** 4000 BCE → 500 CE
3. PCA/ADMIXTURE description of autosomal continuity
4. Schematic map of J2a vs G2a distribution over time (textual description)
5. Demographic model parameters if any published
6. Remaining unanswered questions
7. Full reference list with DOIs
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

## � Фаза 2: Новые Исследовательские Направления

### Приоритетная Матрица (Фаза 2)

| # | Тема | Приоритет | Статус |
|---|------|-----------|--------|
| 11.1 | Меотийская aDNA | 🔴 Высокий | ✅ Выполнено |
| 11.2 | G2a1a vs G2a2b split | 🔴 Высокий | ✅ Выполнено |
| 11.3 | mtDNA Continuity | 🔴 Высокий | ✅ Выполнено |
| 11.4 | J1-Z1842 субклады | 🟡 Средний | ✅ Выполнено |
| 11.5 | Q1a на Кавказе | 🟡 Средний | ✅ Выполнено |
| 11.6 | Аутосомный профиль | 🟡 Средний | ✅ Выполнено |
---

## 🔬 Фаза 4: Продвинутые Темы

### Приоритетная Матрица (Фаза 4)

| # | Тема | Приоритет | Статус |
|---|------|-----------|--------|
| 12.1 | Абхазы vs Адыги | 🟡 Средний | ✅ Выполнено |
| 12.2 | Генетика Княжеских Родов | 🟡 Средний | ✅ Выполнено |
| 12.3 | Убыхское Наследие | 🟢 Низкий | ✅ Выполнено |
---

## 🔬 Фаза 5: Специализированные Темы

### Приоритетная Матрица (Фаза 5)

| # | Тема | Приоритет | Статус |
|---|------|-----------|--------|
| 13.1 | Черкесская Диаспора | 🟡 Средний | ✅ Выполнено |
| 13.2 | Сванский Угол | 🟡 Средний | ✅ Выполнено |
| 13.3 | Хронологический Синтез | 🔴 Высокий | ✅ Выполнено |

---

### 13.1. Черкесская Диаспора — Генетика Мухаджиров

> Скопируй весь блок ниже:

```
Please conduct a comprehensive genetic analysis of the Circassian diaspora.
Focus on publications from 2015-2025 and DNA project data.
Provide full citations with DOI links.

TOPIC: Genetics of the Circassian Diaspora (Muhajirs) - 160 years after the exile

CONTEXT:
In 1864, following the Russian conquest, ~90% of Circassians were exiled to the 
Ottoman Empire. Today, the diaspora (~5-7 million) vastly outnumbers the homeland 
population (~750,000 in Russia). Key diaspora locations:

| Country | Population | Notes |
|---------|------------|-------|
| Turkey | 3-5 million | Largest community |
| Jordan | ~100,000 | Amman guards tradition |
| Syria | ~100,000 | War displacement |
| Israel | ~4,000 | Kfar Kama, Rehaniya |
| Kosovo | ~3,000 | 19th century settlement |

QUESTIONS:
1. **Genetic Preservation:**
   - Has the diaspora maintained the homeland Y-DNA profile?
   - G2a frequencies in Turkey vs Russia Circassians?
   - Evidence of genetic drift in isolated communities?

2. **Admixture Analysis:**
   - Turkish admixture in Anatolian Circassians?
   - Arab admixture in Jordanian community?
   - Balkan admixture in Kosovar Circassians?
   - Quantify: % of autosomal admixture per generation?

3. **Founder Effects:**
   - Did specific clans/tribes dominate certain diaspora regions?
   - Evidence of bottleneck in small communities (Israel, Kosovo)?
   - STR diversity comparison: diaspora vs homeland?

4. **Community-Specific Studies:**
   - Israeli Circassians (Kfar Kama): any published DNA studies?
   - Jordanian Royal Guard Circassians?
   - Turkish "Çerkes köyleri" genetic surveys?

5. **mtDNA vs Y-DNA:**
   - Is there evidence of female-line admixture (local wives)?
   - Y-DNA preservation stronger than autosomal?

6. **Inbreeding/Endogamy:**
   - ROH (Runs of Homozygosity) in diaspora vs homeland?
   - Cousin marriage frequencies in different communities?

KEY DIASPORA COMMUNITIES:
| Community | Country | Tribal Origin | Expected Profile |
|-----------|---------|---------------|------------------|
| Kfar Kama | Israel | Shapsug | G2a dominant |
| Uzunyayla | Turkey | Mixed Adyghe | Diverse |
| Amman | Jordan | Kabardian | G2a + R1a |
| Prizren | Kosovo | Abzakh | G2a |

SOURCES TO CHECK:
- FTDNA Circassian Diaspora projects
- Turkish genetic surveys
- Jordanian/Israeli population studies
- Balkan genetic studies
- Yunusbayev et al. on Caucasus populations

EXPECTED OUTPUT FORMAT:
1. Y-DNA frequency comparison: homeland vs each diaspora community
2. Admixture proportions table by country
3. STR diversity metrics
4. Assessment of genetic preservation
5. Recommendations for future sampling
6. Full reference list with DOIs
```

---

### 13.2. Сванский Угол — G2a1a в Лингвистическом Изоляте

> Скопируй весь блок ниже:

```
Please conduct a comprehensive genetic analysis of the Svan population.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Svan genetics - the G2a1a paradox in a Kartvelian-speaking isolate

CONTEXT:
The Svans inhabit the highest valleys of the Greater Caucasus (Svaneti, Georgia).
They speak Svan, the most divergent Kartvelian language (~3900 years divergence).
Paradoxically, their Y-DNA profile resembles Ossetians (G2a1a), not other Kartvelians.

KNOWN DATA:
| Population | G2a1a | G2a2b | J2 | R1a |
|------------|-------|-------|----|----|
| Svans | ~70% | Low | ~15% | Low |
| Ossetians | ~70% | Low | ~10% | ~15% |
| Mingrelians | ~50%? | Mixed | ~20% | Low |
| Circassians | Low | ~70% | ~15% | ~10% |

THE PARADOX:
- Svans speak Kartvelian (like Georgians, Mingrelians)
- Svans have G2a1a (like Ossetians, Balkars)
- Circassians speak NWC (unrelated) but are both linguistically and genetically distant

QUESTIONS:
1. **G2a1a Subclades:**
   - Which specific G2a1a branches in Svans?
   - Same as Ossetian G2a1a or different?
   - TMRCA of Svan-specific branches?

2. **Isolation Analysis:**
   - ROH (Runs of Homozygosity) levels in Svans?
   - Evidence of extreme founder effects?
   - Effective population size (Ne) estimates?

3. **Linguistic vs Genetic:**
   - Did Svans adopt Kartvelian language from a different genetic population?
   - Or did Kartvelian speakers acquire G2a1a through admixture?
   - Timing of language shift (if any)?

4. **Ancient DNA:**
   - Any aDNA from Svaneti region?
   - Koban samples: are they ancestral to Svans?
   - Continuity from Bronze Age?

5. **Autosomal Profile:**
   - CHG proportion in Svans?
   - Steppe admixture level?
   - PCA position: closer to Georgians or Ossetians?

6. **mtDNA:**
   - Maternal lineages in Svans?
   - Same as other Kartvelians or distinct?

KEY COMPARATIVE QUESTION:
Why do Svans (Kartvelian) and Ossetians (Iranian) share G2a1a,
while Circassians (NWC) and Kartvelians are genetically distant
despite geographic proximity?

SOURCES TO CHECK:
- Georgian biobank studies
- Schurr et al. (2023) on Mingrelians
- Ossetian genetic studies
- Lazaridis et al. (2022) on Southern Arc
- AADR database for Caucasus samples

EXPECTED OUTPUT FORMAT:
1. G2a1a subclade comparison: Svans vs Ossetians vs Koban
2. ROH/IBD analysis if available
3. Autosomal PCA position
4. Historical scenario: how did G2a1a reach Svaneti?
5. Language vs genetics: reconciliation model
6. Full reference list with DOIs
```

---

### 13.3. Хронологический Синтез — Полная База aDNA Кавказа

> Скопируй весь блок ниже:

```
Please compile a comprehensive ancient DNA database for the Caucasus region.
Focus on peer-reviewed publications from 2015-2025.
Provide full citations with DOI links.

TOPIC: Complete chronological synthesis of Caucasus Y-DNA from ancient samples

CONTEXT:
Multiple studies have published ancient DNA from the Caucasus, but data is scattered.
We need a unified timeline showing Y-haplogroup evolution from Paleolithic to Medieval.

TIMELINE GAP ANALYSIS:
| Period | Approximate Date | Cultures | aDNA Status |
|--------|------------------|----------|-------------|
| Paleolithic | 15000-10000 BCE | CHG | ✅ Kotias, Satsurblia |
| Mesolithic | 10000-6000 BCE | ? | ❌ Gap |
| Neolithic | 6000-4000 BCE | Shulaveri-Shomu | ⚠️ Limited |
| Chalcolithic | 4000-3000 BCE | Maykop, Novosvobodnaya | ✅ Good coverage |
| Early Bronze | 3000-2000 BCE | Kura-Araxes | ⚠️ Limited |
| Middle Bronze | 2000-1500 BCE | Dolmen, Trialeti | ⚠️ Some samples |
| Late Bronze | 1500-1000 BCE | Late Dolmen | ✅ I2051 |
| Iron Age | 1000 BCE - 0 CE | Koban, Scythian | ⚠️ Limited |
| Classical | 0 - 500 CE | Meotian, Sarmatian | ⚠️ Limited |
| Medieval | 500 - 1500 CE | Alan, Saltovo | ✅ Good coverage |

QUESTIONS:
1. **Complete Sample List:**
   - List ALL published Y-haplogroup results from Caucasus aDNA
   - Include: Sample ID, Site, Date, Culture, Y-Hg, mtDNA, Source

2. **Culture-by-Culture Breakdown:**
   a) CHG (Kotias, Satsurblia): What Y-DNA?
   b) Maykop/Novosvobodnaya: J2a, G2a, L ratios?
   c) Kura-Araxes: J1, J2, G proportions?
   d) Dolmen culture: J2a-L283, other?
   e) Koban culture: G2a1a confirmed, what else?
   f) Saltovo-Mayaki: Full haplogroup spectrum?

3. **Transition Points:**
   - When does J2a decline and G2a rise?
   - When does R1a/R1b appear in Caucasus?
   - First evidence of Steppe admixture in aDNA?

4. **Modern Continuity:**
   - Which ancient samples match modern populations?
   - Direct ancestral links (IBD) if detected?

5. **Gaps and Future Priorities:**
   - Which periods/regions need more sampling?
   - Meotian aDNA: status?
   - Abkhazian aDNA: any samples?

REQUIRED OUTPUT FORMAT:
Create a MASTER TABLE with columns:
| Sample ID | Site | Country | Culture | Date (BCE/CE) | Y-Hg | Y-Subclade | mtDNA | Modern Match | Source |

Sort by chronological order.

SOURCES TO CHECK:
- Wang et al. (2019) Nature
- Lazaridis et al. (2022) Cell
- Harney et al. - Koban samples
- Gerber et al. (2024) - Avars
- Andreeva et al. (2025) - Scythians
- AADR database complete
- Allen Ancient DNA Resource

EXPECTED OUTPUT FORMAT:
1. Master table of ALL Caucasus aDNA samples with Y-DNA
2. Chronological summary by period
3. Haplogroup frequency charts by culture
4. Gap analysis with priorities
5. Modern population matches
6. Full reference list with DOIs
```

---

## 🔬 Фаза 6: Специальные Исследования

### Приоритетная Матрица (Фаза 6)

| # | Тема | Приоритет | Статус |
|---|------|-----------|--------|
| 14.1 | Греческие Колонии | 🟡 Средний | ✅ Готово |
| 14.2 | Шапсугский Феномен | 🔴 Высокий | ✅ Готово |
| 14.3 | Дагестанские Границы | 🟡 Средний | ✅ Готово |
| 14.4 | Золотоордынское Влияние | 🔴 Высокий | ✅ Готово |
| 14.5 | Генетические Болезни Кавказа | 🟡 Средний | ✅ Готово |

---

### 14.1. Греческие Колонии — Средиземноморский След на Кавказе

> Скопируй весь блок ниже:

```
Please conduct a genetic analysis of Greek colonial impact on the Circassian coast.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Genetic legacy of Greek, Roman, and Byzantine colonies on the Northwest Caucasus coast

CONTEXT:
The Northwest Caucasus coast hosted numerous Greek colonies from ~600 BCE to ~400 CE:

| Colony | Modern Location | Period | Notes |
|--------|-----------------|--------|-------|
| Dioscurias | Sukhumi | 6th c BCE - 1st c CE | Major port |
| Pitiunt | Pitsunda | 4th c BCE - 6th c CE | Fortress |
| Phanagoria | Taman | 6th c BCE - 10th c CE | Bosporan capital |
| Gorgippia | Anapa | 5th c BCE - 3rd c CE | Greek polis |
| Hermonassa | Taman | 6th c BCE | Colony |

QUESTIONS:
1. **Mediterranean Haplogroups:**
   - E1b1b (E-M35) frequencies in coastal populations?
   - J2a Mediterranean subclades?
   - T1a presence?
   - Any Greek-specific SNPs identified?

2. **Comparison Coastal vs Inland:**
   - Do Shapsugs/Natukhai (coastal) differ from Kabardians (inland)?
   - Higher Mediterranean admixture on the coast?
   - Quantify: % difference in autosomal "Mediterranean" component?

3. **Ancient DNA from Colonies:**
   - Any aDNA from Phanagoria, Gorgippia?
   - Comparison with Greek colonial DNA from Crimea?
   - Bosporan Kingdom samples?

4. **Genetic Trace of Byzantium:**
   - Dioscurias was Byzantine fortress until 6th c CE
   - Any Byzantine genetic signature in Abkhaz?

5. **Jewish Component:**
   - Phanagoria had Jewish community (archaeological evidence)
   - Any genetic trace in modern populations?

EXPECTED OUTPUT FORMAT:
1. Y-DNA frequency comparison: coastal vs inland Circassians
2. Autosomal Mediterranean component analysis
3. List of aDNA samples from Black Sea colonies
4. Historical scenario of colonial integration
5. Assessment: how much Greek DNA remains?
6. Full reference list with DOIs
```

---

### 14.2. Шапсугский Феномен — Экстремальный Founder Effect

> Скопируй весь блок ниже:

```
Please conduct a genetic analysis of the extreme founder effect in Shapsugs.
Focus on publications from 2015-2025 and FTDNA data.
Provide full citations with DOI links.

TOPIC: Why do Shapsugs have up to 81% G2a? Extreme founder effect analysis

CONTEXT:
The Shapsugs are a Western Circassian subgroup with extraordinary genetic homogeneity:

| Population | G2a Frequency | Other |
|------------|---------------|-------|
| Shapsugs | **81%** | Minimal diversity |
| Western Circassians | 60-70% | Some diversity |
| Kabardians | 40-50% | More diverse |
| Abkhaz | 50-60% | Moderate |

This level of homogeneity is UNUSUAL even for Circassians.

QUESTIONS:
1. **Which G2a Subclade?**
   - Is it one specific terminal SNP?
   - Or multiple G2a branches?
   - G-P303 (YY1215) specifically?
   - TMRCA of the dominant lineage?

2. **Bottleneck Analysis:**
   - When did the bottleneck occur?
   - Was it 4.2ky event, Medieval period, or 19th century?
   - Effective population size (Ne) estimates?

3. **Geographic Isolation:**
   - Did mountain valleys create genetic islands?
   - Comparison between coastal Shapsugs and mountain Shapsugs?

4. **ROH Analysis:**
   - Runs of Homozygosity in Shapsugs?
   - Comparison with other populations?
   - Evidence of inbreeding?

5. **Medical Implications:**
   - Known founder mutations?
   - Genetic disease prevalence?
   - Recommendations for genetic screening?

6. **STR Diversity:**
   - YSTR diversity comparison with other Circassians?
   - Evidence of recent expansion vs ancient bottleneck?

KEY DATA TO GATHER:
| Parameter | Expected Finding |
|-----------|------------------|
| Dominant SNP | G-P303 or subclade? |
| TMRCA | ~2000-4000 years? |
| ROH level | Higher than outbred populations |
| Ne | Very low (founder effect) |

SOURCES TO CHECK:
- FTDNA Circassian projects
- Balanovsky et al. studies
- ROH analyses in Caucasus populations
- Genetic disease studies in Adygea

EXPECTED OUTPUT FORMAT:
1. G2a subclade breakdown for Shapsugs
2. TMRCA and bottleneck timing estimate
3. ROH comparison with other populations
4. Ne (effective population size) estimate
5. Medical genetics implications
6. Full reference list with DOIs
```

---

### 14.3. Дагестанские Границы — Генетический Барьер NWC vs NEC

> Скопируй весь блок ниже:

```
Please conduct a comparative genetic analysis of the NWC-NEC boundary.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Genetic boundary between Northwest and Northeast Caucasian speakers

CONTEXT:
The Caucasus hosts two unrelated language families:
- Northwest Caucasian (NWC): Circassians, Abkhaz, Ubykh
- Northeast Caucasian (NEC): Chechens, Ingush, Avars, Dargins, Lezgins

Do the linguistic families correspond to genetic boundaries?

KNOWN Y-DNA PATTERNS:
| Population | Dominant Y-DNA | J1 | J2 | G2a | R1a |
|------------|----------------|----|----|-----|-----|
| Circassians | **G2a** | 5% | 15% | 50% | 10% |
| Abkhaz | **G2a** | 5% | 10% | 60% | 5% |
| Chechens | **J1** + J2 | 30% | 25% | 5% | 5% |
| Ingush | **J2** | 20% | 35% | 5% | 5% |
| Avars | **J1** | 40%+ | 20% | <5% | 15% |

QUESTIONS:
1. **Genetic Distance:**
   - Fst between Circassians and Chechens?
   - Is it greater than between Circassians and Georgians?
   - PCA visualization of the boundary?

2. **Boundary Location:**
   - Where exactly is the genetic boundary?
   - Does it match the linguistic divide?
   - Any transitional populations (Balkars?)

3. **IBD Sharing:**
   - Do NWC speakers share IBD segments with NEC speakers?
   - Or is there no recent common ancestry?

4. **J1 Distribution:**
   - J1-Z1842 is "NEC signature"
   - Its presence in Adyghe (5%) = ancient substrate or recent admixture?
   - Direction of gene flow?

5. **G2a Boundary:**
   - Does G2a "stop" at the NWC/NEC border?
   - Any G2a in Dagestan?
   - Chechens have ~5% G2a — which subclades?

6. **Origins:**
   - Were NWC and NEC speakers always separate?
   - Or did they differentiate from common Caucasus population?
   - When did the genetic divide form?

COMPARATIVE TABLE TO FILL:
| Metric | NWC (Circassians) | NEC (Chechens) |
|--------|-------------------|-----------------|
| Dominant Y-DNA | G2a (~50%) | J1+J2 (~55%) |
| CHG proportion | ~60-70% | ~?% |
| Steppe | ~15-20% | ~?% |
| Fst distance | - | ? |

SOURCES TO CHECK:
- Balanovsky on Caucasus Y-DNA
- Yunusbayev et al. (2012)
- Kushniarevich et al. on genetic structure
- Lazaridis et al. (2022) on Southern Arc

EXPECTED OUTPUT FORMAT:
1. Y-DNA frequency comparison table
2. Autosomal component comparison
3. Fst/genetic distance matrix
4. PCA visualization description
5. IBD analysis if available
6. Historical scenario: when did divide form?
7. Full reference list with DOIs
```

---

### 14.4. Золотоордынское Влияние — Монгольский и Тюркский Генетический След

> Скопируй весь блок ниже:

```
Please conduct a genetic analysis of Mongol and Turkic impact on Circassian populations.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Genetic legacy of the Golden Horde and Crimean Khanate on Northwest Caucasian populations

CONTEXT:
The Mongol invasion (1237-1240 CE) and subsequent Golden Horde period (~1240-1502 CE) 
profoundly affected the political history of the North Caucasus:

| Period | Event | Potential Genetic Impact |
|--------|-------|--------------------------|
| 1237-1240 | Mongol invasion | Possible bottleneck |
| 1240-1380 | Golden Horde domination | Turkic/Mongol admixture? |
| 1380-1502 | Horde fragmentation | Kabardian expansion |
| 1502-1783 | Crimean Khanate influence | Tatar admixture? |

QUESTIONS:
1. **East Asian Markers:**
   - Any C2-M217 (Mongolic marker) in Circassians?
   - N1a (Uralic/Siberian) frequencies?
   - Haplogroup Q frequencies?
   - Any genomic segments of East Asian origin?

2. **Turkic Markers:**
   - R1a-Z93 "Steppe" subclade distribution?
   - Comparison with Crimean Tatars, Balkars, Kumyks?
   - Direction of gene flow: into or out of Circassians?

3. **Population Bottleneck:**
   - Evidence of ~1240 CE bottleneck in Circassian aDNA?
   - TMRCA of major lineages — do any date to 1200-1400 CE?
   - Ne estimates for post-Mongol period?

4. **Kabardian Expansion:**
   - Kabardians expanded eastward after Horde collapse
   - Genetic evidence of founder effect in eastern Kabardian groups?
   - Admixture with remnant Alans during expansion?

5. **Crimean Khanate Period:**
   - Circassian slaves (Mamluks) exported to Egypt
   - Reverse gene flow from Crimea to Circassia?
   - Genetic traces in modern Kabardians, Beslenei?

KEY MARKERS TO CHECK:
| Haplogroup | Association | Expected in Circassians? |
|------------|-------------|--------------------------|
| C2-M217 | Mongolic | Very low (<1%?) |
| N1a | Ural-Siberian | Low |
| Q-M242 | Central Asian | 1-5% |
| R1a-Z93 | Turkic Steppe | 5-15% |

SOURCES TO CHECK:
- Yunusbayev et al. on Caucasus admixture
- Zhivotovsky et al. on Mongol genetic legacy
- Zhabagin et al. on steppe signatures
- Ancient DNA from Golden Horde burials

EXPECTED OUTPUT FORMAT:
1. East Asian haplogroup frequencies in Circassians
2. Autosomal East Asian / Turkic component estimates
3. Timeline of admixture events
4. Bottleneck evidence analysis
5. Comparison: Circassians vs neighboring Turkic peoples
6. Full reference list with DOIs
```

---

### 14.5. Генетические Болезни Кавказа — Founder Mutations и Медицинская Генетика

> Скопируй весь блок ниже:

```
Please conduct a medical genetics analysis of founder mutations in Caucasus populations.
Focus on publications from 2015-2025 and medical genetics databases.
Provide full citations with DOI links.

TOPIC: Founder mutations and genetic disease prevalence in isolated Caucasian populations

CONTEXT:
Isolated populations with strong founder effects often harbor specific genetic diseases 
at elevated frequencies. The Caucasus, with its extreme genetic isolation (especially 
among Shapsugs, Abkhaz mountain communities), may have similar patterns.

KNOWN FOUNDER EFFECTS:
| Population | Key Lineage | Evidence |
|------------|-------------|----------|
| Shapsugs | G2a (81-86%) | Extreme bottleneck |
| Ossetians | G2a1 (~70%) | Single lineage dominance |
| Isolated Abkhaz | G2a | Mountain valley isolation |
| Ingush | J2 (~35%) | Strong founder |

QUESTIONS:
1. **Known Founder Mutations:**
   - Any documented founder mutations in Circassians?
   - Comparison with Ashkenazi Jewish, Finnish founder mutations?
   - ClinVar/OMIM entries for Caucasus populations?

2. **Elevated Disease Frequencies:**
   - Any rare diseases at elevated frequencies in Adygea, Abkhazia?
   - Metabolic disorders (similar to Finnish disease heritage)?
   - Neurological conditions?
   - Hemoglobinopathies (Mediterranean connection)?

3. **ROH and Homozygosity Burden:**
   - Consequences of elevated ROH in Shapsugs?
   - FROH (inbreeding coefficient) estimates?
   - Correlation with recessive disease prevalence?

4. **Consanguinity Patterns:**
   - Documented consanguineous marriage rates?
   - Clan endogamy effects?
   - Pre-1864 vs post-deportation patterns?

5. **Screening Recommendations:**
   - Do genetic counselors recommend specific panels for Caucasus patients?
   - Carrier screening for known mutations?
   - Any regional genetic screening programs?

EXPECTED OUTPUT FORMAT:
1. List of known founder mutations in Caucasus populations
2. Disease frequency comparison table
3. ROH/FROH statistics by population
4. Consanguinity prevalence data
5. Medical/clinical recommendations
6. Full reference list with DOIs

NOTE: This research has practical medical implications for genetic counseling 
of Circassian diaspora worldwide.
```

---

## 🔬 Фаза 7: Древняя ДНК — Расширенный Анализ

### Приоритетная Матрица (Фаза 7)

| # | Тема | Приоритет | Статус |
|---|------|-----------|--------|
| 17.1 | Меотская aDNA | 🔴 Высокий | ✅ Готово |
| 17.2 | Зихская aDNA | 🔴 Высокий | ✅ Готово |
| 17.3 | Скифы vs Черкесы | 🟡 Средний | ✅ Готово |
| 17.4 | Хазарский Каганат | 🟡 Средний | ✅ Готово |

---

## 🔬 Фаза 8: Детализация Субкладов

### Приоритетная Матрица (Фаза 8)

| # | Тема | Приоритет | Статус |
|---|------|-----------|--------|
| 18.1 | J-PH1795 и подветви | 🔴 Высокий | ✅ Готово |
| 18.2 | C-BY154208 Монгольская ветвь | 🔴 Высокий | ✅ Готово |

---

### 18.2. C-BY154208 — Монгольско-Маньчжурская Ветвь Гаплогруппы C

> Скопируй весь блок ниже:

```
Please conduct a comprehensive analysis of haplogroup C-BY154208 and its relationship 
to the larger C-F3796 branch. Focus ESPECIALLY on Chinese and Mongolian sources.
Provide full citations with DOI links where available.

TOPIC: Detailed phylogenetic analysis of C-BY154208 with focus on East Asian distribution 
and potential Caucasus connections

PHYLOGENETIC PATH:
C-M217 > C-L1373 > C-F3447 > C-F1699 > C-F4032 > C-FGC16273 > C-M504 > C-F3618 > C-Y11121 > **C-BY154208**

KEY DATA FROM MULTIPLE SOURCES:

## YFull Data:
- **C-BY154208:** TMRCA ~2400 ybp (YFull) / 2795 ybp (TheYTree)
- **Defining SNPs:** BY154208 + 10 SNPs
- **Downstream clades:**
  - C-Y170660 (formed 2795 ybp, TMRCA 1790 ybp)
  - C-Y170537 (formed 1790 ybp, TMRCA 1500 ybp)
  - C-Y215105 (formed 1790 ybp, TMRCA 1355 ybp)
  - C-Y205287 (formed 1355 ybp, TMRCA 1355 ybp)

## TheYTree Samples:
| Sample ID | Surname | Location | Ethnicity | mtDNA |
|-----------|---------|----------|-----------|-------|
| AU61939 | Dong | Liaocheng, Shandong, Xin County | Han Chinese | N9a10 |
| AU61709 | Liu | Inner Mongolia, Horqin Right Front Banner | Han Chinese | F2a6 |
| AU63754 | Su | Hebei, Baoding | Manchu | M8a2'3 |

## 23mofang (Chinese Database) Data:
- **C-BY154208:** Formed 3200 years ago, 17 relatives
- **Downstream structure:**
  - C-ZQ1012 (formed 1130 ybp)
  - C-MF204213 (formed 2590 ybp, 17 relatives)
    - C-MF380228
    - C-MF204209 (formed 2080 ybp, 17 relatives)
      - C-MF380202 (formed 800 ybp)
      - C-MF204214 (formed 1730 ybp, 6 relatives)
      - C-MF378936 (formed 1640 ybp, 8 relatives)

## Key Samples from 23mofang:
| Sample | Surname | Ethnicity | Location |
|--------|---------|-----------|----------|
| C-MF380220 | Yang | Han | Zhangdian District, Zibo, Shandong |
| C-MF204210 | Liu | Han | Inner Mongolia, Xing'an League |
| C-MF380199 | Dong | Han | Liaocheng, Shandong, Xin County |
| C-MF442282 | Li | Han | Shanghai, Baoshan |
| C-MF402594 | Su | **Manchu** | Hebei, Baoding |
| **C-MF378954** | **Aisin Gioro** | **Manchu** | Jilin, Tonghua, Ji'an |
| **C-MF380183** | **Ilgen Gioro** | **Manchu** | Heilongjiang, Harbin, Shuangcheng |

CRITICAL OBSERVATION: 
**Aisin Gioro (愛新覺羅)** — the imperial clan of the Qing Dynasty!
**Ilgen Gioro** — a branch of the Manchu royal lineage!
This suggests C-BY154208 may be connected to Manchu nobility.

QUESTIONS:

1. **Relationship to C-F3796:**
   - What is the phylogenetic distance between BY154208 and F3796?
   - Are they sister clades or nested?
   - What is the TMRCA of their common ancestor?

2. **Mongolic vs Manchu-Tungusic:**
   - C-M217 is often called the "Mongolic marker"
   - But samples show Han Chinese, Manchu, not Mongol ethnicity
   - Is BY154208 specifically Manchu-Tungusic rather than Mongolic?

3. **Qing Dynasty Connection:**
   - Aisin Gioro samples in this clade!
   - Is this the genetic lineage of the Qing emperors?
   - Historical implications?

4. **Shandong-Liaoning Corridor:**
   - Multiple samples from Shandong (Dong, Yang, Liu)
   - Is this Han assimilation of Manchu lineages?
   - Or ancient migration pattern?

5. **TMRCA Discrepancy:**
   - YFull: ~2400 ybp
   - TheYTree: ~2795 ybp  
   - 23mofang: ~3200 ybp
   - Which is most accurate? Why the difference?

6. **Caucasus Connection (if any):**
   - Is there ANY C-BY154208 in Caucasus databases?
   - C-M217 is 14-18% in Nogais (steppe neighbors of Circassians)
   - But <2% in Circassians themselves
   - Could BY154208 represent post-Mongol introgression?

SOURCES TO CHECK (prioritize Chinese):
- 23mofang (魔方祖源): https://www.23mofang.com/ancestry/ytree/C-BY154208
- TheYTree: https://www.theytree.com/tree/C-BY154208
- YFull: https://www.yfull.com/tree/C-BY154208/
- WeGene (微基因) haplogroup database
- Chinese academic papers on C-M217 distribution
- Manchu genetic studies (especially imperial lineage)
- Zhabagin et al. on Mongol genetic legacy

EXPECTED OUTPUT FORMAT:
1. Complete phylogenetic tree from C-M217 to terminal BY154208 subclades
2. TMRCA reconciliation across databases
3. Ethnic distribution analysis (Manchu vs Han vs Mongol)
4. Historical scenario: Qing Dynasty genetic legacy?
5. Relationship to C-F3796 clarified
6. Any Caucasus samples (AADNA relevance)
7. Full reference list with DOIs (Chinese sources welcome!)

NOTE: This haplogroup is important for understanding potential Mongol/Manchu 
genetic traces in Caucasus populations, even if BY154208 itself is not present there.
```

---

### 18.1. J-PH1795 — Детальный Анализ Кавказских Ветвей

> Скопируй весь блок ниже:

```
Please conduct a comprehensive analysis of haplogroup J-PH1795 and its downstream subclades 
where Adygo-Abkhaz samples are present.
Focus on YFull tree data, published studies, and FTDNA projects.
Provide full citations with DOI links where available.

TOPIC: Detailed phylogenetic and demographic analysis of J-PH1795 with focus on Caucasus samples

CONTEXT FROM YFULL TREE:
J-PH1795 is a branch of J2a2a (J-L581):
- **Parent haplogroup:** J-Y164552
- **Defining SNPs:** BY128998, PH3085, PH1984 +75 SNPs
- **TMRCA (Formation):** ~7600 ybp
- **TMRCA (Diversification):** ~2000 ybp

IDENTIFIED CIRCASSIAN/ABKHAZ SAMPLES ON YFULL:
| Sample ID | Location | Ethnicity | Subclade |
|-----------|----------|-----------|----------|
| YF078875 | GEO [GE-AB] | Abkhaz (abk) | J-FT147742 |
| YF143372 | RUS [RU-KB] | Adyghe (ady) | J-BY114993 |
| YF081111 | RUS [RU-KB] | Unknown | J-BY114993 |
| YF072143 | RUS [RU-KB] | Karachay (krc) | J-BY114993 |
| YF070826 | RUS [RU-KB] | Kabardian (kbd) | J-PH2466 |

KEY SUBCLADES TO ANALYZE:
1. **J-FT147742** (formed 1550 ybp, TMRCA 1450 ybp)
   - Includes: Abkhaz (YF078875), Oman, China, Kazakhstan
   - Question: Connection between Abkhaz and Omani samples?

2. **J-BY114993** (formed 1950 ybp, TMRCA 1950 ybp)
   - Ancient samples: RISE602 (RU-AL, ancient)
   - Modern: Multiple RU-KB (Kabardino-Balkaria), China
   - Contains Adyghe and Karachay samples
   - Key question: Is RISE602 linked to proto-Circassians?

3. **J-PH2466** (formed 1950 ybp, TMRCA 1550 ybp)
   - Includes: China (Shaanxi), Kabardian (YF070826), Uyghur (HGDP)
   - Silk Road connection?

QUESTIONS:
1. **Phylogenetic Structure:**
   - What is the relationship between J-FT147742, J-BY114993, J-PH2466?
   - Which subclade is most specifically Caucasian?
   - Are there "purely Caucasian" downstream SNPs?

2. **Ancient DNA:**
   - RISE602 and RISE504 appear in this branch - what cultures?
   - Any Bronze Age Caucasus samples?
   - Connection to Koban/Maykop?

3. **Distribution Pattern:**
   - Why are Caucasus samples mixed with China/Oman?
   - Ancient trade routes (Silk Road)?
   - Or parallel lineages from a common Central Asian ancestor?

4. **TMRCA Analysis:**
   - J-BY114993 TMRCA ~1950 ybp = ~0 CE / start of Common Era
   - Historical event correlations?
   - Roman-Parthian trade? Sarmatian expansion?

5. **Comparison with Other J2 on Caucasus:**
   - How does J-PH1795 compare to J-M67, J-SK1313?
   - Is J-PH1795 "autochthonous" or "intrusive"?
   - Frequency estimates in Adyghe/Abkhaz populations?

SOURCES TO CHECK:
- YFull tree: https://www.yfull.com/tree/J-PH1795/
- FTDNA J2 Project haplogroup pages
- Reich Lab aDNA (RISE samples)
- Wang et al. (2019) Caucasus Bronze Age
- Lazaridis et al. Southern Arc

EXPECTED OUTPUT FORMAT:
1. Complete phylogenetic tree from J-PH1795 to terminal Caucasian subclades
2. TMRCA table for all relevant branches
3. Distribution map description (Caucasus + non-Caucasus)
4. Ancient DNA context (RISE602, RISE504)
5. Historical scenario: When and how did J-PH1795 reach the Caucasus?
6. Comparison with other J2 subclades on the Caucasus
7. Frequency estimates if available
8. Full reference list with DOIs
```

---

### 17.1. Меотская Древняя ДНК — Синды, Керкеты, Тореаты

> Скопируй весь блок ниже:

```
Please search for ancient DNA studies from Meotian culture sites.
Focus on publications from 2018-2025 and unpublished datasets.
Provide full citations with DOI links.

TOPIC: Ancient DNA from Meotian culture (Sindica, Kerkets, Toreats) — genetic precursors to Circassians?

CONTEXT:
The Maeotae (Меоты) were tribes inhabiting the eastern Black Sea coast and Kuban region 
during the 1st millennium BCE to early 1st millennium CE:

| Tribe | Location | Period | Archaeological Sites |
|-------|----------|--------|---------------------|
| Sindi (Синды) | Taman Peninsula | 6th c BCE - 1st c CE | Semibratnee, Gorgippia |
| Kerketae (Керкеты) | Coastal | 5th c BCE - 2nd c CE | Raevskoe |
| Toreatae (Тореаты) | Inland | 4th c BCE - 1st c CE | Various |
| Dandarii (Дандарии) | Kuban | Same period | Ust-Labinsk |

QUESTIONS:
1. **Published aDNA Samples:**
   - Any Y-DNA/mtDNA from Meotian burials?
   - Which sites have been sampled?
   - Are any samples in AADR/ENA databases?

2. **Expected Genetic Profile:**
   - If Meotae were proto-Circassians, expect high G2a
   - If Greek-influenced, expect J2a, E1b1b
   - If Scythian-influenced, expect R1a-Z93

3. **Comparison with Modern Circassians:**
   - Would Meotian aDNA cluster with modern Shapsugs/Natukhai?
   - Or with Greeks/Sarmatians?

4. **Archaeological Context:**
   - Burial practices: kurgan vs flat grave
   - Inventory: Greek imports vs local production
   - Social structure implications

5. **Gap Analysis:**
   - Why is there little/no Meotian aDNA published?
   - Which sites should be prioritized for sampling?

KEY SITES TO CHECK:
| Site | Region | Culture | aDNA Status? |
|------|--------|---------|--------------|
| Semibratnee Kurgan | Taman | Sindian | ? |
| Elizavetinskaya | Kuban | Meotian | ? |
| Ust-Labinsk | Kuban | Meotian | ? |
| Gorgippia necropolis | Anapa | Greek-Sindian | ? |

EXPECTED OUTPUT FORMAT:
1. List of ALL published Meotian aDNA samples
2. Summary of unpublished/ongoing projects
3. Genetic profile if available
4. Comparison with modern Circassians
5. Recommendations for future sampling
6. Full reference list with DOIs
```

---

### 17.2. Зихская Древняя ДНК — Средневековые Предки Черкесов

> Скопируй весь блок ниже:

```
Please search for ancient DNA from medieval Zygian/Kasogian sites.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Ancient DNA from medieval Zikhia and Kasog period (6th-15th century CE)

CONTEXT:
The Zygii (Зихи) and later Kasogs (Касоги) are the direct historical predecessors 
of modern Circassians, documented by Byzantine, Arab, and Russian sources:

| Period | Name in Sources | Location | Key Events |
|--------|-----------------|----------|------------|
| 1-6th c CE | Zygii | Coastal | Byzantine contacts |
| 6-10th c CE | Zikhia | Coast + foothills | Christianization |
| 10-13th c CE | Kasogs | Expanded | Contact with Rus' |
| 13-15th c CE | Circassians | Expanded | Mongol period |

QUESTIONS:
1. **Published Medieval aDNA:**
   - Any samples from Zygian/Kasog period?
   - Christian cemetery aDNA from Alania-Zikhia border?
   - Byzantine fortress garrisons?

2. **Expected Profile:**
   - Should see high G2a (L1264, P303)
   - Lower diversity than Bronze Age (founder effect ongoing)
   - Minimal steppe admixture if isolation maintained

3. **Comparison:**
   - Medieval Zygians vs Bronze Age Dolmen culture?
   - Medieval Zygians vs modern Shapsugs?
   - Evidence of continuity or disruption?

4. **Critical Transition:**
   - aDNA from Mongol invasion period (1237-1240)?
   - Before/after genetic comparison?

5. **Archaeological Sites:**
   - Christian churches on the coast
   - Medieval fortresses (Anakopia, Tsebelda)
   - Burial grounds in Shapsugia

SOURCES TO CHECK:
- Korobov et al. on Alanic-Zygian border
- Byzantine archaeological projects in Abkhazia
- Medieval Adygea excavations

EXPECTED OUTPUT FORMAT:
1. List of ALL medieval Caucasus aDNA samples
2. Genetic profile comparison by period
3. Continuity evidence: Zygii → Circassians
4. Mongol period impact assessment
5. Full reference list with DOIs
```

---

### 17.3. Скифы и Сарматы vs Черкесы — Степной Контакт

> Скопируй весь блок ниже:

```
Please analyze the genetic relationship between Scythians/Sarmatians and Circassians.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Did Scythians and Sarmatians contribute to Circassian ancestry?

CONTEXT:
Scythian and Sarmatian cultures dominated the steppes north of the Caucasus:

| Culture | Period | Core Region | Nearest to Circassians |
|---------|--------|-------------|------------------------|
| Scythians | 7th-3rd c BCE | Pontic Steppe | Kuban steppes |
| Sarmatians | 4th c BCE-4th c CE | Volga-Don | Terek-Kuban |
| Alans | 1st-13th c CE | North Caucasus | Direct neighbors |

QUESTIONS:
1. **Scythian-Circassian Contact:**
   - Did Scythians penetrate into mountain valleys?
   - Any G2a in Scythian samples?
   - Any R1a-Z93 transfer to Circassians?

2. **Sarmatian Influence:**
   - Sarmatian aDNA profiles (typically R1a-Z93, R1b-Z2103, J2)
   - Did Sarmatian women marry into Circassian tribes?
   - mtDNA exchange evidence?

3. **Physical Barrier:**
   - Did mountains block steppe gene flow?
   - Compare: Kuban steppe samples vs Kuban mountain samples

4. **R1a-Z93 in Circassians:**
   - Modern frequency: ~5-10%
   - Is this Scythian/Sarmatian legacy?
   - Or older Bronze Age Steppe component?

5. **Autosomal Evidence:**
   - Steppe ancestry in Circassians: how much?
   - Bronze Age Steppe vs Iron Age Steppe?

KEY SAMPLES TO ANALYZE:
| Sample | Culture | Y-DNA | Relevance |
|--------|---------|-------|-----------|
| Scythian Ak-Alakha | Scythian | R1a | Steppe marker |
| Sarmatian samples | Sarmatian | R1a-Z93, J2 | Comparison |
| Circassian modern | - | G2a, R1a | Target |

SOURCES TO CHECK:
- Krzewińska et al. (2018) on Scythians
- Unterländer et al. on Sarmatians
- Wang et al. (2019) on Steppe Maykop

EXPECTED OUTPUT FORMAT:
1. Y-DNA comparison: Scythians vs Circassians
2. Autosomal Steppe component quantification
3. Timeline of potential admixture events
4. Barrier effect assessment
5. Full reference list with DOIs
```

---

### 17.4. Хазарский Каганат — Кавказский Компонент

> Скопируй весь блок ниже:

```
Please analyze the Caucasian genetic component in the Khazar Khaganate.
Focus on publications from 2018-2025 and ancient DNA from Khazar sites.
Provide full citations with DOI links.

TOPIC: Caucasian (Circassian/Alanian) genetic component in the Khazar Khaganate

CONTEXT:
The Khazar Khaganate (650-969 CE) was a multi-ethnic empire north of the Caucasus.
Sample DA190 from Salto-Mayaki culture shows Caucasian ancestry:

| Sample | Site | Date | Y-DNA | Significance |
|--------|------|------|-------|--------------|
| DA190 | Belgorod | 687 CE | G-FGC693 | Caucasian in Khazaria! |
| Other Khazar samples | Various | 7-10th c | Mixed | Diverse empire |

QUESTIONS:
1. **Caucasian Component in Khazars:**
   - How many Khazar samples show G2a or J2?
   - Was there a "Caucasian elite" in Khazaria?
   - Or Caucasian slaves/mercenaries?

2. **DA190 Analysis:**
   - G-FGC693 is Caucasian subclade
   - Where does it fit in modern Circassian tree?
   - Was this person Circassian, Alanian, or other?

3. **Direction of Gene Flow:**
   - Khazar → Caucasus admixture?
   - Caucasus → Khazar admixture?
   - Both directions?

4. **Trade and Military:**
   - Alanian cavalry served Khazars
   - Caucasian merchants in Atil/Samandar
   - Genetic traces of these connections?

5. **Post-Khazar Period:**
   - Where did Caucasian-origin Khazars go?
   - Return to Caucasus? Assimilate into Rus?

SAMPLES TO CHECK:
- All Salto-Mayaki culture aDNA
- Atil excavation samples (if any)
- Khazar fortress samples

SOURCES TO CHECK:
- Flegontov et al. on Medieval Khazars
- Csáky et al. on Avar-Khazar transition
- DA190 original publication

EXPECTED OUTPUT FORMAT:
1. List of ALL Khazar aDNA with Caucasian affinity
2. G2a frequency in Khazar dataset
3. Subclade analysis (which specific G2a/J2 branches?)
4. Historical scenario reconstruction
5. Comparison with modern Circassian/Ossetian lineages
6. Full reference list with DOIs
```

---

### 12.1. Абхазы vs Адыги — Генетические Различия Родственных Народов

> Скопируй весь блок ниже:

```
Please conduct a comparative genetic analysis of Abkhazians vs Circassians.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Genetic differences between Abkhazians and Adyghe - linguistic cousins with distinct profiles

CONTEXT:
Abkhazians and Circassians (Adyghe) speak closely related Northwest Caucasian languages.
Linguistically, they diverged ~3000-4000 years ago. But are they genetically similar?

KNOWN DATA:
| Population | G2a | J2 | R1a | Other |
|------------|-----|----|----|-------|
| Abkhazians | 56-70% | 10-15% | 5-8% | Low diversity |
| Adyghe | 40-50% | 15-20% | 5-10% | Higher diversity |
| Abazins | ~60% | ~15% | ~10% | Similar to Abkhaz |

KEY DIFFERENCES TO INVESTIGATE:
1. **G2a Subclade Composition:**
   - Do Abkhaz and Adyghe have the SAME G2a subclades?
   - Or did they branch before L1264 split?

2. **J2a vs J2b:**
   - J2a (Maykop) vs J2b-L283 (Dolmen/Koban)
   - Different ratios in Abkhaz vs Adyghe?

3. **Autosomal Differences:**
   - CHG/ANF/Steppe proportions comparison
   - PCA position: do they cluster together?

4. **mtDNA Comparison:**
   - Same maternal lineages or divergent?
   - Evidence of geographic isolation?

QUESTIONS:
1. **Subclade Resolution:**
   - Which G2a subclades in Abkhaz? (FGC21495, Z44222, other?)
   - Which G2a subclades in Adyghe?
   - When did they diverge?

2. **Geographic Barrier:**
   - Did Greater Caucasus range isolate Abkhaz from Adyghe?
   - When did gene flow stop between groups?

3. **Colchian Connection:**
   - Abkhaz live in ancient Colchis region
   - Are they genetically closer to Mingrelians than to Adyghe?

4. **Greek Colonial Impact:**
   - Abkhaz coast had Greek colonies (Dioscurias)
   - Any Mediterranean admixture in Abkhaz absent in Adyghe?

5. **Modern vs Ancient:**
   - Any aDNA from Abkhazia specifically?
   - How has the profile changed over time?

SOURCES TO CHECK:
- Yunusbayev et al. (2012) - Caucasus study
- Balanovsky et al. - Russian genetic surveys
- FTDNA G2a project by region
- Georgian biobank (for Mingrelian comparison)

EXPECTED OUTPUT FORMAT:
1. Side-by-side Y-DNA frequency comparison
2. G2a subclade breakdown for each group
3. Autosomal comparison (PCA, ADMIXTURE)
4. mtDNA comparison table
5. Historical scenario: when/how did they diverge?
6. Full reference list with DOIs
```

---

### 12.2. Генетика Княжеских Родов — Молекулярная Генеалогия

> Скопируй весь блок ниже:

```
Please conduct a genetic genealogy analysis of Caucasian noble families.
Focus on Y-DNA studies and publications from 2015-2025.
Provide full citations with DOI links.

TOPIC: Genetic signatures of Caucasian noble clans - verifying oral traditions

CONTEXT:
Caucasian societies maintained strict clan (фамилия) structures for centuries.
Oral traditions claim specific origins for noble families, but genetics can test these.

KNOWN CASES:
| Family | Claimed Origin | Y-DNA Result | Verified? |
|--------|----------------|--------------|-----------|
| Tamby (Тамби) | Inal dynasty | R1a-BY60213 | ✅ ~500 CE |
| Ankvab (Анкваб) | Ancient Abkhaz | R1b-FGC43622 | ✅ ~2150 BCE |
| Shogenov? | Kabardian | Unknown | ❓ |
| Chachba? | Abkhaz kings | Unknown | ❓ |

QUESTIONS:
1. **Known Lineages:**
   - Complete list of tested Caucasian noble families?
   - Which haplogroups for each?
   - Do multiple families share the same Y-DNA (common ancestor)?

2. **Inal Dynasty Testing:**
   - Tamby = BY60213 confirmed
   - Other families claiming Inal descent: same haplogroup?
   - Evidence for/against Inal as historical figure?

3. **Abkhazian Nobility:**
   - Chachba (Shervashidze) royal family Y-DNA?
   - Marshania, Anchabadze, other princes?

4. **TMRCA and Oral History:**
   - Does genetic dating match historical claims?
   - Examples of confirmed vs disproven genealogies?

5. **Founder Effects:**
   - Which clans show star-burst expansion (reproductive success)?
   - Evidence of polygyny in elite lineages?

6. **Cross-border Connections:**
   - Georgian (Dadiani, Gurieli) vs Circassian nobility genetics?
   - Alan-Ossetian nobility genetics?

KEY FAMILIES TO INVESTIGATE:
| Family | Ethnicity | Historical Role |
|--------|-----------|-----------------|
| Кабардинские князья | Kabardian | Inal lineage claim |
| Chachba/Shervashidze | Abkhaz | Royal dynasty |
| Marshania | Abkhaz | Feudal lords |
| Digor aristocracy | Ossetian | Basiats caste |

SOURCES TO CHECK:
- FTDNA Circassian projects
- Kabardino-Balkarian genetic studies
- Russian anthropological journals
- Family Trees DNA projects for Caucasus
- Ossetian genealogy studies

EXPECTED OUTPUT FORMAT:
1. Table of tested noble families with Y-DNA results
2. Phylogenetic tree of related noble lineages
3. TMRCA comparison: genetic vs historical claims
4. Map of noble family geographic origins
5. Evaluation: which oral traditions are supported?
6. Full reference list with DOIs
```

---

### 12.3. Убыхское Наследие — Генетика Исчезнувшего Народа

> Скопируй весь блок ниже:

```
Please conduct a genetic genealogy search for Ubykh descendants.
Focus on publications from 2015-2025 and genetic databases.
Provide full citations with DOI links.

TOPIC: The genetic legacy of the Ubykh - an extinct NWC language, surviving genes

CONTEXT:
The Ubykh were a Northwest Caucasian people whose language went extinct in 1992 
with the death of the last speaker, Tevfik Esenç. The Ubykh language was famous 
for having the most consonants (81-84) of any known language.

HISTORICAL BACKGROUND:
- Original homeland: Black Sea coast between Sochi and Gagra
- 1864: Almost entire population (~45,000) exiled to Ottoman Empire
- Today: Descendants live in Turkey, Jordan, Israel
- Language: extinct, but Y-DNA survives

QUESTIONS:
1. **Genetic Identity:**
   - Have any Ubykh descendants been Y-DNA tested?
   - What haplogroups do they carry?
   - Do they differ from Adyghe/Abkhaz profiles?

2. **Diaspora Genetics:**
   - Ubykh diaspora in Turkey: any genetic studies?
   - Comparison with Circassian diaspora in Turkey?

3. **Pre-Exodus Profile:**
   - Based on geographic position (between Abkhaz and Adyghe)
   - Expected to be intermediate between two groups?
   - Any unique lineages specific to Ubykh coast?

4. **Historical Records:**
   - Ubykh tribal structure (Shapsygh, Sahache, etc.)
   - Any clan-specific genetic markers?

5. **Modern Descendants:**
   - Known Ubykh families in Turkey: Esenç, Güngör, others?
   - Have they contributed to genetic projects?

6. **Linguistic-Genetic Correlation:**
   - Ubykh language was closest to Abkhaz
   - Are Ubykh genetically closer to Abkhaz or Adyghe?

KEY SEARCH TARGETS:
| Group | Location | Notes |
|-------|----------|-------|
| Ubykh families | Turkey (Marmara) | Diaspora since 1864 |
| Esenç family | Turkey | Last speaker's family |
| Uzunyayla Circassians | Turkey | Mixed community |

SOURCES TO CHECK:
- FTDNA Circassian projects
- Turkish genetic studies
- Diaspora community genealogy projects
- Linguistic anthropology papers on Ubykh
- Ottoman exile records

EXPECTED OUTPUT FORMAT:
1. List of known Ubykh Y-DNA results (if any)
2. Comparison with Abkhaz and Adyghe profiles
3. Map of Ubykh diaspora settlements
4. Assessment: is Ubykh genetic profile recoverable?
5. Recommendations for future sampling
6. Full reference list with DOIs
```

---

### 11.1. Меотийская aDNA — Пропущенное Звено

> Скопируй весь блок ниже:

```
Please conduct a comprehensive search for ancient DNA from Meotian culture burials.
Focus on archaeological publications and aDNA databases from 2018-2025.
Provide full citations with DOI links.

TOPIC: Ancient DNA from Meotians (Maeotae) - the missing link in Northwest Caucasus

CONTEXT:
The Meotians (Maeotae) were an ancient people inhabiting the Kuban River basin and 
Sea of Azov coast from ~600 BCE to ~400 CE. They are considered the direct ancestors 
of modern Adyghe (Circassians). However, there is a critical gap in ancient DNA:

KNOWN aDNA TIMELINE:
| Period | Culture | Y-DNA Known |
|--------|---------|-------------|
| 3500 BCE | Novosvobodnaya | J2a (I6268) ✅ |
| 3300 BCE | Maykop | J2a (I6266, OSS002) ✅ |
| 1325 BCE | Late Dolmen | J2a (I2051) ✅ |
| 1200-400 BCE | Koban | G2a1a (Koban7, Koban9) ✅ |
| **600 BCE - 400 CE** | **MEOTIAN** | **???** ❓ |
| 700-900 CE | Saltovo-Mayaki | G2a, R1a, J2a ✅ |
| Modern | Circassians | 70-80% G2a ✅ |

THE GAP:
There is an ~800-year gap in Y-DNA data between Koban (400 BCE) and Saltovo (700 CE).
The Meotians occupy exactly this period. Did they carry J2a, G2a, or both?

QUESTIONS:
1. **Archaeological Sites:**
   - What are the major excavated Meotian burial sites?
   - Sites: Ust-Labinsk, Elizavetinskaya, Semibratnee, Tsemdolina?
   - Any aDNA sequencing attempts?

2. **Published aDNA:**
   - Are there ANY Y-haplogroup results from Meotian contexts?
   - If yes, what haplogroups?
   - If no, why? (preservation, access, funding?)

3. **Greek Colonial Context:**
   - Meotians interacted heavily with Greek colonies (Panticapaeum, Phanagoria)
   - Any aDNA from Bosporan Kingdom contexts that might include Meotians?
   - Y-DNA from Greek colonial cemeteries in the Kuban?

4. **Ethnic Composition:**
   - Ancient sources describe Meotians as related to Sindoi and other "Maeotic" tribes
   - Genetic distinction between Sindoi/Meotians and interior groups?
   - Sarmatian admixture in Meotians?

5. **mtDNA Evidence:**
   - Even without Y-DNA, is there mtDNA from Meotian contexts?
   - Can mtDNA show continuity to modern Circassians?

KEY SITES TO SEARCH:
| Site | Location | Period | Notes |
|------|----------|--------|-------|
| Ust-Labinsk kurgan | Kuban | 5th-3rd c. BCE | Rich Meotian burials |
| Elizavetinskaya | Kuban delta | 4th c. BCE | Greek-Meotian contact |
| Semibratnee | Kuban | 5th c. BCE | Elite burials |
| Tsemdolina | Near Novorossiysk | 4th-2nd c. BCE | Meotian necropolis |

SOURCES TO CHECK:
- Russian Archaeological journals (Российская Археология)
- Krasnodar Museum publications
- AADR database for any Kuban Iron Age samples
- Publications by Leskov, Marchenko on Meotian archaeology
- aDNA studies from adjacent cultures (Scythians, Sarmatians)

EXPECTED OUTPUT FORMAT:
1. Summary of Meotian archaeology (key sites, chronology)
2. Table of ALL aDNA results from Iron Age Kuban if any exist
3. If no Y-DNA: analysis of why and prospects for future sampling
4. mtDNA data if available
5. Prediction: what Y-DNA would we expect in Meotians?
6. Full reference list with DOIs
```

---

### 11.2. G2a1a vs G2a2b — Две Разные Популяции G2a

> Скопируй весь блок ниже:

```
Please conduct a phylogeographic analysis of the G2a split in the Caucasus.
Focus on YFull tree data and publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Why is Koban G2a1a different from Circassian G2a2b/L1264?

CONTEXT:
Ancient DNA and modern distributions show two distinct G2a populations in the Caucasus:

| Clade | TMRCA | Ancient DNA | Modern Distribution |
|-------|-------|-------------|---------------------|
| **G2a1a (Z6653/FGC1159)** | ~8000 BCE | Koban7, Koban9 (Iron Age) | Ossetians (70%), Balkars, Georgians |
| **G2a2b (L1264)** | ~2200 BCE | AU78077 (7th c. CE Avar) | Circassians (70%), Abkhazians |

THE PARADOX:
- Koban culture (1200-400 BCE) is in central North Caucasus
- Circassians descend from western Koban/Meotians
- Yet Koban aDNA = G2a1a, Circassians = G2a2b

Why are they different? Where is G2a2b in ancient DNA?

HYPOTHESES:
1. **Geographic Split:**
   - G2a1a = Central Caucasus (Koban → Ossetians)
   - G2a2b = Western Caucasus (Colchis → Circassians)
   - Two refugia, independent expansions?

2. **Chronological Split:**
   - G2a1a is older (~8000 BCE)
   - G2a2b/L1264 is younger (~2200 BCE), post-4.2ky founder effect?
   - L1264 expanded AFTER Koban era samples?

3. **Colchian Origin:**
   - G2a2b originated in Colchis (humid Black Sea coast)
   - Expanded into NW Caucasus after Dolmen collapse
   - Never reached central Koban zone?

QUESTIONS:
1. **Phylogenetic Deep Dive:**
   - What is the exact relationship: G2a1 vs G2a2?
   - Common ancestor TMRCA?
   - When did they split geographically?

2. **Modern Distribution Map:**
   - G2a1a frequencies in: Ossetians, Balkars, Karachays, Georgians, Svans
   - G2a2b frequencies in: Adyghe, Abkhazians, Ubykh descendants
   - Is there a clear geographic boundary?

3. **Ancient DNA Search:**
   - Are there ANY ancient G2a2b/L1264 samples from Caucasus (not Avar)?
   - Any G2a from Colchian contexts (Western Georgia)?
   - Any G2a from Dolmen culture?

4. **Georgian/Mingrelian Diversity:**
   - Reports show high G2a diversity in Mingrelians
   - Are both G2a1a AND G2a2b present?
   - Is Colchis the source for both clades?

5. **Linguistic Correlation:**
   - G2a1a → Ossetic/Kartvelian speakers?
   - G2a2b → NWC (Abkhaz-Adyghe) speakers?
   - Does the genetic split match the linguistic divide?

KEY SUBCLADES TO ANALYZE:
| Clade | Key SNPs | Modern Distribution |
|-------|----------|---------------------|
| G-Z6653 (G2a1a) | FGC1159, FGC1160 | Ossetia, Georgia |
| G-L1264 (G2a2b) | FGC21495, Z44222 | Circassia, Abkhazia |
| G-L293 | - | Ossetia (different from L1264!) |
| G-P303 | - | Parent of L1264 |

SOURCES TO CHECK:
- YFull: https://www.yfull.com/tree/G-P15/
- FTDNA G2a project
- Koban aDNA publications (Harney et al.)
- Georgian biobank studies
- Publications on Ossetian genetics

EXPECTED OUTPUT FORMAT:
1. Phylogenetic tree showing G2a1 vs G2a2 relationship
2. Split date (TMRCA of common ancestor)
3. Geographic distribution map (textual description)
4. Table of ancient G2a samples with precise subclades
5. Hypothesis evaluation: which scenario best fits data?
6. Full reference list with DOIs
```

---

### 11.3. mtDNA Continuity — Материнские Линии от Дольменов к Современности

> Скопируй весь блок ниже:

```
Please conduct a comprehensive mtDNA analysis of Northwest Caucasus populations.
Focus on publications from 2015-2025.
Provide full citations with DOI links.

TOPIC: Mitochondrial DNA continuity from Dolmen culture to modern Circassians

CONTEXT:
The Y-DNA shows a dramatic shift (J2a → G2a), but mtDNA should show CONTINUITY 
if the "female line persistence" model is correct. Testing this hypothesis:

Y-DNA SHIFT (known):
- Dolmen/Maykop: J2a dominant
- Modern Circassians: G2a dominant (70%)
- Interpretation: Y-DNA replacement

mtDNA PREDICTION:
- If population was replaced: mtDNA should also change
- If only Y-DNA replaced (elite dominance): mtDNA should show CONTINUITY

QUESTIONS:
1. **Ancient mtDNA Inventory:**
   - List ALL mtDNA haplogroups from:
     a) Maykop culture
     b) Novosvobodnaya
     c) Dolmen culture
     d) Koban culture
   - Create frequency table

2. **Modern Circassian mtDNA:**
   - Major haplogroups in Adyghe, Kabardians, Abkhazians?
   - Common haplogroups: H, U5, T2, HV, etc.?
   - Frequency comparison with ancient samples

3. **Continuity Test:**
   - Which specific mtDNA lineages appear in BOTH ancient and modern?
   - Example: If H1a is in Dolmen AND modern Adyghe = continuity marker
   - Statistical analysis of haplogroup overlap?

4. **Contrast with Y-DNA:**
   - mtDNA turnover % vs Y-DNA turnover %?
   - Is mtDNA more stable (as predicted)?

5. **East Asian Signal:**
   - AU78077 (Avar G-L1264) had D4j11 (East Asian)
   - Any East Asian mtDNA in modern Circassians?
   - Evidence of Avar/Turkic maternal contribution?

6. **Comparative Analysis:**
   - Caucasus mtDNA vs European Neolithic?
   - Caucasus mtDNA vs Steppe populations?
   - Unique "Caucasian" mtDNA lineages?

KEY mtDNA HAPLOGROUPS TO TRACK:
| Haplogroup | Typical Association | Expected in Caucasus? |
|------------|---------------------|----------------------|
| H | European Neolithic | High in Caucasus |
| U5 | European Hunter-Gatherer | Should persist |
| T2 | Neolithic farmer | Present |
| HV | West Asian | Expected |
| X2 | Ancient Near East | Possible |
| U4 | Eastern European | Steppe admixture? |

SOURCES TO CHECK:
- Wang et al. (2019) - Maykop mtDNA
- Lazaridis et al. (2022) - Caucasus samples
- Circassian genetic studies (Yunusbayev, Balanovsky)
- Georgian biobank mtDNA data
- AADR database mtDNA annotations

EXPECTED OUTPUT FORMAT:
1. Table: Ancient Caucasus mtDNA by culture (Maykop, Dolmen, Koban)
2. Table: Modern Circassian mtDNA frequencies
3. Venn diagram description: overlap between ancient and modern
4. Statistical measure of continuity (if calculated in any study)
5. Comparison: mtDNA stability vs Y-DNA turnover
6. Full reference list with DOIs
```

---

### 11.4. J1-Z1842 — Закавказский Древний Субстрат

> Скопируй весь блок ниже:

```
Please conduct a comprehensive phylogeographic analysis of J1-Z1842 in the Caucasus.
Focus on publications from 2018-2025 and YFull data.
Provide full citations with DOI links.

TOPIC: J1-Z1842 - The ancient Transcaucasian layer in Adyghe genetics

CONTEXT:
J1 is the third most common Y-haplogroup among modern Circassians (~10-15%). 
Unlike J2a (Maykop elite), J1 has different associations:

- J1-Z1842 is linked to **Kura-Araxes culture** (3400-2000 BCE)
- Found in both South and North Caucasus
- Present in modern Adyghe, Abkhaz, Chechens, Georgians

KEY PHYLOGENETIC DATA:
| Subclade | TMRCA | Distribution |
|----------|-------|--------------|
| J1-Z1842 | ~4300 BCE | Pan-Caucasian |
| J1-L136 | ~3000 BCE | Dagestan, Chechnya |
| J1-FGC6064 | ~2000 BCE | Specific clans |

QUESTIONS:
1. **Phylogenetic Position:**
   - Full path from J1-M267 to caucasian subclades
   - TMRCA of Z1842 (YFull estimates)?
   - Downstream clades specific to Circassians?

2. **Ancient DNA:**
   - Any J1-Z1842 in Kura-Araxes samples?
   - J1 in Maykop? (contrast with J2a)
   - J1 in Koban or Dolmen contexts?

3. **Modern Distribution:**
   - J1 frequency in: Adyghe, Kabardians, Abkhaz
   - Comparison with: Chechens, Ingush, Dagestani
   - Is J1 more "Northeast Caucasian" than "Northwest"?

4. **Historical Interpretation:**
   - Did J1 arrive with Kura-Araxes expansion?
   - Or is it pre-Kura-Araxes indigenous?
   - Relation to "Hurrian" substrate hypothesis?

5. **Contrast with J2a:**
   - J2a = Maykop elite (confirmed)
   - J1 = different population layer?
   - Geographic separation in ancient period?

KEY SAMPLES TO FIND:
| Culture | Period | Expected J1? |
|---------|--------|--------------|
| Kura-Araxes | 3400-2000 BCE | Likely |
| Maykop | 3700-3000 BCE | Minority |
| Koban | 1200-400 BCE | Possible |

SOURCES TO CHECK:
- YFull: https://www.yfull.com/tree/J-Z1842/
- FTDNA J1 project
- Kura-Araxes aDNA publications
- Balanovsky et al. on Caucasus Y-DNA
- Chechen/Ingush genetic studies

EXPECTED OUTPUT FORMAT:
1. J1-Z1842 phylogenetic tree with key subclades
2. Ancient DNA table with all J1 samples from Caucasus
3. Modern frequency map (textual description)
4. Historical scenario: J1 arrival and persistence
5. Comparison: J1 vs J2a geographic/temporal distribution
6. Full reference list with DOIs
```

---

### 11.5. Q1a — Тюркско-Гуннское Наследие

> Скопируй весь блок ниже:

```
Please conduct a comprehensive analysis of haplogroup Q in the North Caucasus.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Haplogroup Q in the Caucasus - Hunnic, Turkic, or earlier?

CONTEXT:
Haplogroup Q is found at notable frequencies in the North Caucasus, particularly 
among Turkic-speaking groups (Balkars, Karachays: 10-20%) and at lower levels 
in Circassians (~5%). Its origin is a subject of debate:

COMPETING HYPOTHESES:
1. **Hunnic arrival (370 CE):** Q arrived with the Huns
2. **Turkic Khaganate (552+ CE):** Q came with Bulgar/Khazar migrations
3. **Bronze Age presence:** Q was already in Caucasus from Yamnaya/Catacomb

KEY DATA POINTS:
| Group | Q frequency | Possible source |
|-------|-------------|-----------------|
| Balkars | 15-20% | Turkic? |
| Karachays | 12-18% | Turkic? |
| Kabardians | 3-5% | Admixture? |
| Adyghe | 2-5% | Low frequency |

Ancient sample:
- Novozavedennoye-III: **Q1b** individual (~500 BCE, Scythian context)

QUESTIONS:
1. **Subclade Identification:**
   - Which Q subclades are found in Caucasus?
   - Q1a vs Q1b distribution?
   - Specific SNPs (L54, M3, M242)?

2. **Ancient DNA Timeline:**
   - Q in Scythian samples (Novozavedennoye)?
   - Q in Saltovo-Mayaki (Khazar period)?
   - Q in Hunnic-period burials?

3. **Turkic vs Pre-Turkic:**
   - Do Caucasian Q lineages cluster with:
     a) Siberian Turkic (Yakuts, Tuvans)?
     b) Hunnic-period samples?
     c) Bronze Age steppe (Yamnaya, Catacomb)?
   - TMRCA analysis to date arrival?

4. **Linguistic Correlation:**
   - Q highest in Turkic speakers (Balkars, Karachays)
   - Does this prove Turkic migration brought Q?
   - Or did Turkic language spread to Q-carrying locals?

5. **Geographic Pattern:**
   - Q concentrated in central North Caucasus
   - Low in coastal/western groups (Adyghe, Abkhaz)
   - Does this reflect Turkic settlement pattern?

KEY SOURCES TO CHECK:
- Novozavedennoye excavation reports
- Hunnic/Avar genetic studies
- Saltovo-Mayaki aDNA
- Balkar/Karachay genetic studies
- Yunusbayev et al. on Turkic populations

EXPECTED OUTPUT FORMAT:
1. Q subclade distribution in Caucasus (table)
2. Timeline of Q arrival based on aDNA
3. Comparison with Central Asian/Siberian Q
4. Most likely historical scenario
5. Association with Turkic language spread
6. Full reference list with DOIs
```

---

### 11.6. Аутосомный Профиль — CHG, EHG, Анатолия

> Скопируй весь блок ниже:

```
Please conduct a comprehensive autosomal ancestry analysis of Northwest Caucasus.
Focus on publications from 2018-2025.
Provide full citations with DOI links.

TOPIC: Autosomal ancestry components in Circassians - CHG, EHG, and Anatolian

CONTEXT:
Modern Circassians show a unique autosomal profile that differs from their neighbors.
Key ancestral components in the region:

| Component | Full Name | Source Population |
|-----------|-----------|-------------------|
| **CHG** | Caucasus Hunter-Gatherer | Indigenous Caucasus (Kotias, Satsurblia) |
| **EHG** | Eastern Hunter-Gatherer | Eastern Europe (Samara, Karelia) |
| **Anatolia_N** | Anatolian Neolithic | Early farmers (Çatalhöyük) |
| **Iran_N** | Iranian Neolithic | Zagros (Ganj Dareh) |
| **Steppe_EMBA** | Steppe Early/Middle Bronze | Yamnaya-derived |

The Northwest Caucasus shows HIGH CHG + moderate Anatolia_N + LOW Steppe compared
to their Steppe neighbors, but more Steppe than South Caucasians.

QUESTIONS:
1. **Modern Circassian Profile:**
   - What is the ADMIXTURE/qpAdm model for Adyghe?
   - CHG vs Anatolia_N vs Steppe proportions?
   - Comparison: Circassians vs Ossetians vs Georgians vs Armenians

2. **Ancient Trajectory:**
   - Maykop autosomal profile (Wang 2019)?
   - Dolmen/Novosvobodnaya profile?
   - Koban profile?
   - How did it change over time?

3. **Steppe Admixture:**
   - When did Steppe_EMBA arrive in NW Caucasus?
   - Proportion in ancient vs modern?
   - Is it increasing or stable?

4. **The "Maykop Enigma":**
   - Maykop has CHG + Iran_N + low Steppe
   - This is DIFFERENT from Yamnaya
   - Did Maykop block Yamnaya expansion into Caucasus?

5. **PCA Position:**
   - Where do Circassians plot on West Eurasia PCA?
   - Closest ancient populations?
   - Drift from Bronze Age to modern?

6. **Y-DNA vs Autosomal:**
   - Y-DNA shows turnover (J2a→G2a)
   - Autosomal shows continuity
   - How to reconcile mathematically?

KEY STUDIES TO CHECK:
- Wang et al. (2019) Nature - Maykop
- Lazaridis et al. (2022) Cell - Southern Arc
- Ringbauer et al. (2024/2025) - Caucasus IBD
- AADR modern Caucasus samples

EXPECTED OUTPUT FORMAT:
1. ADMIXTURE bar chart description for Circassians
2. qpAdm model table (source populations, proportions, p-values)
3. PCA position description
4. Temporal trajectory: Maykop → Dolmen → Koban → Modern
5. Comparison table: Circassians vs neighbors
6. Resolution of Y-DNA turnover vs autosomal continuity
7. Full reference list with DOIs
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
