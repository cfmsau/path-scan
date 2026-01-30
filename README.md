<h1><b> PATH-SCAN v1.0.0</b></h1>

![Build Status](https://github.com/cfmsau/path-scan/actions/workflows/discord.yml/badge.svg)
![Downloads](https://img.shields.io/github/downloads/cfmsau/path-scan/total?color=blueviolet)
![Visitors](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2Fcfmsau%2Fpath-scan.json%3Fcolor%3D263124)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/cfmsau/path-scan/blob/main/LICENSE)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-F16061?logo=ko-fi&logoColor=white)](https://ko-fi.com/cloudfusion)

A lightweight CLI toolkit for remote Plex library management.  
No more hunting for Library IDs—this tool detects them automatically by matching file paths.

Its main purpose, however, is to **perform partial library scans of folders.**  
Looking to scan a single TV show rather than a whole TV library? **USE THIS TOOL.**

Linux release only so far.  
Tested on Debian, Ubuntu & other Linux distros.  
**Just install Python and you're ready to use it!**

---

<h2><b>🚀 QUICK START</b></h2>

1. **Clone the repository:**
<pre>
git clone https://github.com/cfmsau/path-scan.git
cd path-scan
</pre>

2. **Create a Virtual Environment (Recommended):**
<pre>
python3 -m venv venv
source venv/bin/activate
</pre>

3. **Install requirements:**
<pre>
pip install -r requirements.txt
</pre>
or
<pre>
pip install requests
</pre>

4. **Make executable:**
<pre>
chmod +x path-scan.py
</pre>

---

<h2><b>☕ Support this project</b></h2>

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cloudfusion)

---

<h2><b>🛠️ FEATURES</b></h2>

- **Auto-Detection:** Finds Library IDs by matching file paths.
- **Colorized Output:** Visual feedback for Movies (Blue), Shows (Yellow), and Success (Green).
- **VENV Compatible:** Prevents "Externally Managed Environment" errors.
- **Logging:** All actions recorded in a log.

---

<h2><b>🎮 USAGE</b></h2>

*Note: Ensure your venv is active (source venv/bin/activate) before running.*

1. **LIST LIBRARIES:**
<pre>
./path-scan.py list "YOUR_URL" "YOUR_TOKEN"
</pre>

2. **SCAN A FOLDER:**
<pre>
./path-scan.py scan "YOUR_URL" "YOUR_TOKEN" "/path/to/media"
</pre>

3. **DRY RUN (TESTING):**
<pre>
./path-scan.py scan "YOUR_URL" "YOUR_TOKEN" "/path/to/media" --dry-run
</pre>

---

<h2><b>⚡ SPEED TIP: CREATE A BASH FUNCTION (Bash Alias)</b></h2>

To avoid typing your Plex URL and Token every time, you can add functions to your `~/.bashrc`. This allows you to simply type `server1-scan` (followed by the path) or `server1-list` to list all the libraries of the saved server.

**1. Open your bash configuration:**
<pre>nano ~/.bashrc</pre>

**2. Add these function to the bottom of the file:**
<pre>
server1-scan() {
    if [ -z "$1" ]; then
        echo "Usage: server1-scan '/some/media/mount/movies/Movie Name (Year)'"
        return 1
    fi

    # --- CONFIGURATION ---
    local PLEX_URL="http://IP_ADDRESS:32400"
    local PLEX_TOKEN="YOUR_PLEX_TOKEN_HERE"
    local REPO_DIR="YOUR_PATH-SCAN_DIR"
    # ---------------------

    local SCRIPT_PATH="$REPO_DIR/path-scan.py"
    local VENV_PYTHON="$REPO_DIR/venv/bin/python3"

    $VENV_PYTHON "$SCRIPT_PATH" scan "$PLEX_URL" "$PLEX_TOKEN" "$1" "${@:2}"
}
server1-list() {
    local PLEX_URL="http://IP_ADDRESS:32400"
    local PLEX_TOKEN="YOUR_PLEX_TOKEN_HERE"
    local REPO_DIR="YOUR_PATH-SCAN_DIR"

    $REPO_DIR/venv/bin/python3 $REPO_DIR/plex-ctrl.py list "$PLEX_URL" "$PLEX_TOKEN"
    #Usage: server1-list
}

</pre>

NOTE: server1-scan and server1-list can be called anything. They can be server specific. You can make as many aliases as you want.
Also insert your correct values above for PLEX_URL, PLEX_TOKEN and REPO_DIR (install DIR).

**3. Reload your profile:**
<pre>source ~/.bashrc</pre>

**4. Usage:**
Now you can scan any folder with a simple command. Below is an example:
<pre>server1-scan "/mnt/media/movies/The Matrix (1999)"</pre>

Or use server1-list to show all the available libraries on the server:
<pre>server1-list</pre>

---

<h2><b>📸 Screenshots</b></h2>

### **Library Scan in Progress**
{INSERT UPDATED SCREENSHOTS}

### **Detected Library List**
{INSERT UPDATED SCREENSHOTS}

---

<h2><b>🔍 HOW TO FIND YOUR PLEX TOKEN</b></h2>

1. Log into Plex Web (app.plex.tv).
2. Click on any Movie or Episode.
3. Click the "..." (More) button and select "Get Info".
4. Click "View XML" at the bottom left of the window.
5. Look at the URL in your browser's address bar.
6. Copy the string at the very end after `X-Plex-Token=`.

---

<h2><b>⚖️ License</b></h2>

Distributed under the [MIT License](LICENSE). See `LICENSE` for more information.
