
#include <windows.h>
#include <VaelixLdr.h>
#include <stdio.h>

typedef struct _INSTANCE {

    struct {

        WIN32_FUNC( printf )

    } Win32;

    struct {

        PVOID Msvcrt;

    } Modules;

} INSTANCE, *PINSTANCE;

extern INSTANCE Instance;

VOID ModuleInit();
VOID ModuleMain();