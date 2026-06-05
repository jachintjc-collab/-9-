#!/usr/bin/env python3
"""Phase 59n — Weekly site health monitor.

Generates weekly-report.html with:
  - Total pages, schema blocks, sitemap URLs
  - Schema validity health
  - Hreflang health
  - Orphan pages (no internal links pointing to them)
  - Broken internal links
  - Pages added/removed since baseline (if baseline.json exists)
  - Top 10 most-linked pages (internal PageRank proxy)

Usage:
  python3 phase59n_weekly_monitor.py [--baseline]
    --baseline saves current state as baseline for next-week diffing.
"""
import re, json, sys
from pathlib import Path
from datetime import datetime
from collections import Counter

OUT = Path("/sessions/gallant-wizardly-hopper/mnt/outputs/phase59-final")
BASELINE = OUT / ".monitor-baseline.json"

# Collect all HTML pages
all_pages = []
for p in sorted(OUT.glob("*.html")):
    all_pages.append(("en", str(p.relative_to(OUT))))
for p in sorted((OUT / "ko").glob("*.html")):
    all_pages.append(("ko", str(p.relative_to(OUT))))

# Stats containers
schema_count = 0
schema_valid = 0
hreflang_clean = 0
internal_link_counter = Counter()
broken_links_per_page = {}
orphan_pages = []
all_filenames = {Path(p).name for _, p in all_pages}
schema_pat = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL)

for lang, path in all_pages:
    full = OUT / path
    text = full.read_text(encoding="utf-8")

    # Schemas
    for m in schema_pat.finditer(text):
        schema_count += 1
        try:
            json.loads(m.group(1).strip())
            schema_valid += 1
        except:
            pass

    # Hreflang health
    if re.search(r'rel="alternate"\s+hreflang="(en|ko|x-default)"', text):
        hreflang_clean += 1

    # Internal links
    page_broken = []
    for href in re.findall(r'href="(?!mailto:|tel:|https?:|//|#|/)([^"]+\.html)"', text):
        target_name = href.split("/")[-1]
        # In same dir? Or in ko/?
        if "/ko/" in path or path.startswith("ko/"):
            target_full = OUT / "ko" / target_name
            if not target_full.exists():
                target_full = OUT / target_name
        else:
            target_full = OUT / target_name
        if not target_full.exists():
            page_broken.append(href)
        else:
            internal_link_counter[str(target_full.relative_to(OUT))] += 1
    if page_broken:
        broken_links_per_page[path] = page_broken

# Find orphans (pages no other page links to)
linked_targets = set(internal_link_counter.keys())
for _, p in all_pages:
    if p not in linked_targets and not (p.endswith("index.html") or p in ("about.html", "terms.html", "privacy.html", "dmca.html", "contact.html", "404.html", "schema-monitoring.html", "hreflang-health.html", "weekly-report.html")):
        orphan_pages.append(p)

# Top 10 most-linked
top_linked = internal_link_counter.most_common(10)

# Sitemap URLs
sitemap_path = OUT / "sitemap.xml"
sitemap_urls = sitemap_path.read_text(encoding="utf-8").count("<loc>") if sitemap_path.exists() else 0

# Baseline comparison
current_state = {
    "scan_date": datetime.utcnow().isoformat(),
    "total_pages": len(all_pages),
    "schema_count": schema_count,
    "sitemap_urls": sitemap_urls,
    "pages": [p for _, p in all_pages],
}

if "--baseline" in sys.argv:
    BASELINE.write_text(json.dumps(current_state, indent=2), encoding="utf-8")
    print(f"✓ Baseline saved to {BASELINE.name}")
    print(f"  Pages: {current_state['total_pages']}, Schemas: {schema_count}, Sitemap: {sitemap_urls}")
    sys.exit(0)

# Diff against baseline if exists
diff_added = []
diff_removed = []
prev = None
if BASELINE.exists():
    prev = json.loads(BASELINE.read_text(encoding="utf-8"))
    prev_set = set(prev["pages"])
    cur_set = set(current_state["pages"])
    diff_added = sorted(cur_set - prev_set)
    diff_removed = sorted(prev_set - cur_set)

