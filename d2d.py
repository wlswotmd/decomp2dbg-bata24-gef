#
# ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ███╗██████╗ ██████╗ ██████╗ ██████╗  ██████╗
# ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔══██╗╚════██╗██╔══██╗██╔══██╗██╔════╝
# ██║  ██║█████╗  ██║     ██║   ██║██╔████╔██║██████╔╝ █████╔╝██║  ██║██████╔╝██║  ███╗
# ██║  ██║██╔══╝  ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔═══╝ ██║  ██║██╔══██╗██║   ██║
# ██████╔╝███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗██████╔╝██████╔╝╚██████╔╝
# ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚═════╝ ╚═════╝  ╚═════╝
# by mahaloz
#

# discover interface
is_gdb = True
try:
    import gdb
except ImportError:
    is_gdb = False

if is_gdb:
    _globals = globals()
    if "gef" in _globals:
        from decomp2dbg.clients.gdb.gef_client import GEFClient
        GEFClient(register_external_context_pane, gef_print, gef)
    elif "__gef__" in _globals:
        from decomp2dbg.clients.gdb.gef_bata24_client import GEFBata24Client
        GEFBata24Client(gef_print, get_process_maps, get_filepath, ContextCommand, __config__, __gef__)
    elif "pwndbg" in _globals:
        from decomp2dbg.clients.gdb.pwndbg_client import PwndbgClient
        PwndbgClient()
    else:
        from decomp2dbg.clients.gdb.gdb_client import GDBClient
        GDBClient()
else:
    raise Exception("Unsupported debugger type detected, decomp2dbg will not run!")