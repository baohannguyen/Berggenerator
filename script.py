import bpy
import mathutils

bpy.ops.object.select_all(action='SELECT') 
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'


mountainSize = 2
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))


bpy.ops.mesh.primitive_plane_add(size = mountainSize, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
obj = bpy.context.active_object

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.subdivide(number_cuts=100)
bpy.ops.mesh.subdivide(number_cuts=1)

obj.scale = (5, 5, 5)
mat = bpy.data.materials.new(name="mountainTexture")
mat.use_nodes = True
mat.cycles.displacement_method = 'DISPLACEMENT'
allNodes = mat.node_tree.nodes


#Code für die Farbe
#mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0143394, 0.207794, 0.8, 1)
disNode = allNodes.new(type="ShaderNodeDisplacement")
material_output = allNodes.get("Material Output")
textImage = allNodes.new(type="ShaderNodeTexImage")
cRamp = allNodes.new(type="ShaderNodeValToRGB")
colorRamp = allNodes.new(type="ShaderNodeValToRGB")

textImage.image =bpy.data.images.load(filepath="C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\ruap.png")
textImage.image.colorspace_settings.name = 'Linear'
heightTexture = bpy.data.textures.new('textureMountain', type ='IMAGE')
heightTexture.image = textImage.image
dispMod = obj.modifiers.new("Displace", type='DISPLACE')
dispMod.texture = heightTexture


mat.node_tree.links.new(disNode.outputs[0], material_output.inputs[2])
#mat.node_tree.links.new(textImage.outputs[0], disNode.inputs[0])
#mat.node_tree.links.new(textImage.outputs[0], cRamp.inputs[0])
#mat.node_tree.links.new(textImage.outputs[0], colorRamp.inputs[0])
mat.node_tree.links.new(cRamp.outputs[0], allNodes["Principled BSDF"].inputs[0])
mat.node_tree.links.new(colorRamp.outputs[0], allNodes["Principled BSDF"].inputs[9])

cRamp.color_ramp.elements[0].position = (0.600)
cRamp.color_ramp.elements[0].color = (0.33,0.1,0,1)
cRamp.color_ramp.elements[1].position = (0.950)

colorRamp.color_ramp.elements[0].position = (0.027)
colorRamp.color_ramp.elements[1].position = (0.482)


disNode.inputs[2].default_value = 3.3
disNode.inputs[1].default_value = 0

obj.modifiers.new("ps", type='PARTICLE_SYSTEM')
ps= obj.particle_systems[0].settings
ps.type ='HAIR'
ps.use_advanced_hair = True
ps.render_type = 'COLLECTION'
bpy.ops.import_scene.obj(filepath="C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\smalltree.obj")
bpy.ops.import_scene.obj(filepath="C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\smalltree2.obj")

bpy.context.active_object.data.materials.append(mat)

#bpy.ops.object.shade_smooth()

bpy.ops.object.editmode_toggle()