# Build dashboard
def row(name, value, status="ok"):
    color = "#66bb6a" if status == "ok" else ("#ef5350" if status == "fail" else "#ba7517")
    return f'<div class="stat"><div class="num" style="color:{color};">{value}</div><div class="lbl">{name}</div></div>'

orphans_html = ""
if orphan_pages:
    orphans_html = '<ul class="issue-list">' + "".join(f"<li><code>{p}</code></li>" for p in orphan_pages[:30]) + "</ul>"
    if len(orphan_pages) > 30:
        orphans_html += f'<p style="font-size:11px;color:#b0a09a;">…{len(orphan_pages) - 30} more</p>'
else:
    orphans_html = '<p style="color:#66bb6a;">✓ No orphan pages</p>'

broken_html = ""
if broken_links_per_page:
    rows = "".join(
        f'<tr><td><code>{p}</code></td><td><ul style="margin:0;padding-left:18px;">' + "".join(f"<li>{b}</li>" for b in broken[:3]) + "</ul></td></tr>"
        for p, broken in list(broken_links_per_page.items())[:20]
    )
    broken_html = f'<table style="font-size:12px;width:100%;border-collapse:collapse;"><thead><tr><th>Page</th><th>Broken links</th></tr></thead><tbody>{rows}</tbody></table>'
else:
    broken_html = '<p style="color:#66bb6a;">✓ No broken internal links</p>'

top_html = '<table style="width:100%;border-collapse:collapse;font-size:13px;"><thead><tr><th>#</th><th>Page</th><th>Links to it</th></tr></thead><tbody>' + \
    "".join(f'<tr><td>{i+1}</td><td><code>{p}</code></td><td>{c}</td></tr>' for i, (p, c) in enumerate(top_linked)) + \
    '</tbody></table>'

diff_html = ""
if prev:
    diff_html = f'''
<h2>Diff since last baseline ({prev["scan_date"][:10]})</h2>
<div class="summary-grid">
  <div class="stat"><div class="num" style="color:{'#66bb6a' if not diff_added else '#ba7517'};">+{len(diff_added)}</div><div class="lbl">Pages added</div></div>
  <div class="stat"><div class="num" style="color:{'#66bb6a' if not diff_removed else '#ef5350'};">-{len(diff_removed)}</div><div class="lbl">Pages removed</div></div>
  <div class="stat"><div class="num">{schema_count - prev["schema_count"]:+d}</div><div class="lbl">Schema delta</div></div>
  <div class="stat"><div class="num">{sitemap_urls - prev["sitemap_urls"]:+d}</div><div class="lbl">Sitemap delta</div></div>
</div>
{('<h3>Added</h3><ul>' + "".join(f'<li><code>{p}</code></li>' for p in diff_added) + '</ul>') if diff_added else ''}
{('<h3 style="color:#ef5350;">Removed</h3><ul>' + "".join(f'<li><code>{p}</code></li>' for p in diff_removed) + '</ul>') if diff_removed else ''}
'''
else:
    diff_html = '<p style="font-size:13px;color:#b0a09a;">No baseline yet. Run with <code>--baseline</code> flag to save current state.</p>'

report = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Weekly Site Health Report — re9guide.it.com</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 1400px; margin: 30px auto; padding: 0 20px; background: #1a0f0a; color: #f0ebe8; }}
h1 {{ color: #c0392b; border-bottom: 2px solid #c0392b; padding-bottom: 10px; }}
h2 {{ color: #ba7517; margin-top: 40px; border-bottom: 0.5px solid rgba(186,117,23,0.3); padding-bottom: 8px; }}
h3 {{ color: #f0ebe8; margin-top: 20px; }}
.summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 20px 0; }}
.stat {{ background: rgba(192, 57, 43, 0.08); border-left: 3px solid #c0392b; padding: 14px; }}
.stat .num {{ font-size: 26px; font-weight: bold; color: #c0392b; }}
.stat .lbl {{ font-size: 11px; text-transform: uppercase; color: #b0a09a; letter-spacing: 0.5px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 0.5px solid rgba(192,57,43,0.18); }}
th {{ background: rgba(192,57,43,0.15); color: #c0392b; font-size: 11px; text-transform: uppercase; }}
code {{ background: rgba(192,57,43,0.1); padding: 2px 6px; border-radius: 2px; font-size: 12px; }}
.issue-list {{ margin: 0; padding-left: 20px; font-size: 12px; }}
.issue-list li {{ margin: 3px 0; }}
.intro {{ background: rgba(186, 117, 23, 0.08); border-left: 3px solid #ba7517; padding: 15px; margin: 20px 0; font-size: 13px; }}
.health-ok {{ color: #66bb6a; }}
.health-warn {{ color: #ba7517; }}
.health-fail {{ color: #ef5350; }}
</style>
</head>
<body>

<h1>Weekly Site Health Report</h1>
<p style="color:#b0a09a;font-size:13px;">Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")} · re9guide.it.com</p>

<div class="intro">
<strong>Site-wide health snapshot.</strong> Run this script weekly: <code>python3 phase59n_weekly_monitor.py</code>.
First run, add <code>--baseline</code> to save state. Subsequent runs compare to baseline.
</div>

<h2>Overview</h2>
<div class="summary-grid">
  <div class="stat"><div class="num">{len(all_pages)}</div><div class="lbl">Total HTML pages</div></div>
  <div class="stat"><div class="num">{schema_count}</div><div class="lbl">Schema blocks</div></div>
  <div class="stat"><div class="num">{sitemap_urls}</div><div class="lbl">Sitemap URLs</div></div>
  <div class="stat"><div class="num health-{'ok' if schema_valid == schema_count else 'fail'}">{schema_valid}/{schema_count}</div><div class="lbl">Schema valid</div></div>
  <div class="stat"><div class="num health-{'ok' if hreflang_clean >= len(all_pages) - 5 else 'warn'}">{hreflang_clean}/{len(all_pages)}</div><div class="lbl">Hreflang clean</div></div>
  <div class="stat"><div class="num health-{'ok' if not broken_links_per_page else 'fail'}">{sum(len(b) for b in broken_links_per_page.values())}</div><div class="lbl">Broken internal links</div></div>
  <div class="stat"><div class="num health-{'ok' if not orphan_pages else 'warn'}">{len(orphan_pages)}</div><div class="lbl">Orphan pages</div></div>
</div>

{diff_html}

<h2>Top 10 most-linked pages (internal PageRank proxy)</h2>
{top_html}

<h2>Orphan pages — no internal links to them</h2>
<p style="font-size:12px;color:#b0a09a;">These pages exist but no other page links to them. Google may struggle to discover them via crawl.</p>
{orphans_html}

<h2>Broken internal links</h2>
{broken_html}

<hr style="margin-top:50px;border:none;border-top:0.5px solid rgba(192,57,43,0.3);">
<p style="text-align:center;font-size:11px;color:#706056;">Phase 59n weekly monitor · re9guide.it.com</p>

</body>
</html>'''

(OUT / "weekly-report.html").write_text(report, encoding="utf-8")
print(f"✓ Weekly report: weekly-report.html")
print(f"  Pages scanned: {len(all_pages)}")
print(f"  Schema blocks: {schema_count} ({schema_valid} valid)")
print(f"  Hreflang clean: {hreflang_clean}/{len(all_pages)}")
print(f"  Internal broken links: {sum(len(b) for b in broken_links_per_page.values())} across {len(broken_links_per_page)} pages")
print(f"  Orphan pages: {len(orphan_pages)}")
if prev:
    print(f"  Diff: +{len(diff_added)} pages, -{len(diff_removed)} pages since {prev['scan_date'][:10]}")
