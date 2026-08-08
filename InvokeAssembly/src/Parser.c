
#include <DModule.h>
#include <Parser.h>

VOID ParserNew( PPARSER parser, PCHAR buffer )
{
    UINT32 Size   = 0;

    if ( parser == NULL )
        return;

    memcpy( &Size, buffer, sizeof( UINT32 ) );

    parser->buffer      = buffer + sizeof( UINT32 );
    parser->original    = buffer;
    /* Size is payload length (Packer.p.size), not including this header dword. */
    parser->length      = Size;
}

INT32 ParserGetInt32( PPARSER parser )
{
    INT32 intBytes = 0;

    if ( parser->length < 4 )
        return 0;

    memcpy( &intBytes, parser->buffer, 4 );

    parser->buffer += 4;
    parser->length -= 4;

    return ( INT ) intBytes;
}

PCHAR ParserGetBytes( PPARSER parser, PINT size )
{
    UINT32  length  = 0;
    PCHAR   outdata = NULL;

    if ( parser->length < 4 )
        return NULL;

    memcpy( &length, parser->buffer, 4 );
    parser->buffer += 4;

    outdata = parser->buffer;
    if ( outdata == NULL )
        return NULL;

    parser->length -= 4;
    parser->length -= length;
    parser->buffer += length;

    if ( size != NULL )
        *size = length;

    return outdata;
}