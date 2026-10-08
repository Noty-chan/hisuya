"""Prepare Quartz content from the vault, without editing the source notes."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / '.site' / 'content'
assert CONTENT.resolve().parent == (ROOT / '.site').resolve()
if CONTENT.exists():
    shutil.rmtree(CONTENT)
CONTENT.mkdir()

count = 0
for source in ROOT.iterdir():
    if source.is_dir() and (re.match(r'^\d\d ', source.name) or source.name == 'файлы'):
        for file in source.rglob('*'):
            if not file.is_file():
                continue
            rel = file.relative_to(ROOT)
            target = CONTENT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if 'Ноти' in rel.parts or file.name == 'noty_specification.md':
                if file.suffix == '.md':
                    target.write_text('# Посторонний проект\n\nЭта запись относится к программному проекту Ноти и не опубликована в справочнике мира.\n', encoding='utf-8')
                continue
            if file.suffix == '.md':
                text = file.read_text(encoding='utf-8-sig')
                # Local archive stays on the author's computer, not on the public website.
                text = re.sub(r'\[Полная копия до уборки\]\(<[^>]+>\)', 'Полная копия до уборки сохранена у автора локально.', text)
                # Quartz uses index.md as the homepage; preserve readable labels.
                text = re.sub(r'\[\[Хисуя(?:\.md)?(?=[|\]#])', '[[index', text)
                target.write_text(text, encoding='utf-8')
            else:
                shutil.copy2(file, target)
            count += 1

home = (ROOT / 'Хисуя.md').read_text(encoding='utf-8-sig')
home = re.sub(r'\[Полная копия до уборки\]\(<[^>]+>\)', 'Полная копия до уборки сохранена у автора локально.', home)
home = '---\ntitle: Возвращение в Хисую\naliases:\n  - Хисуя\n---\n\n' + home
(CONTENT / 'index.md').write_text(home, encoding='utf-8')
print(f'Prepared {count + 1} files for Quartz')
