#!/usr/bin/env python3

import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from alive_progress import alive_bar

console = Console()

# -------- Default Config --------
DEFAULT_URL = input("Url : ")
DEFAULT_COUNT = int(input("Reload count : "))
DEFAULT_MIN_DELAY = 1.5
DEFAULT_MAX_DELAY = 3.5
DEFAULT_HEADLESS = False
IMPLICIT_WAIT_SECONDS = 5
# -------------------------------

def make_driver(headless_mode: bool) -> webdriver.Chrome:
    chrome_opts = Options()
    if headless_mode:
        chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--log-level=3")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_opts)
    driver.implicitly_wait(IMPLICIT_WAIT_SECONDS)
    return driver

def run_reload_loop(target_url: str, reload_count: int, delay_min: float, delay_max: float, headless: bool):
    console.print(Panel.fit(
        f"[bold cyan]Reload Automation[/bold cyan]\n"
        f"[white]Target:[/white] {target_url}\n"
        f"[white]Reloads:[/white] {reload_count} | "
        f"[white]Delay:[/white] {delay_min:.2f}-{delay_max:.2f}s | "
        f"[white]Headless:[/white] {headless}",
        border_style="cyan"
    ))

    driver = None
    records = []
    try:
        driver = make_driver(headless)
        driver.get(target_url)
        console.print("[green]Initial page load successful.[/green]\n")

        with alive_bar(reload_count, bar='smooth', spinner='classic', stats=False) as bar:
            for i in range(1, reload_count + 1):
                delay = random.uniform(delay_min, delay_max)
                time.sleep(delay)

                try:
                    driver.refresh()
                    records.append((i, delay, True, "", time.strftime("%H:%M:%S")))
                except Exception as e:
                    records.append((i, delay, False, str(e), time.strftime("%H:%M:%S")))

                bar.text(f"-> Reload {i}/{reload_count}")
                bar()

        table = Table(show_header=True, header_style="bold white", box=box.ROUNDED)
        table.add_column("#", justify="center", style="cyan")
        table.add_column("Time", justify="center", style="white")
        table.add_column("Delay (s)", justify="center")
        table.add_column("Status", justify="center", style="green")
        table.add_column("Error", justify="center", style="red")

        for i, delay, ok, err, ts in records:
            table.add_row(str(i), ts, f"{delay:.2f}", "[green]OK[/green]" if ok else "[red]FAIL[/red]", err or "-")

        console.print(Panel(table, title="[bold green]Reload Summary[/bold green]", border_style="cyan"))

    except Exception as e:
        console.print(f"[bold red]Fatal error:[/bold red] {e}")
    finally:
        if driver:
            driver.quit()
        console.print("[dim]Browser closed. Exiting.[/dim]")

def parse_args():
    parser = argparse.ArgumentParser(description="Reload automation with pretty terminal output.")
    parser.add_argument("--url", "-u", default=DEFAULT_URL, help="Target URL (file:/// or http(s)://).")
    parser.add_argument("--count", "-c", type=int, default=DEFAULT_COUNT, help="Number of reloads to perform.")
    parser.add_argument("--min-delay", type=float, default=DEFAULT_MIN_DELAY, help="Minimum delay between reloads (seconds).")
    parser.add_argument("--max-delay", type=float, default=DEFAULT_MAX_DELAY, help="Maximum delay between reloads (seconds).")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode.")
    return parser.parse_args()

def main():
    args = parse_args()
    run_reload_loop(args.url, args.count, args.min_delay, args.max_delay, args.headless)

if __name__ == "__main__":
    main()
