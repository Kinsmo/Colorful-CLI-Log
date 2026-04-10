# colorful_cli_log.py ✨🖥️📄

A simple Python tool that reads a plain text terminal log and reconstructs it into a styled HTML page with terminal-like formatting. 🎨

It is designed for logs that have already lost their original ANSI color codes, such as exported `.txt` files from Windows CMD, PowerShell, Codex CLI, or similar tools. 🧩

Instead of restoring the original terminal colors exactly, this script re-renders the log based on text structure and common patterns, producing a clean, readable HTML output. 🌈

---

## 🚀 Features

- ✅ Reconstructs diff-style lines with:
  - green `+` lines ➕🟢
  - red `-` lines ➖🔴
  - line numbers 🔢
  - row background highlighting 🎨
- ✅ Highlights common operation lines such as:
  - `• Edited ...` ✏️
  - `• Ran ...` ▶️
  - `✔ ...` ✔️
- ✅ Preserves tree-style terminal output such as:
  - `│`
  - `└`
  - `├` 🌲
- ✅ Highlights common error and success messages ⚠️✅
- ✅ Outputs a standalone HTML file 🌐
- ✅ No third-party dependencies required 📦

---

## 🤔 Why This Exists

When terminal output is exported as plain text, important visual information is often lost:

- ANSI colors 🎨
- diff highlighting ➕➖
- terminal hierarchy 🌲
- operation markers 🛠️
- readability 👀

This script rebuilds much of that presentation layer heuristically from the text itself. 🧠

It works especially well for logs that contain:

- code diffs 💻
- Codex CLI output 🤖
- PowerShell output ⚡
- Windows CMD logs 🪟
- structured terminal transcripts 📜

---

## 📥 Input and Output

The script reads:
text
log.txt
and generates:

log_rendered.html

You can open the generated HTML file directly in a browser. 🌍

⚡ Usage

Save the script as:

render_log.py

Place your log file in the same directory:

log.txt

Then run:

python render_log.py

After running, the script will generate:

log_rendered.html

Open it in your browser and enjoy a much cleaner view of your terminal log. ✨

⚙️ Configuration

All paths are configured directly inside the script.

Example:

INPUT_FILE = r"log.txt"
OUTPUT_FILE = r"log_rendered.html"
TITLE = "Terminal Log Render"

This project intentionally does not use command-line arguments. 🎯

🔍 Supported Patterns

The renderer currently detects and styles patterns such as:

Diff-like lines ➕➖
56 +                }
57 +            }
8 -@="xxx"
Edited file summary ✏️
• Edited open-in-obsidian-context-menu.reg (+1 -1)
Command execution lines ▶️
• Ran reg import open-in-obsidian-context-menu.reg
Status lines ✅❌
✔ You approved codex to run ...
✖ Something failed
Tree-style terminal output 🌲
└ The operation completed successfully.
│ Additional output...
Error lines ⚠️

Lines containing words like:

error
exception
FullyQualifiedErrorId

will be highlighted as error-related output.

⚠️ Limitations

This script works from plain text only. 📄

That means it cannot truly recover:

original ANSI escape sequences
exact terminal theme colors
original syntax highlighting
exact tool-specific rendering

Instead, it reconstructs the visual structure heuristically from the text content. 🧠

So the result is best understood as:

a styled reconstruction, not a perfect restoration. 🎭

🪟 Best Use Cases

This tool is especially useful if you:

export logs from Windows CMD or PowerShell 🪟
save Codex CLI output as plain text 🤖
want a nicer way to archive terminal sessions 🗂️
want to share readable diffs and logs with others 🤝
need a lightweight log-to-HTML workflow ⚡
📦 Dependencies

None. 🎉

This script uses only Python’s standard library:

html
os
re
pathlib

No pip install required. ✅

🧪 Example Workflow
Save terminal output into log.txt 📝
Run:
python render_log.py
Open:
log_rendered.html
View a much more readable, terminal-like HTML log in your browser 🌈
💡 Notes

This renderer is especially good for reconstructing logs that contain:

diff snippets
command execution traces
terminal tree output
PowerShell error blocks
Codex CLI style transcripts

If your original log already contains ANSI color codes, a different ANSI-to-HTML tool may preserve the original terminal output more accurately. 🎨

This script is mainly for logs where the original colors are already gone. 🧩

📄 License

MIT 📘

