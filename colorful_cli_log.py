import html
import os
import re
from pathlib import Path

# ========= 直接在这里改路径 =========
INPUT_FILE = r"log.txt"
OUTPUT_FILE = r"log_rendered.html"
TITLE = "Terminal Log Render"
# ===================================


def escape(s: str) -> str:
    return html.escape(s, quote=False)


def wrap_span(text: str, cls: str) -> str:
    return f'<span class="{cls}">{escape(text)}</span>'


def render_diff_line(line: str) -> str | None:
    """
    匹配这种行：
        56 +                }
        8 -@="xxx"
    """
    m = re.match(r'^(\s*)(\d+)(\s+)([+-])(\s*)(.*)$', line)
    if not m:
        return None

    indent, lineno, midspace, sign, postspace, content = m.groups()
    sign_cls = "diff-plus" if sign == "+" else "diff-minus"

    return (
        f'<div class="line code {sign_cls}-row">'
        f'{wrap_span(indent, "ws")}'
        f'{wrap_span(lineno, "lineno")}'
        f'{wrap_span(midspace, "ws")}'
        f'{wrap_span(sign, sign_cls)}'
        f'{wrap_span(postspace, "ws")}'
        f'{wrap_span(content, "code-text")}'
        f'</div>'
    )


def render_edited_header(line: str) -> str | None:
    """
    匹配：
    • Edited open-in-obsidian-context-menu.reg (+1 -1)
    """
    m = re.match(r'^(•)\s+(Edited)\s+(.+?)\s+\((\+\d+)\s+(-\d+)\)\s*$', line)
    if not m:
        return None

    bullet, word, filename, addn, deln = m.groups()
    return (
        f'<div class="line edited-header">'
        f'{wrap_span(bullet, "bullet")} '
        f'{wrap_span(word, "edited")} '
        f'{wrap_span(filename, "filename")} '
        f'('
        f'{wrap_span(addn, "diff-plus")} '
        f'{wrap_span(deln, "diff-minus")}'
        f')'
        f'</div>'
    )


def render_ran_header(line: str) -> str | None:
    """
    匹配：
    • Ran reg import xxx
    """
    m = re.match(r'^(•)\s+(Ran)\s+(.+?)\s*$', line)
    if not m:
        return None

    bullet, word, cmd = m.groups()
    return (
        f'<div class="line ran-header">'
        f'{wrap_span(bullet, "bullet")} '
        f'{wrap_span(word, "ran")} '
        f'{wrap_span(cmd, "command")}'
        f'</div>'
    )


def render_generic_bullet(line: str) -> str | None:
    """
    匹配：
    • 注册表命令已经确认...
    """
    m = re.match(r'^(•)\s+(.*)$', line)
    if not m:
        return None

    bullet, rest = m.groups()
    return (
        f'<div class="line bullet-line">'
        f'{wrap_span(bullet, "bullet")} '
        f'{wrap_span(rest, "text")}'
        f'</div>'
    )


def render_check_line(line: str) -> str | None:
    """
    匹配：
    ✔ You approved ...
    """
    m = re.match(r'^(✔|✖)\s+(.*)$', line)
    if not m:
        return None

    symbol, rest = m.groups()
    cls = "ok" if symbol == "✔" else "fail"
    return (
        f'<div class="line {cls}-line">'
        f'{wrap_span(symbol, cls)} '
        f'{wrap_span(rest, "text")}'
        f'</div>'
    )


def render_tree_line(line: str) -> str | None:
    """
    匹配：
      └ The operation completed successfully.
      │ ...
    """
    m = re.match(r'^(\s*)([│└├─]+)(.*)$', line)
    if not m:
        return None

    indent, tree, rest = m.groups()
    extra_cls = "error-text" if "error" in rest.lower() or "exception" in rest.lower() else "text"
    return (
        f'<div class="line tree-line">'
        f'{wrap_span(indent, "ws")}'
        f'{wrap_span(tree, "tree")}'
        f'{wrap_span(rest, extra_cls)}'
        f'</div>'
    )


