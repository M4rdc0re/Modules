# Modules

BOF/DLL modules used by the **Vaelix** teamserver (`ModulesPath`, default `third_party/Modules`).

Vaelix registers these as **native console commands in Go** (no Python). Object files (`.o`) and DLLs under each module are what the implant loads; the `.py` files are reference stubs only (`vaelix_host`).

### Powerpick
Unmanaged PowerShell via DllSpawn.

### InvokeAssembly
.NET assembly execution via DllSpawn (AMSI/ETW patched in the child).

### Template
Base template for writing new modules.

### SituationalAwareness
Situational Awareness beacon object files. From [Situational Awareness BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF)

### RemoteOps
Remote Operation beacon object files. From [Remote Operations BOF](https://github.com/trustedsec/CS-Remote-OPs-BOF)

### Domaininfo
A BOF tool to enumerate domain information using Active Directory Domain Services.
Full credit goes to [Cneelis](https://twitter.com/Cneelis). Bof is from his [C2-Tool-Collection](https://github.com/outflanknl/C2-Tool-Collection)

### Jump-exec psexec
A BOF to lateral move using the psexec technique.

### Jump-exec scshell
A BOF to lateral move using the scshell technique.
This technique relies on ChangeServiceConfigA to run commands (this case our service executable)
This BOF is based on [Mr-Un1k0d3r's](https://twitter.com/MrUn1k0d3r) [SCShell](https://github.com/Mr-Un1k0d3r/SCShell/tree/master/CS-BOF)

### nanorobeus
Kerberos helpers (sessions, tgtdeleg, kerberoast, …).

### Delegation
Find delegation settings, users with SPNs and ASREP using LDAP.

### SamDump
Dump the SAM registry.

### Migrate
Automigrate WoW64 agents to x64.
