import bpy

class CITY_PT_main_panel(bpy.types.Panel):
    bl_label = "Procedural City Generator"
    bl_idname = "CITY_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CityGen'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj and obj.modifiers and "GeometryNodes" in obj.modifiers:
            node_group = obj.modifiers["GeometryNodes"].node_group
            if node_group:
                layout.label(text="City Parameters")
                for node in node_group.nodes:
                    if node.type == 'FUNCTION' and node.name == "Random Value":
                        layout.prop(node.inputs[1], "default_value", text="Deletion Probability")
                        # Add more controls for other parameters here
            else:
                layout.label(text="No Geometry Node Group found.")
        else:
            layout.label(text="Select the city object with Geometry Nodes.")

def register():
    bpy.utils.register_class(CITY_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(CITY_PT_main_panel)

if __name__ == "__main__":
    register()
