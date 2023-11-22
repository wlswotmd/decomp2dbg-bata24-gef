from .gdb_client import GDBClient

class GEFBata24Client(GDBClient):
    def __init__(self, gef_print, gef_get_process_maps, gef_get_filepath, gef_ContextCommand, gef_config, gef_ref):
        super(GEFBata24Client, self).__init__()
        
        self.dec_pane.print = gef_print
        self.gef_get_process_maps = gef_get_process_maps
        self.gef_get_filepath = gef_get_filepath
        self.gef_config = gef_config
        self.gef_ContextCommand = gef_ContextCommand
        self.gef_ref = gef_ref
    
    # stolen from https://github.com/hugsy/gef/blob/3b0d9da2b302df4266b70e5f361ab5554f5a17f6/gef.py#L4659
    def update_setting(self, command_obj, name, value, description=None):
        """Update the value of a setting without destroying the description"""
        # make sure settings are always associated to the root command (which derives from GenericCommand)
        if "GenericCommand" not in [x.__name__ for x in command_obj.__class__.__bases__]:
            return

        # key = command_obj.__get_setting_name(name)
        key = f"context.{name}"
        self.gef_config[key][0] = value
        self.gef_config[key][1] = type(value)
        if description:
            self.gef_config[key][3] = description

        # get_gef_setting.cache_clear()
        return
       
    # stolen from https://github.com/hugsy/gef/blob/3b0d9da2b302df4266b70e5f361ab5554f5a17f6/gef.py#L10687
    def add_context_pane(self, pane_name, display_pane_and_title_function):
        """Add a new context pane to ContextCommand."""
        for _, _, class_obj in self.gef_ref.loaded_commands:
            if isinstance(class_obj, self.gef_ContextCommand):
                context_obj = class_obj
                break
        
        # assure users can toggle the new context
        corrected_settings_name = pane_name.replace(" ", "_")
        layout_settings = context_obj.get_setting("layout")
        self.update_setting(context_obj, "layout", "{} {}".format(layout_settings, corrected_settings_name))
        
        # overload the printing of pane title
        context_obj.layout_mapping[corrected_settings_name] = display_pane_and_title_function
        
    def register_decompiler_context_pane(self, decompiler_name):
        self.add_context_pane("decompilation", self.dec_pane.display_pane_and_title)

    def deregister_decompiler_context_pane(self, decompiler_name):
        self.gef_config["context.layout"] = self.gef_config["context.layout"].replace(" decompilation", "")
        
    def find_text_segment_base_addr(self, is_remote=False):        
        maps = self.gef_get_process_maps()

        for sect in maps:
            if sect.path == self.gef_get_filepath():
                return sect.page_start
            
        raise Exception("Unable to find the text segment base addr, please report this! (gef bata24)")
