"""
Build a single self-contained HTML page showing every spec's Assisted Combat
rotation, with a class/spec picker.
"""

import argparse
import json
import logging
import os
import sys

import pandas as pd

from wow_assist_mapper.skeleton import (
    describe_rule,
    get_plan_rotation,
    parse_and_build_db_dumps,
    resolve_build,
)

_logger = logging.getLogger(__name__)

DEFAULT_OUT_FILE = "out/rotations.html"

# Checks nearly every step has; shown as compact badges instead of full sentences
ROUTINE_RULE_LABELS = {
    0: "Talent taken",
    2: "Off cooldown",
    14: "Can afford",
    56: "In range",
    67: "Castable",
}
UNKNOWN_RULE_TYPES = {70}


def build_rotations(classes, condition_map):
    """Collect every spec's rotation as plain data for the page."""
    rotations = []
    for class_name, class_data in sorted(classes.items()):
        for spec_data in sorted(class_data["specs"].values(), key=lambda spec: spec["Name"]):
            rotation = get_plan_rotation(spec_data.get("assist_plan"))
            if not rotation:
                continue
            steps = []
            for step in rotation:
                rules = []
                for _, rule in sorted(step["rules"].items()):
                    cond_type = int(rule["raw"]["ConditionType"])
                    if cond_type in ROUTINE_RULE_LABELS:
                        kind = "routine"
                    elif cond_type in UNKNOWN_RULE_TYPES:
                        kind = "unknown"
                    else:
                        kind = "condition"
                    rules.append({
                        "type": cond_type,
                        "kind": kind,
                        "label": ROUTINE_RULE_LABELS.get(cond_type),
                        "text": describe_rule(rule, step["SpellName"], condition_map),
                    })
                steps.append({"spellId": step["SpellID"], "spell": step["SpellName"], "rules": rules})
            rotations.append({
                "class": class_name,
                "classColor": class_data["Color"],
                "spec": spec_data["Name"],
                "steps": steps,
            })
    return rotations


def render_page(data_file_name):
    return PAGE_TEMPLATE.replace("__DATA_URL__", json.dumps(data_file_name))


