import bpy

def create_city_nodes(dummy=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.name = "Procedural City"

    modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
    node_group = bpy.data.node_groups.new(name="CityGenerator", type='GeometryNodeTree')
    modifier.node_group = node_group

    nodes = node_group.nodes
    links = node_group.links

    # Create Grid
    grid_node = nodes.new(type="GeometryNodeMeshGrid")
    grid_node.inputs['Size X'].default_value = 15
    grid_node.inputs['Size Y'].default_value = 15
    grid_node.inputs['Vertices X'].default_value = 6
    grid_node.inputs['Vertices Y'].default_value = 6

    # Subdivision Surface
    subdiv_node = nodes.new(type="GeometryNodeSubdivisionSurface")
    subdiv_node.inputs['Level'].default_value = 1

    # Delete Geometry
    delete_node = nodes.new(type="GeometryNodeDeleteGeometry")
    delete_node.domain = 'FACE'

    # Random Value for Deletion
    random_value_node = nodes.new(type="FunctionNodeRandomValue")
    random_value_node.data_type = 'BOOLEAN'
    random_value_node.inputs['Probability'].default_value = 0.5

    # Connect Grid to Subdivision
    links.new(grid_node.outputs['Mesh'], subdiv_node.inputs['Mesh'])

    # Connect Subdivision to Delete Geometry
    links.new(subdiv_node.outputs['Mesh'], delete_node.inputs['Geometry'])

    # Connect Random Value to Delete Geometry
    links.new(random_value_node.outputs['Value'], delete_node.inputs['Selection'])

    # Finally, output the modified geometry
    group_output = nodes.new(type="NodeGroupOutput")
    links.new(delete_node.outputs['Geometry'], group_output.inputs['Geometry'])

    # Optionally: Frame and organize nodes
    frame = nodes.new(type='NodeFrame')
    frame.label = "City Generation"
    for node in [grid_node, subdiv_node, delete_node, random_value_node, group_output]:
        node.parent = frame
