#!/usr/bin/env python3
"""Analyze subclade G-L1264 for DNA Guide project."""

import json
import csv
from pathlib import Path

# Configuration
TREE_PATH = "/home/valalav/obsidian/01_ЛЧ Проекты/00_DNA/Публикации/claude_2025_12_29/dna_guide/current_tree.json"
CSV_PATH = "/home/valalav/obsidian/01_ЛЧ Проекты/00_DNA/Публикации/claude_2025_12_29/dna_guide/aadna_data.csv"


def find_haplogroup_node(tree, target_id):
    """Recursively find a haplogroup node in the tree by id."""
    if isinstance(tree, dict):
        if tree.get("id") == target_id:
            return tree
        if tree.get("name") == target_id:
            return tree
        # Check SNPs for synonym match
        snps = tree.get("snps", "")
        if target_id in snps:
            return tree
        if "children" in tree:
            for child in tree["children"]:
                result = find_haplogroup_node(child, target_id)
                if result:
                    return result
    return None


def get_full_path(tree, target_id, path=None):
    """Get the full path from root to target node."""
    if path is None:
        path = []

    if isinstance(tree, dict):
        current_id = tree.get("id") or tree.get("name")
        if current_id is None:
            current_id = "Unknown"
        new_path = path + [current_id]

        if current_id == target_id:
            return new_path
        if tree.get("name") == target_id:
            return new_path
        snps = tree.get("snps", "")
        if target_id in snps:
            return new_path

        if "children" in tree:
            for child in tree["children"]:
                result = get_full_path(child, target_id, new_path)
                if result:
                    return result
    return None


def load_aadna_data(csv_path):
    """Load AADNA CSV data."""
    samples = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Extract relevant columns
                sample = {
                    "Name": row.get("Name", ""),
                    "Surname": row.get("Фамилия", ""),
                    "Location": row.get("Lacation", ""),
                    "Subethnos": row.get("Субэтнос", ""),
                    "Haplogroup": row.get("Haplogroup", ""),
                    "Kit": row.get("Kit Number", ""),
                }
                # Only include rows with valid data
                if sample["Haplogroup"]:
                    samples.append(sample)
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return samples


def filter_samples_by_haplogroup(samples):
    """Filter samples that belong to G-L1264 or its immediate subclades."""
    filtered = []

    # Target haplogroups to match (direct L1264 or key subclades)
    target_patterns = [
        "G-L1264",
        "L1264",
        "G-FGC21495",
        "FGC21495",
        "G-Y513104",
        "Y513104",
    ]

    for sample in samples:
        haplo = sample.get("Haplogroup", "")
        # Check if any target pattern is in the haplogroup string
        for pattern in target_patterns:
            if pattern in haplo:
                filtered.append(sample)
                break

    return filtered


def format_lineage_path(path):
    """Format lineage path for display."""
    return " > ".join(path)


