cmake_minimum_required( VERSION 3.19 )
project( InvokeAssembly C )

set( PROJECT_NAME InvokeAssembly )

# set compiler settings
set( CMAKE_C_STANDARD 11 )
set( CMAKE_C_COMPILER x86_64-w64-mingw32-gcc )

# adding module sources
include_directories( include )

set( COMMON_SOURCE
        src/Win32.c
        src/VaelixLdr.c
        src/DllMain.c
        src/Parser.c
        src/InvokeAssembly.c
)


# add compiled module targets
add_executable( ${PROJECT_NAME} ${COMMON_SOURCE} )
