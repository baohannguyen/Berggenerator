import bpy
import mathutils

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'

mountainSize = 5
#bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

bpy.ops.mesh.primitive_plane_add(size = mountainSize, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.subdivide(number_cuts=100)
bpy.ops.mesh.subdivide(number_cuts=1)

mat = bpy.data.materials.new(name="mountainTexture")
mat.use_nodes = True
mat.cycles.displacement_method = 'DISPLACEMENT'
allNodes = mat.node_tree.nodes
#Code für die Farbe
#mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0143394, 0.207794, 0.8, 1)
disNode = allNodes.new(type="ShaderNodeDisplacement")
material_output = allNodes.get("Material Output")

textImage = allNodes.new(type="ShaderNodeTexImage")
textImage.image =bpy.data.images.load(filepath="C:\\Users\\ducha\\OneDrive\\Desktop\\Screenshot 2022-11-20 114700.png")
textImage.image.colorspace_settings.name = 'Linear'
mat.node_tree.links.new(disNode.outputs[0], material_output.inputs[2])
mat.node_tree.links.new(textImage.outputs[0], disNode.inputs[0])
disNode.inputs[2].default_value = 0.3
bpy.context.active_object.data.materials.append(mat)
bpy.ops.object.editmode_toggle()





