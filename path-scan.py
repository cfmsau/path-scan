#!/usr/bin/env python3
"""
Plex-Ctrl: A colorized CLI toolkit for remote Plex library management.
"""

import sys
import argparse
import urllib.parse
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

# --- ANSI Color Codes ---
class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

# Absolute path ensures logs stay in the repo folder
LOG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plex_tool.log")

def log(msg: str, color=None, file_only=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if msg == "":
        print("")
        return
    raw_output = f"[{timestamp}] {msg}"
    if color:
        formatted_output = f"{Color.BOLD}[{timestamp}]{Color.RESET} {color}{msg}{Color.RESET}"
    else:
        formatted_output = f"[{timestamp}] {msg}"
    if not file_only:
        print(formatted_output)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(raw_output + "\n")
    except IOError:
        pass

def get_libraries(url: str, token: str):
    base_url = url.rstrip('/')
    request_url = f"{base_url}/library/sections?X-Plex-Token={token}"
    headers = {"User-Agent": "Plex-Ctrl-Tool/1.0"}
    try:
        response = requests.get(request_url, headers=headers, timeout=10)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except Exception as e:
        log(f"❌ Connection Error: {e}", color=Color.RED)
    return None

def cmd_list(args):
    log("") 
    root = get_libraries(args.url, args.token)
    if root is None: return
    log(f"Connected to: {args.url}", color=Color.CYAN)
    log("")
    header = f"{'ID':<5} | {'Type':<10} | {'Library Name'}"
    log(header, color=Color.BOLD)
    log("-" * 70)
    for directory in root.findall('Directory'):
        lib_id = directory.get('key')
        lib_type = directory.get('type')
        lib_title = directory.get('title')
        type_color = Color.YELLOW if lib_type == 'show' else Color.BLUE
        log(f"{Color.BOLD}{lib_id:<5}{Color.RESET} | {type_color}{lib_type:<10}{Color.RESET} | {Color.BOLD}{lib_title}{Color.RESET}")
        for loc in directory.findall('Location'):
            log(f"      ↳ Path: {loc.get('path')}")
        log("-" * 35)
    log("")
    print(f"{Color.GREEN}{Color.BOLD}DONE.{Color.RESET}")
    log("")

def cmd_scan(args):
    log("")
    base_url = args.url.rstrip('/')
    target_id = args.id
    # Clean trailing slashes from the target path
    target_path = args.path.rstrip('/')

    if not target_id:
        log(f"🔍 Analyzing path: {target_path}", color=Color.CYAN)
        root = get_libraries(args.url, args.token)
        if root is not None:
            best_match_len = -1
            for directory in root.findall('Directory'):
                for loc in directory.findall('Location'):
                    p = loc.get('path').rstrip('/')
                    if target_path.startswith(p) and len(p) > best_match_len:
                        best_match_len = len(p)
                        target_id = directory.get('key')
                        lib_name = directory.get('title')
            if target_id:
                log(f"🎯 Auto-detected Library: {lib_name} (ID: {target_id})", color=Color.GREEN)
    
    if not target_id:
        log("❌ Error: Path does not match any known Plex library.", color=Color.RED)
        return

    if args.dry_run:
        log(f"🧪 [DRY RUN] Would scan ID {target_id} for path: {target_path}", color=Color.YELLOW)
        print(f"\n{Color.GREEN}DONE.{Color.RESET}")
        return

    refresh_url = f"{base_url}/library/sections/{target_id}/refresh?path={urllib.parse.quote(target_path, safe='')}"
    headers = {"X-Plex-Token": args.token, "User-Agent": "Plex-Ctrl-Tool/1.0"}

    log(f"→ Sending scan request...", color=Color.CYAN)
    try:
        response = requests.get(refresh_url, headers=headers, timeout=10)
        if response.status_code == 200:
            log("✅ Success: Plex accepted the scan request.", color=Color.GREEN)
        else:
            log(f"❌ Failed: Server returned {response.status_code}", color=Color.RED)
    except Exception as e:
        log(f"❌ Error: {e}", color=Color.RED)
    
    log("")
    print(f"{Color.GREEN}{Color.BOLD}DONE.{Color.RESET}")
    log("")

def main():
    parser = argparse.ArgumentParser(description="Plex-Ctrl: Intelligent Remote Scanner")
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_p = subparsers.add_parser('list')
    list_p.add_argument('url')
    list_p.add_argument('token')
    scan_p = subparsers.add_parser('scan')
    scan_p.add_argument('url')
    scan_p.add_argument('token')
    scan_p.add_argument('path')
    scan_p.add_argument('--id')
    scan_p.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.command == 'list': cmd_list(args)
    elif args.command == 'scan': cmd_scan(args)

if __name__ == "__main__":
    main()
