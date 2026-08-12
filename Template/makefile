MAKEFLAGS 		+= -s

NAME 			= Template

COMPILER_x86 	= i686-w64-mingw32-gcc
COMPILER_x64 	= x86_64-w64-mingw32-gcc

CFLAGS			=  -Os -fno-asynchronous-unwind-tables -shared -masm=intel
CFLAGS 			+= -fno-ident -fpack-struct=8 -falign-functions=1
CFLAGS  		+= -s -ffunction-sections -falign-jumps=1 -w
CFLAGS			+= -falign-labels=1 -fPIC
CFLAGS			+= -Wl,-s,--no-seh,--enable-stdcall-fixup

INCLUDE			= -I include
SOURCE 			= $(wildcard src/*.c)

# KaynCaller is implemented in C (KaynLdr.c); nasm Util.s is unused.
x64:
	mkdir -p bin
	$(COMPILER_x64) $(INCLUDE) $(SOURCE) $(CFLAGS) -o bin/$(NAME).x64.dll -lntdll -luser32

x86:
	mkdir -p bin
	$(COMPILER_x86) $(INCLUDE) $(SOURCE) $(CFLAGS) -Wno-incompatible-pointer-types -Wno-incompatible-function-pointer-types -Wno-int-conversion -o bin/$(NAME).x86.dll -lntdll -luser32

all: x64