def render_separator(line: str) -> str | None:
    s = line.strip()
    if s and all(ch in "─—-" for ch in s):
        return f'<div class="line separator">{escape(line)}</div>'
    return None


def render_plain_code(line: str) -> str:
    """
    兜底：普通等宽文本
    """
    cls = "plain"
    lower = line.lower()

    if "error" in lower or "exception" in lower:
        cls = "error-text"
    elif "success" in lower or "completed successfully" in lower or lower == "ok":
        cls = "ok-text"

    return f'<div class="line code {cls}">{escape(line)}</div>'


def render_line(line: str) -> str:
    line = line.rstrip("\n")

    for renderer in (
        render_separator,
        render_edited_header,
        render_ran_header,
        render_check_line,
        render_tree_line,
        render_diff_line,
        render_generic_bullet,
    ):
        out = renderer(line)
        if out is not None:
            return out

    return render_plain_code(line)


def build_html(rendered_lines: list[str], title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<style>
:root {{
    --bg: #0d1117;
    --panel: #161b22;
    --text: #c9d1d9;
    --muted: #8b949e;
    --border: #30363d;
    --green: #3fb950;
    --green-bg: rgba(63, 185, 80, 0.12);
    --red: #f85149;
    --red-bg: rgba(248, 81, 73, 0.12);
    --blue: #79c0ff;
    --cyan: #56d4dd;
    --yellow: #e3b341;
    --purple: #d2a8ff;
    --orange: #ffb86b;
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px;
}}

.header {{
    margin-bottom: 16px;
    padding: 16px 18px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
}}

.header h1 {{
    margin: 0 0 6px 0;
    font-size: 20px;
    color: var(--blue);
}}

.header p {{
    margin: 0;
    color: var(--muted);
    font-size: 13px;
}}

.log {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    padding: 14px 0;
}}

.line {{
    white-space: pre-wrap;
    word-break: break-word;
    padding: 2px 16px;
    line-height: 1.55;
    font-size: 14px;
}}

.line:hover {{
    background: rgba(255,255,255,0.025);
}}

.code {{
    white-space: pre;
    overflow-x: auto;
}}

.separator {{
    color: var(--muted);
}}

.bullet {{
    color: var(--cyan);
    font-weight: 700;
}}

.edited {{
    color: var(--purple);
    font-weight: 700;
}}

.ran {{
    color: var(--blue);
    font-weight: 700;
}}

.filename {{
    color: var(--yellow);
}}

.command {{
    color: var(--text);
}}

.text {{
    color: var(--text);
}}

.tree {{
    color: var(--muted);
}}

.lineno {{
    color: var(--muted);
}}

.diff-plus {{
    color: var(--green);
    font-weight: 700;
}}

.diff-minus {{
    color: var(--red);
    font-weight: 700;
}}

.diff-plus-row {{
    background: linear-gradient(to right, var(--green-bg), transparent 70%);
}}

.diff-minus-row {{
    background: linear-gradient(to right, var(--red-bg), transparent 70%);
}}

.code-text {{
    color: var(--text);
}}

.ok {{
    color: var(--green);
    font-weight: 700;
}}

.fail {{
    color: var(--red);
    font-weight: 700;
}}

.ok-text {{
    color: var(--green);
}}

.error-text {{
    color: var(--red);
}}

.ws {{
    color: transparent;
}}

.footer {{
    color: var(--muted);
    font-size: 12px;
    margin-top: 12px;
    padding-left: 4px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>{html.escape(title)}</h1>
        <p>Rendered from plain text log. Colors are reconstructed heuristically.</p>
    </div>

    <div class="log">
        {"".join(rendered_lines)}
    </div>

    <div class="footer">
        Generated by log renderer
    </div>
</div>
</body>
</html>
"""


def main() -> None:
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"找不到输入文件: {input_path}")

    with input_path.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    rendered = [render_line(line) for line in lines]
    html_doc = build_html(rendered, TITLE)

    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)

    abs_path = os.path.abspath(output_path)
    print(f"已生成: {abs_path}")


if __name__ == "__main__":
    main()
