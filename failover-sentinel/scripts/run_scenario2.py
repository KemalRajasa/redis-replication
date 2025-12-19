#!/usr/bin/env python3
"""
Automation helper for Skenario 2 (Redis Sentinel failover).

The script orchestrates the following steps:
1. (Optional) Ensure all containers from docker-compose.yml are running.
2. Validate Sentinel quorum.
3. Generate continuous SET workload via the redis-client container.
4. Stop the redis-master container to trigger failover.
5. Wait until a replica becomes the new master and resume writes.
6. Emit metrics + logs so they can be pasted into the report.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import shlex
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import List, Optional

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
COMPOSE_FILE = PROJECT_ROOT / "docker-compose.yml"
DEFAULT_COMPOSE_CMD = os.environ.get("DOCKER_COMPOSE", "docker compose")
COMPOSE_BASE = shlex.split(DEFAULT_COMPOSE_CMD)
TARGET_SERVICES = ["redis-master", "redis-replica-1", "redis-replica-2"]


class ScenarioError(RuntimeError):
    """Custom error to make handling explicit."""


def run_command(cmd: List[str], *, capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Wrapper around subprocess.run with text output enabled by default."""
    try:
        return subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check,
        )
    except FileNotFoundError as exc:
        raise ScenarioError(f"Command {cmd[0]!r} not found. Please ensure Docker/Compose is installed.") from exc


