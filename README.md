# Vaelix Modules

BOF and DllSpawn objects for the **[Vaelix](https://github.com/M4rdc0re/Vaelix)** teamserver (`Teamserver.ModulesPath`, default `third_party/Modules` in the Vaelix tree).

Fork of [HavocFramework/Modules](https://github.com/HavocFramework/Modules), maintained for Vaelix. Authorized red team / penetration testing use only. BOF/COFF loading is **Windows-only**.

Vaelix registers these as **native console commands in Go** (`teamserver/internal/modules`). The implant loads object files (`.o`) and DLLs. The `.py` files are **reference stubs** only (`vaelix_host.py`); they are not executed.

Operator catalog, packing, and limits: [Vaelix `docs/modules.md`](https://github.com/M4rdc0re/Vaelix/blob/master/docs/modules.md). Type `help` in the session console for the merged verb list.

## Clone

This repository is a git submodule of Vaelix, and it **nests further submodules** (TrustedSec / Fortra sources):

```bash
# From a Vaelix clone
git submodule update --init --recursive

# Standalone
git clone --recurse-submodules https://github.com/M4rdc0re/Modules
```

Nested:

| Path | Upstream |
|------|----------|
| `SituationalAwareness/CS-Situational-Awareness-BOF` | [trustedsec/CS-Situational-Awareness-BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF) |
| `RemoteOps/CS-Remote-OPs-BOF` | [trustedsec/CS-Remote-OPs-BOF](https://github.com/trustedsec/CS-Remote-OPs-BOF) |
| `nanodump/nanodump` | [fortra/nanodump](https://github.com/fortra/nanodump) |
| `NoConsolation/No-Consolation` | [fortra/No-Consolation](https://github.com/fortra/No-Consolation) |

A plain clone without `--recurse-submodules` leaves those source trees empty. Prebuilt objects under `ObjectFiles/` / `bin/` may still be present in this repo.

## Layout (what Vaelix loads)

Paths are relative to `ModulesPath`. Arch is `x64` or `x86` from the agent. `{name}` is the BOF/DLL stem (for example `whoami`, `PowerPick`).

| Directory | Console (Vaelix) | Artifacts |
|-----------|------------------|-----------|
| **SituationalAwareness** | `arp`, `whoami`, `ipconfig`, `netstat`, `reg_query`, `ldapsearch`, `tasklist`, ... | `ObjectFiles/{name}.{arch}.o` |
| **RemoteOps** | `adduser`, `sc_create`, `reg_set`, `adcs_request`, ... | `bin/{name}.{arch}.o` |
| **Bofbelt** | `bofbelt` (chains ~38 SA BOFs) | `ObjectFiles/{name}.{arch}.o` — falls back to SA `ObjectFiles/` if missing |
| **Domaininfo** | `dcenum` | `Domaininfo.o` (x64 only) |
| **Jump-exec** | `jump-exec psexec` / `scshell` / `wmi-eventsub` / `wmi-proccreate` | `Psexec/psexec.{arch}.o`, `ScShell/scshell.{arch}.o`, `WMI/EventSub/bin/EventSub.{arch}.o`, `WMI/ProcCreate/bin/ProcCreate.{arch}.o` |
| **Delegation** | `get-delegation`, `get-spns`, `get-asrep` | `bin/ldapsearch.{arch}.o` |
| **nanorobeus** | `sessions`, `tgtdeleg`, `kerberoast` | `bin/nanorobeus.{arch}.o` |
| **nanodump** | `nanodump`, `nanodump_ppl_dump`, `nanodump_ppl_medic`, `nanodump_ssp` | `bin/nanodump.{arch}.o` (+ companion `.dll` for PPL/SSP variants) |
| **SamDump** | `samdump` | `regdump.{arch}.o` |
| **mimidrv** | `mimidrv` | `dist/mimidrv.x64.o` |
| **NoConsolation** | `noconsolation` | `bin/NoConsolation.{arch}.o` |
| **PowerPick** | `powerpick` | `bin/PowerPick.{arch}.dll` (DllSpawn) |
| **InvokeAssembly** | `dotnet execute` | `bin/InvokeAssembly.{arch}.dll` (DllSpawn). Builtin `dotnet inline-execute` is in-process CLR, not this DLL. |
| **Template** | — | Skeleton for a new DllSpawn module (`VaelixLdr` + MinGW cmake) |

Sanity check after clone:

```bash
ls SituationalAwareness/ObjectFiles/whoami.x64.o
ls PowerPick/bin/PowerPick.x64.dll
```

If `whoami.x64.o` is missing, the Vaelix teamserver logs a warning at startup and `whoami` falls back to the builtin username job.

## Not loaded by Vaelix

These remain in-tree as historical stubs. The teamserver implements the same behaviour in Go:

| Path | Vaelix equivalent |
|------|-------------------|
| `Migrate/auto_migrate.py` | WoW64 auto-migrate: teamserver enqueues `inject spawn` of an x64 PIC baked from a live HTTP(S) listener |
| `Packer/packer.py` | `teamserver/internal/modules/packer.go` (BOF argument buffers) |

## Build

Prebuilt objects ship for the verbs Vaelix registers. To rebuild from source (MinGW-w64):

```bash
git submodule update --init --recursive
make
```

The root makefile walks each subdirectory that has a `makefile` / `Makefile` (skips `Template`). PowerPick / InvokeAssembly / Template also have CMake (`x86_64-w64-mingw32-gcc`). Upstream trees (nanodump, No-Consolation, TrustedSec BOFs) keep their own build docs.

## Credits

- Situational Awareness / Remote Ops BOFs: [TrustedSec](https://github.com/trustedsec)
- Domaininfo: [Cneelis](https://twitter.com/Cneelis) / [Outflank C2-Tool-Collection](https://github.com/outflanknl/C2-Tool-Collection)
- Jump-exec scshell: [Mr-Un1k0d3r SCShell](https://github.com/Mr-Un1k0d3r/SCShell/tree/master/CS-BOF)
- nanodump / No-Consolation: [Fortra](https://github.com/fortra)
- nanorobeus, Delegation, SamDump, mimidrv, Jump-exec psexec/WMI: see each subdirectory
