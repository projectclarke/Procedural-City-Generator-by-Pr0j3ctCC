bl_info = {
    "name": "Procedural City Generator by Pr0j3ctCC",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import random

class ProceduralCityGenerator(bpy.types.Operator):
    bl_idname = "object.procedural_city_generator"
    bl_label = "Generate Procedural City"
    bl_options = {'REGISTER', 'UNDO'}

    city_size: bpy.props.IntProperty(
        name="City Size",
        description="Size of the city (number of blocks)",
        default=10,
        min=1,
        max=100
    )

    road_spacing: bpy.props.IntProperty(
        name="Road Spacing",
        description="Spacing between roads",
        default=2,
        min=1,
        max=10
    )

    building_height_min: bpy.props.FloatProperty(
        name="Min Building Height",
        description="Minimum height of buildings",
        default=1.0,
        min=0.5,
        max=10.0
    )

    building_height_max: bpy.props.FloatProperty(
        name="Max Building Height",
        description="Maximum height of buildings",
        default=3.0,
        min=0.5,
        max=20.0
    )

    vegetation_density: bpy.props.FloatProperty(
        name="Vegetation Density",
        description="Density of vegetation",
        default=0.3,
        min=0.0,
        max=1.0
    )

    def execute(self, context):
        self.generate_city(context)
        return {'FINISHED'}

    def generate_city(self, context):
        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        size = self.city_size
        spacing = self.road_spacing

        for i in range(-size, size):
            for j in range(-size, size):
                if i % spacing == 0 or j % spacing == 0:
                    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(i, j, 0))
                else:
                    height = random.uniform(self.building_height_min, self.building_height_max)
                    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(i, j, height / 2))
                    bpy.context.object.scale.z = height
                    if random.random() < self.vegetation_density:  # Add some trees
                        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, enter_editmode=False, align='WORLD', location=(i, j, height + 0.5))
                        bpy.context.object.location.z = height + 0.5 + 0.2  # Corrected height placement

class ProceduralCityPanel(bpy.types.Panel):
    bl_label = "Procedural City Generator"
    bl_idname = "VIEW3D_PT_procedural_city"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'City Generator'

    def draw(self, context):
        layout = self.layout
        op = layout.operator("object.procedural_city_generator", text="Generate City")
        layout.prop(context.scene, "city_size")
        layout.prop(context.scene, "road_spacing")
        layout.prop(context.scene, "building_height_min")
        layout.prop(context.scene, "building_height_max")
        layout.prop(context.scene, "vegetation_density")

def menu_func(self, context):
    self.layout.operator(ProceduralCityGenerator.bl_idname)

def register():
    bpy.utils.register_class(ProceduralCityGenerator)
    bpy.utils.register_class(ProceduralCityPanel)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Scene.city_size = bpy.props.IntProperty(name="City Size", default=10, min=1, max=100)
    bpy.types.Scene.road_spacing = bpy.props.IntProperty(name="Road Spacing", default=2, min=1, max=10)
    bpy.types.Scene.building_height_min = bpy.props.FloatProperty(name="Min Building Height", default=1.0, min=0.5, max=10.0)
    bpy.types.Scene.building_height_max = bpy.props.FloatProperty(name="Max Building Height", default=3.0, min=0.5, max=20.0)
    bpy.types.Scene.vegetation_density = bpy.props.FloatProperty(name="Vegetation Density", default=0.3, min=0.0, max=1.0)

def unregister():
    bpy.utils.unregister_class(ProceduralCityGenerator)
    bpy.utils.unregister_class(ProceduralCityPanel)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Scene.city_size
    del bpy.types.Scene.road_spacing
    del bpy.types.Scene.building_height_min
    del bpy.types.Scene.building_height_max
    del bpy.types.Scene.vegetation_density

if __name__ == "__main__":
    register()