def compose_cmd(*args: str, capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run docker compose with the project compose file."""
    cmd = COMPOSE_BASE + list(args)
    env = os.environ.copy()
    # Force Compose to read the correct file even if user runs from elsewhere.
    env["COMPOSE_FILE"] = str(COMPOSE_FILE)
    return run_command(cmd, capture_output=capture_output, check=check)


def wait_for_quorum(timeout: int, log) -> None:
    """Wait until sentinel-1 reports the requested quorum."""
    log("Menunggu quorum Sentinel (ckquorum)...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = compose_cmd(
            "exec",
            "-T",
            "sentinel-1",
            "redis-cli",
            "-p",
            "26379",
            "SENTINEL",
            "ckquorum",
            "mymaster",
            check=False,
        )
        output = (result.stdout or "").strip()
        if result.returncode == 0 and output.startswith("OK"):
            log(f"Sentinel quorum siap: {output}")
            return
        time.sleep(2)
    raise ScenarioError("Sentinel quorum tidak pernah siap dalam batas waktu.")


def detect_master_service(log, skip: Optional[str] = None) -> Optional[str]:
    """Return the docker-compose service name whose role is master."""
    for service in TARGET_SERVICES:
        if skip and service == skip:
            continue
        result = compose_cmd(
            "exec",
            "-T",
            service,
            "redis-cli",
            "INFO",
            "replication",
            check=False,
        )
        if result.returncode != 0:
            continue
        info = result.stdout or ""
        if "role:master" in info:
            return service
    log("Belum menemukan master baru, Sentinel masih melakukan failover...")
    return None


def stop_master(log) -> None:
    """Stop the original master container."""
    log("Mematikan redis-master untuk memicu failover...")
    compose_cmd("stop", "redis-master", capture_output=False)


def tail_logs(service: str, lines: int = 50) -> str:
    """Return the recent logs of a service."""
    result = compose_cmd("logs", f"--tail={lines}", service, check=False)
    return result.stdout or ""


@dataclass
class ScenarioMetrics:
    """Minimal metrics recorded during the run."""

    failure_triggered_at: Optional[float] = None
    first_failed_write_at: Optional[float] = None
    recovery_write_at: Optional[float] = None
    new_master_identified_at: Optional[float] = None
    promoted_service: Optional[str] = None
    current_target: str = "redis-master"
    lock: threading.Lock = field(default_factory=threading.Lock)

    def get_target(self) -> str:
        with self.lock:
            return self.current_target

    def set_target(self, service: str) -> None:
        with self.lock:
            self.current_target = service


def workload_loop(
    stop_event: threading.Event,
    log,
    metrics: ScenarioMetrics,
    interval: float,
) -> None:
    """Continuously send SET commands through redis-client."""
    attempt = 0
    while not stop_event.is_set():
        attempt += 1
        target_service = metrics.get_target()
        key = f"failover:key:{attempt}"
        value = f"{time.time():.6f}"
        result = compose_cmd(
            "exec",
            "-T",
            "redis-client",
            "redis-cli",
            "-h",
            target_service,
            "-p",
            "6379",
            "SET",
            key,
            value,
            check=False,
        )
        now = time.time()
        if result.returncode == 0 and "OK" in (result.stdout or ""):
            if (
                metrics.failure_triggered_at
                and metrics.first_failed_write_at
                and not metrics.recovery_write_at
            ):
                metrics.recovery_write_at = now
                log(f"WRITE #{attempt} sukses lagi -> {target_service} (pemulihan {now - metrics.failure_triggered_at:.2f}s)")
            else:
                log(f"WRITE #{attempt} OK -> {target_service}")
        else:
            if metrics.failure_triggered_at and not metrics.first_failed_write_at:
                metrics.first_failed_write_at = now
            log_msg = (result.stderr or result.stdout or "unknown error").strip()
            log(f"WRITE #{attempt} GAGAL -> {target_service} | {log_msg}")
        time.sleep(interval)


def summarize(metrics: ScenarioMetrics, log) -> None:
    """Print a short summary for human consumption."""
    log("--- Ringkasan ---")
    if metrics.promoted_service:
        log(f"Master baru: {metrics.promoted_service}")
    if metrics.failure_triggered_at and metrics.recovery_write_at:
        duration = metrics.recovery_write_at - metrics.failure_triggered_at
        log(f"Waktu dari master mati ke write pulih: {duration:.2f} detik")
    if metrics.first_failed_write_at and metrics.failure_triggered_at:
        lag = metrics.first_failed_write_at - metrics.failure_triggered_at
        log(f"Lag antara failure trigger dan WRITE pertama yang gagal: {lag:.2f} detik")
    if metrics.new_master_identified_at and metrics.failure_triggered_at:
        leader_election = metrics.new_master_identified_at - metrics.failure_triggered_at
        log(f"Durasi failover menurut Sentinel: {leader_election:.2f} detik")


def ensure_directories() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo otomatis failover Sentinel (Skenario 2).")
    parser.add_argument("--failure-delay", type=float, default=10.0, help="Detik sebelum master dimatikan.")
    parser.add_argument("--writes-per-second", type=float, default=5.0, help="Frekuensi workload SET.")
    parser.add_argument("--post-failover", type=float, default=10.0, help="Berapa detik workload berjalan setelah master baru siap.")
    parser.add_argument("--quorum-timeout", type=int, default=60, help="Batas waktu menunggu sentinel ckquorum.")
    parser.add_argument("--failover-timeout", type=int, default=120, help="Batas waktu menunggu master baru.")
    parser.add_argument("--skip-up", action="store_true", help="Lewati docker compose up -d (gunakan cluster yang sudah berjalan).")
    parser.add_argument("--teardown", action="store_true", help="Matikan seluruh stack (docker compose down) setelah skenario.")
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    ensure_directories()
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"scenario2-{timestamp}.log"
    log_file = log_path.open("w", encoding="utf-8")

    def log(message: str) -> None:
        ts = dt.datetime.now().isoformat(timespec="seconds")
        line = f"[{ts}] {message}"
        print(line)
        log_file.write(line + "\n")
        log_file.flush()

    interval = 1.0 / max(args.writes_per_second, 0.1)
    log(f"Menjalankan skenario 2 dengan interval workload {interval:.2f}s.")

    if not COMPOSE_FILE.exists():
        raise ScenarioError(f"Tidak menemukan docker-compose.yml di {COMPOSE_FILE}.")

    if not args.skip_up:
        log("Menyalakan seluruh stack docker compose...")
        compose_cmd("up", "-d")

    wait_for_quorum(args.quorum_timeout, log)

    metrics = ScenarioMetrics()

    stop_event = threading.Event()
    worker = threading.Thread(
        target=workload_loop,
        args=(stop_event, log, metrics, interval),
        daemon=True,
    )
    worker.start()

    log(f"Workload berjalan. Akan memicu failure dalam {args.failure_delay:.1f} detik.")
    time.sleep(args.failure_delay)
    metrics.failure_triggered_at = time.time()
    stop_master(log)

    log("Menunggu Sentinel memilih master baru...")
    end_time = time.time() + args.failover_timeout
    new_master = None
    while time.time() < end_time:
        master = detect_master_service(log, skip="redis-master")
        if master:
            new_master = master
            metrics.promoted_service = master
            metrics.new_master_identified_at = time.time()
            metrics.set_target(master)
            log(f"Sentinel menunjuk {master} sebagai master baru.")
            break
        time.sleep(2)
    if not new_master:
        stop_event.set()
        worker.join(timeout=5)
        raise ScenarioError("Timeout menunggu master baru dari Sentinel.")

    log(f"Menunggu workload berjalan selama {args.post_failover:.1f} detik setelah failover.")
    time.sleep(args.post_failover)
    stop_event.set()
    worker.join(timeout=5)

    summarize(metrics, log)
    log("\n--- Cuplikan log sentinel-1 ---")
    log(tail_logs("sentinel-1"))

    if args.teardown:
        log("Melakukan docker compose down...")
        compose_cmd("down", "-v", capture_output=False)

    log(f"Log lengkap tersimpan di {log_path}")
    log_file.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ScenarioError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        raise SystemExit(1)