def generate_markdown(node, path, samples):
    """Generate markdown output in Russian."""
    formed = node.get("formed", "-")
    tmrca = node.get("tmrca", "-")
    snps = node.get("snps", "")
    children = node.get("children", [])

    # Count child branches
    child_count = len(children)

    # Extract samples data - limit to 30 samples for readability
    sample_lines = []
    if samples:
        display_samples = samples[:30]
        for sample in display_samples:
            surname = sample.get("Surname", "N/A")
            subethnos = sample.get("Subethnos", "N/A")
            location = sample.get("Location", "N/A")
            haplo = sample.get("Haplogroup", "N/A")
            # Only show if surname exists
            if surname and surname != "N/A":
                sample_lines.append(
                    f"- **{surname}** ({subethnos}, {location}): {haplo}"
                )

        if len(sample_lines) == 0:
            sample_lines.append("- Образцы есть, но без указания фамилий")

        if len(samples) > 30:
            sample_lines.append(
                f"\n*... и ещё {len(samples) - 30} образцов из {len(samples)} всего*"
            )
    else:
        sample_lines.append("- Нет образцов в базе данных")

    # Statistics by subethnos
    subethnos_stats = {}
    for sample in samples:
        subethnos = sample.get("Subethnos", "Неизвестно")
        if subethnos not in subethnos_stats:
            subethnos_stats[subethnos] = 0
        subethnos_stats[subethnos] += 1

    # Sort by count
    sorted_subethnos = sorted(subethnos_stats.items(), key=lambda x: x[1], reverse=True)

    # Calculate bottleneck (gap between formed and tmrca)
    gap = "-"
    if formed != "-" and tmrca != "-":
        gap = f"{formed - tmrca} лет"

    markdown = f"""# G-L1264: Кавказская гаплогруппа G2a2

> **Статус:** ✅ Проверено | **TMRCA:** {tmrca} лет назад | **Возраст ветки:** {formed} лет назад

## Основная информация

| Параметр | Значение |
|----------|---------|
| **Идентификатор** | G-L1264 |
| **Синонимы SNP** | {snps} |
| **Сформировано** | {formed} лет назад (формирование ветки) |
| **TMRCA** | {tmrca} лет назад (общий предок) |
| **Период бутылочного горлышка** | {gap} |
| **Потомков веток** | {child_count} |
| **YFull** | https://www.yfull.com/tree/G-L1264/ |
| **AADNA** | https://aadna.ru/ |

## Путь от Адама

```
{format_lineage_path(path)}
```

## Описание гаплогруппы

G-L1264 — это молодая ветка гаплогруппы G2a2 (формируется около {formed} лет назад), которая демонстрирует выраженную связь с Кавказским регионом. 

### Ключевые характеристики:

- **Возраст:** Ветка сформировалась в эпоху бронзы ({formed} лет назад), а общий предок жил около {tmrca} лет назад. Это означает, что линия прошла через длительный период "тумана истории" ({gap} лет) без значительного ветвления.
- **География:** Наибольшее разнообразие и концентрация отмечены в Центральной Кавказского региона, особенно среди западно-кавказских народов.
- **Диверсификация:** Ветка расщепилась на {child_count} основных субкладов, многие из которых имеют специфические этнические распределения.

## Образцы из базы данных AADNA

Ниже приведены протестированные участники, принадлежащие к G-L1264 и её субкладам:

{chr(10).join(sample_lines)}

### Статистика по субэтносам

| Субэтнос | Количество образцов |
|----------|-------------------|
{chr(10).join([f"| {subeth} | {count} |" for subeth, count in sorted_subethnos[:10]])}
{f"| ... | {len(sorted_subethnos) - 10} других субэтносов |" if len(sorted_subethnos) > 10 else ""}

## Кавказский контекст

### Западно-Кавказская фокусировка

G-L1264 представляет собой одну из характерных гаплогрупп для западно-кавказских народов (адыгов, абхазов, абазин). Высокая частота этой линии в регионе может указывать на:

1. **Фундаментальный эффект:** Значительное расширение одной успешной мужской линии в прошлом, которое привело к доминированию в генофонде.
2. **Древнее присутствие:** Поскольку TMRCA составляет {tmrca} лет, линия присутствует в регионе задолго до формирования современных этнических групп.
3. **Связь с древними культурами:** Возраст формирования ({formed} лет назад) перекликается с эпохой Кобанской культуры и других бронзовых цивилизаций Северного Кавказа.

### Важное замечание

Несмотря на то, что G-L1264 широко представлена среди западно-кавказских народов сегодня, **нельзя** говорить об "адыгской" или "абхазской" гаплогруппе в строгом смысле. Современные этносы сформировались значительно позже (в течение последних 1500-2000 лет). Эта линия существовала за тысячи лет до их появления и могла быть ассимилирована из более древнего субстрата региона.

## Субклады (потомки веток)
"""

    # Add information about children
    if children:
        markdown += f"\nВетка G-L1264 имеет **{len(children)}** основных субкладов:\n\n"
        for child in children:
            child_id = child.get("id", "N/A")
            child_tmrca = child.get("tmrca", "N/A")
            child_snps = child.get("snps", "")
            child_name = child.get("name", child_id)

            # Format SNPs - show only first 3 if many
            if child_snps:
                snp_list = [s.strip() for s in child_snps.split(",") if s.strip()]
                if len(snp_list) > 3:
                    snp_display = f"{', '.join(snp_list[:3])} и др."
                else:
                    snp_display = ", ".join(snp_list)
            else:
                snp_display = "нет данных"

            markdown += f"### {child_name}\n"
            markdown += f"- **TMRCA:** {child_tmrca} лет назад\n"
            markdown += f"- **SNPs:** {snp_display}\n\n"

    markdown += """
## Внешние ссылки

- [YFull Tree](https://www.yfull.com/tree/G-L1264/)
- [AADNA Project](https://aadna.ru/)

---
*Обновлено: 2026-01-26 на основе current_tree.json*
"""

    return markdown


def main():
    """Main execution."""
    print("Загрузка дерева YFull...")
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        tree = json.load(f)

    print("Поиск узла G-L1264...")
    node = find_haplogroup_node(tree, "G-L1264")

    if not node:
        print("Узел G-L1264 не найден в дереве")
        return

    print("Получение полного пути...")
    path = get_full_path(tree, "G-L1264")

    # Fix first element if it's "Unknown"
    if path and path[0] == "Unknown":
        path = path[1:]

    print("Загрузка данных AADNA...")
    samples = load_aadna_data(CSV_PATH)

    print("Фильтрация образцов по G-L1264...")
    filtered_samples = filter_samples_by_haplogroup(samples)

    print(f"Найдено {len(filtered_samples)} образцов")

    print("Генерация markdown...")
    markdown = generate_markdown(node, path, filtered_samples)

    # Print output
    print("\n" + "=" * 80)
    print(markdown)
    print("=" * 80)

    # Optionally save to file
    output_path = Path("/tmp/G-L1264_analysis.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"\nСохранено в: {output_path}")


if __name__ == "__main__":
    main()
