# xander node — research workspace

Multi-project workspace for the **xander** node: a 44-core Xeon E5-2699 v4 with an
NVIDIA CMP 170HX (40 GB), RTX 3060 (12 GB) and RTX 2080 Ti (11 GB).

The stack runs a five-layer tool-calling architecture — **select → admit → synthesise →
verify → record** — plus the training/data pipelines that feed it. See
[`docs/SYSTEM_MAP.md`](docs/SYSTEM_MAP.md) for the full architecture and launch matrix.

---

## Layout

```
~/
├── docs/          Documentation (system map, org conventions, service restore)
├── scripts/       Utility scripts — bench/ gpu/ index/ serve/ train/ diag/ infra/
├── systemd/       Source copies of user unit files (installed: ~/.config/systemd/user/)
├── logs/          Runtime logs (health monitor + rotation)
├── data/          Local data staging (data/local/)
├── archive/       Retired material (2026-10-cleanup/, broken-symlinks/)
│
├── Strata/               Main LLM server (125B MoE, expert tiering VRAM→RAM→SSD)
├── kerv/                 Batched typed-decision engine (L0/L1 gate)
├── kerv-dec/             GPU decode / arithmetic experiments
├── kerv-probe/           GPU probing & benchmarking
├── Open-Jev/             JEV evaluation runtime  (source: src/Open-Jev)
├── sec_caps_train_pkg/   Security-caps classifier head
├── mia-gpu/              LoRA fine-tuning
├── offret/               Contrastive encoder training
├── strip/                Sentinel-gated corpus pipeline
├── rl/                   RLVR (GRPO) training runs
├── forge/                Corpus expansion
├── inv/  system1/  gate/  cluster/  ablit/  aicdl/  TENSELERATE/
├── bench-router/  bench-iq/
├── lab/                  Infrastructure (serve/ infra/ bench/ eval/ …)
├── src/                  Buildable sources
├── third_party/          Vendored deps (llama.cpp)
│
├── models/  venvs/  rl-venv/  jev-checkpoints/  datasets/
├── gpu/  roms/           GPU VBIOS dumps & ROM backups
├── data/  data_scrubbed/  corpus_index_v2/  adapters/  mimo-fleet-train/  rl_runs/   (→ /mnt/archive)
└── Desktop/  Documents/  snap/  …
```

Each project directory carries its own `README.md`.

---

## Entry points at `$HOME`

These are **symlinks** kept at the workspace root so systemd units and ad-hoc shells
resolve stable paths. Do not delete them.

| Entry point | Points to | Used by |
|---|---|---|
| `run_jev_onnx.sh` | `lab/serve/run_jev_onnx.sh` | `jev-onnx.service` (:9114) |
| `run_int8_jev.sh` | `lab/serve/run_int8_jev.sh` | `int8-jev.service` (:8090) |
| `start_27b.sh` | `lab/infra/start_27b.sh` | `llama-27b.service` (:8083) |
| `xander_worker.py` | `lab/serve/xander_worker.py` | `node-x-worker.service` |
| `reflex_server.py` | `lab/serve/reflex_server.py` | `hermes-reflex-x.service` (:9112) |
| `speed_watch.py` | `lab/bench/speed_watch.py` | `speed-watch.service` |
| `forge-disk-guard.sh` | `lab/misc/forge-disk-guard.sh` | `forge-disk-guard.service` |
| `int8_jev_server.py` | `lab/serve/int8_jev_server.py` | jev serve scripts |
| `build_index_gpu.py`, `build_index_gpu2.py` | `scripts/index/…` | `idx-1/2.service` |
| `train_schema_scorer.py` | `scripts/train/…` | `ss-localfit.service` |
| `gpu-power-cap.sh`, `initramfs_mask.sh` | `scripts/gpu/…` | power/modeset scripts |
| `kalm_embed_server.py` | `scripts/serve/…` | `run_kalm_embed.sh` |
| `idx-1.log`, `idx-2.log`, `xander_worker.log`, `forge-guard.log` | `logs/…` | systemd `StandardOutput=append:` |
| `data`, `data_scrubbed`, `corpus_index_v2`, `adapters`, `mimo-fleet-train`, `rl_runs` | `/mnt/archive/xander/…` | bulk storage |

---

## Services

```bash
systemctl --user list-units --type=service | grep -E 'kerv|jev|llama|idx|seccaps|reflex|forge|xander'
```

| Service | Port | Purpose |
|---|---|---|
| `kerv-daemon` | — | Decision engine (L1 admit) |
| `jev-onnx` | 9114 | ONNX schema scorer |
| `seccaps` | 9115 | Security-caps head |
| `hermes-reflex-x` | 9112 | Reflex L0 tool selector |
| `int8-jev` | 8090 | Int8 JEV ONNX |
| `llama-27b` | 8083 | Flagship LLM |
| `idx-1` / `idx-2` | — | Corpus index workers |
| `node-x-worker` | — | Mercury cluster worker |
| `forge-disk-guard` | — | Disk-space watchdog |

---

## Common tasks

```bash
# health snapshot (also runs hourly via cron)
cat logs/mlops_health.log

# restart the decision engine
pkill -f control_daemon; python3 ~/kerv/tools/control_daemon.py &

# Strata / flagship
./start_27b.sh

# evaluate a model
cd ~/src/Open-Jev && python3 -m jev.server --checkpoint ~/models/jev/jev13-ours-2b-bin/checkpoint --port 8791
```

---

## Maintenance

| Automation | Schedule | What it does |
|---|---|---|
| `mlops-health-monitor` | hourly | GPU temp/util, disk %, service state, log sizes |
| `log-rotation-daily` | 02:00 daily | Rotate logs >100 MB, purge >30 d |

Manage with the Hermes `cronjob` tool (`action=list`).

---

## Reorganisation notes (Oct 2026)

Loose scripts that previously sat in `$HOME` were consolidated into `scripts/`; docs →
`docs/`; logs → `logs/`; data dumps → `data/local/`; retired material → `archive/2026-10-cleanup/`.
Compat symlinks (above) preserve every absolute-path reference, so services and scripts
were unaffected. Full move log: `archive/2026-10-cleanup/` and the reorg manifest.

`CANARY-DO-NOT-DELETE` is intentionally left in place.
