import bpy
import mathutils

bpy.ops.object.select_all(action='SELECT') 
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'

mountainSize = 5
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

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
<<<<<<< HEAD
cRamp = allNodes.new(type="ShaderNodeValToRGB")
colorRamp = allNodes.new(type="ShaderNodeValToRGB")

textImage.image =bpy.data.images.load(filepath="C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\irland_height_map.png")
=======

cRamp = allNodes.new(type="ShaderNodeValToRGB")

textImage.image = bpy.data.images.load(filepath="D:\Programme\GitHub\Repository\Berggenerator\irland_height_map.png")
>>>>>>> 0d3dfb7364cf3f7cb79d30844052f805de815917
textImage.image.colorspace_settings.name = 'Linear'

mat.node_tree.links.new(disNode.outputs[0], material_output.inputs[2])
mat.node_tree.links.new(textImage.outputs[0], disNode.inputs[0])
mat.node_tree.links.new(textImage.outputs[0], cRamp.inputs[0])
<<<<<<< HEAD
mat.node_tree.links.new(textImage.outputs[0], colorRamp.inputs[0])
mat.node_tree.links.new(cRamp.outputs[0], allNodes["Principled BSDF"].inputs[0])
mat.node_tree.links.new(colorRamp.outputs[0], allNodes["Principled BSDF"].inputs[9])
=======
mat.node_tree.links.new(cRamp.outputs[0], allNodes["Principled BSDF"].inputs[0])
>>>>>>> 0d3dfb7364cf3f7cb79d30844052f805de815917

cRamp.color_ramp.elements[0].position = (0.500)
cRamp.color_ramp.elements[0].color = (0.33,0.1,0,1)
cRamp.color_ramp.elements[1].position = (0.520)
<<<<<<< HEAD

colorRamp.color_ramp.elements[0].position = (0.027)
colorRamp.color_ramp.elements[1].position = (0.482)


=======
>>>>>>> 0d3dfb7364cf3f7cb79d30844052f805de815917
disNode.inputs[2].default_value = 0.3
bpy.context.active_object.data.materials.append(mat)

#bpy.ops.object.shade_smooth()

bpy.ops.object.editmode_toggle()




<<<<<<< HEAD


=======
>>>>>>> 0d3dfb7364cf3f7cb79d30844052f805de815917