def render_data(rotations, build):
    return json.dumps({"build": build, "rotations": rotations}, ensure_ascii=False, indent=1)


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Assisted Combat Rotations</title>
<script>const whTooltips = {colorLinks: true, iconizeLinks: true, renameLinks: true};</script>
<script src="https://wow.zamimg.com/js/tooltips.js"></script>
<style>
:root {
  --bg: #f6f7f9;
  --surface: #ffffff;
  --text: #1c1f24;
  --muted: #5f6672;
  --border: #dde1e7;
  --accent: #2f5fd0;
  --badge-bg: #eef1f5;
  --badge-text: #4a515c;
  --unknown-bg: #fff3d6;
  --unknown-text: #7a5300;
  --filler-bg: #e3f4ea;
  --filler-text: #1d6b3f;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #15171b;
    --surface: #1e2127;
    --text: #e6e8ec;
    --muted: #9aa1ad;
    --border: #2f343c;
    --accent: #8aa9ff;
    --badge-bg: #2a2f37;
    --badge-text: #c3c8d1;
    --unknown-bg: #3d3014;
    --unknown-text: #f2c96b;
    --filler-bg: #183325;
    --filler-text: #8fd9ad;
  }
}
#rotation {
  --class-accent: color-mix(in srgb, var(--class-color, #888) 72%, #000);
  --class-text: color-mix(in srgb, var(--class-color, #888) 55%, #000);
}
@media (prefers-color-scheme: dark) {
  #rotation { --class-accent: var(--class-color, #888); --class-text: var(--class-color, #888); }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif;
}
main { max-width: 860px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 1.5rem; margin: 0 0 4px; }
.subtitle { color: var(--muted); margin: 0 0 20px; }
.controls {
  display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center;
  padding: 12px 14px; margin-bottom: 16px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
}
select {
  font: inherit; padding: 6px 8px; min-width: 220px; max-width: 100%;
  color: var(--text); background: var(--bg); border: 1px solid var(--border); border-radius: 6px;
}
label { display: inline-flex; gap: 6px; align-items: center; color: var(--muted); }
.notes { color: var(--muted); font-size: 0.9rem; margin: 0 0 20px; }
.spec-title {
  font-size: 1.2rem; margin: 0 0 12px; padding-left: 12px;
  border-left: 6px solid var(--class-accent);
}
.notes p { margin: 4px 0; }
ol.steps { list-style: none; margin: 0; padding: 0; }
.step {
  display: grid; grid-template-columns: 2.5rem 1fr; gap: 0 12px;
  padding: 12px 14px; margin-bottom: 8px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  border-left: 4px solid var(--class-accent);
}
.num { font-size: 1.25rem; font-weight: 600; color: var(--class-text); text-align: right; }
.spell { font-weight: 600; font-size: 1.05rem; }
.spell a { color: var(--accent); text-decoration: none; }
.spell a:hover { text-decoration: underline; }
.spell-id { color: var(--muted); font-weight: 400; font-size: 0.85rem; margin-left: 6px; }
.badges { display: flex; flex-wrap: wrap; gap: 4px; margin: 6px 0 0; }
.badge {
  font-size: 0.78rem; padding: 1px 8px; border-radius: 999px;
  background: var(--badge-bg); color: var(--badge-text);
}
.badge.unknown { background: var(--unknown-bg); color: var(--unknown-text); }
/* Steps gated by type 70, which appears to always fail */
.step.disabled { opacity: 0.55; }
.badge.filler { background: var(--filler-bg); color: var(--filler-text); }
ul.conditions { margin: 6px 0 0; padding-left: 18px; }
ul.conditions li { margin: 2px 0; }
.step.compact .routine-text { display: none; }
.step:not(.compact) .badges .badge.routine { display: none; }
</style>
</head>
<body>
<main>
  <h1>Assisted Combat Rotations</h1>
  <p class="subtitle" id="subtitle">Loading rotation data…</p>
  <div class="controls">
    <select id="spec" aria-label="Class and spec"></select>
    <label><input type="checkbox" id="show-all"> Show every rule as text</label>
  </div>
  <div class="notes">
    <p>Steps are checked top to bottom; the first step whose rules all pass is the one suggested.</p>
    <p>"At least" and "at most" include the value itself.</p>
    <p>Faded steps have a type 70 rule. Its meaning is unknown, but in testing it never passes, so these steps (mostly major cooldowns and movement abilities) appear to be disabled.</p>
  </div>
  <section id="rotation">
    <h2 class="spec-title" id="spec-title"></h2>
    <ol class="steps" id="steps"></ol>
  </section>
</main>
<script>
const DATA_URL = __DATA_URL__;
let data;
const subtitle = document.getElementById("subtitle");
const select = document.getElementById("spec");
const showAll = document.getElementById("show-all");
const list = document.getElementById("steps");
const section = document.getElementById("rotation");
const specTitle = document.getElementById("spec-title");

const key = (r) => `${r.class}/${r.spec}`;

function buildPicker() {
  const byClass = new Map();
  for (const r of data.rotations) {
    if (!byClass.has(r.class)) byClass.set(r.class, []);
    byClass.get(r.class).push(r);
  }
  for (const [className, specs] of byClass) {
    const group = document.createElement("optgroup");
    group.label = className;
    for (const r of specs) group.append(new Option(`${r.spec} ${className}`, key(r)));
    select.append(group);
  }
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function render() {
  const rotation = data.rotations.find((r) => key(r) === select.value) || data.rotations[0];
  section.style.setProperty("--class-color", rotation.classColor);
  specTitle.textContent = `${rotation.spec} ${rotation.class}`;
  list.replaceChildren();
  rotation.steps.forEach((step, i) => {
    const disabled = step.rules.some((rule) => rule.kind === "unknown");
    const item = el("li", "step" + (showAll.checked ? "" : " compact") + (disabled ? " disabled" : ""));
    item.append(el("div", "num", String(i + 1)));
    const body = el("div");

    const title = el("div", "spell");
    const link = el("a", "", step.spell);
    link.href = `https://www.wowhead.com/spell=${step.spellId}`;
    link.target = "_blank";
    link.rel = "noopener";
    title.append(link, el("span", "spell-id", `#${step.spellId}`));
    body.append(title);

    const badges = el("div", "badges");
    const conditions = el("ul", "conditions");
    if (step.rules.length === 0) badges.append(el("span", "badge filler", "Filler: no conditions"));
    for (const rule of step.rules) {
      if (rule.kind === "routine") {
        const badge = el("span", "badge routine", rule.label);
        badge.title = rule.text;
        badges.append(badge);
        conditions.append(el("li", "routine-text", rule.text));
      } else if (rule.kind === "unknown") {
        const badge = el("span", "badge unknown", `Likely disabled (type ${rule.type})`);
        badge.title = rule.text;
        badges.append(badge);
      } else {
        conditions.append(el("li", "", rule.text));
      }
    }
    if (badges.childElementCount) body.append(badges);
    if (conditions.childElementCount) body.append(conditions);
    item.append(body);
    list.append(item);
  });
  // Wowhead only scans links present at page load; rescan the ones just rendered
  if (window.$WowheadPower) window.$WowheadPower.refreshLinks();
}

function selectFromHash() {
  const wanted = decodeURIComponent(location.hash.slice(1));
  if (data.rotations.some((r) => key(r) === wanted)) select.value = wanted;
}

fetch(DATA_URL)
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((loaded) => {
    data = loaded;
    subtitle.textContent = `Build ${data.build}`;
    buildPicker();
    select.addEventListener("change", () => { history.replaceState(null, "", "#" + encodeURIComponent(select.value)); render(); });
    showAll.addEventListener("change", render);
    window.addEventListener("hashchange", () => { selectFromHash(); render(); });
    selectFromHash();
    render();
  })
  .catch((error) => {
    // Browsers block fetch() for pages opened straight from disk (file://)
    subtitle.textContent = `Could not load ${DATA_URL} (${error.message}). ` +
      "If you opened this file directly, serve the folder instead, e.g. python -m http.server";
  });
</script>
</body>
</html>
"""


def parse_args(args):
    parser = argparse.ArgumentParser(description="Write every spec's Assisted Combat rotation to one HTML page")
    parser.add_argument(
        "-b",
        "--build",
        type=str,
        help="Game build of the CSVs in data/csv_table to use (default: newest available)",
    )
    parser.add_argument(
        "-o",
        "--out-file",
        default=DEFAULT_OUT_FILE,
        help=f"File to write (default: {DEFAULT_OUT_FILE})",
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
    build = resolve_build(args.build)
    condition_map = pd.read_csv('data/ConditionTypeMap.csv', quoting=0, engine='python', quotechar='"')
    classes, _ = parse_and_build_db_dumps(build)
    # The data is written beside the page, e.g. out/rotations.html -> out/rotations.json
    data_file = os.path.splitext(args.out_file)[0] + ".json"
    os.makedirs(os.path.dirname(args.out_file) or ".", exist_ok=True)
    with open(data_file, "w", encoding="utf-8") as f:
        f.write(render_data(build_rotations(classes, condition_map), build))
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(render_page(os.path.basename(data_file)))
    print(args.out_file)
    print(data_file)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
