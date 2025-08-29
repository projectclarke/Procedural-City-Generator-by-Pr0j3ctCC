bl_info = {
    "name": "Procedural City Generator",
    "blender": (3, 3, 0),
    "category": "Object",
}

import bpy
from .city_generator import create_city_nodes
from .menu import CITY_PT_main_panel

classes = [CITY_PT_main_panel]

def register():
    for cls in classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)
    bpy.app.handlers.load_post.append(create_city_nodes)

def unregister():
    bpy.app.handlers.load_post.remove(create_city_nodes)
    for cls in classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
