from .gdb_client import GDBClient

class GEFBata24Client(GDBClient):
    def __init__(self, gef_print, gef_get_codebase, gef_command_instances, gef_config):
        super(GEFBata24Client, self).__init__()
        self.dec_pane.print = gef_print
        self.gef_get_codebase = gef_get_codebase
        self.gef_config = gef_config
        self.gef_command_instances = gef_command_instances

    def add_context_pane(self, pane_name, display_pane_and_title_function):
        """Add a new context pane to ContextCommand."""
        
        context_obj = self.gef_command_instances["context"]
        
        # assure users can toggle the new context
        corrected_settings_name = pane_name.replace(" ", "_")

        layout_settings: str = self.gef_config.get_gef_setting("context.layout")
        self.gef_config.set_gef_setting("context.layout", layout_settings.replace("source", pane_name))
        
        # overload the printing of pane title
        context_obj.layout_mapping[corrected_settings_name] = display_pane_and_title_function

    def register_decompiler_context_pane(self, decompiler_name):
        self.add_context_pane("decompilation", self.dec_pane.display_pane_and_title)

    def deregister_decompiler_context_pane(self, decompiler_name):
        layout_settings: str = self.gef_config.get_gef_setting("context.layout")
        self.gef_config.set_gef_setting("context.layout", layout_settings.replace("decompilation", "source"))

    def find_text_segment_base_addr(self, is_remote=False):        
        return self.gef_get_codebase()
