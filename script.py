import bpy
import mathutils
import random

bpy.ops.mesh.primitive_plane_add(size = 1)

bpy.ops.object.mode_set(mode='OBJECT')
for o in bpy.context.scene.objects:
   o.hide_set(False)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()

mountainSize = 2
mountainScale = 5

treeScale = 0.02
grassScale = 0.1

hightmapPath = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\ruap.png"
#"C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\ruap.png"

sceneryTree1Path = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\smalltree.obj"
#"C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\smalltree.obj"

sceneryTree2Path = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\smalltree2.obj"
#"C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\smalltree2.obj"

sceneryGrassPath = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\High_Grass.obj"
#"C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\High_Grass.obj"

baseContext = bpy.context

baseContext.scene.render.engine = 'CYCLES'
baseContext.scene.cycles.device = 'GPU'

bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

bpy.ops.mesh.primitive_plane_add(size = mountainSize, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

mountainPlaneObj = baseContext.active_object
mountainPlaneObj.matrix_local.translation = (0,0,1)
mountainPlaneObj.scale = (mountainScale, mountainScale, mountainScale)

heightTexture = bpy.data.textures.new('textureMountain', type ='IMAGE')
heightTexture.image = bpy.data.images.load(filepath=hightmapPath)
heightTexture.image.colorspace_settings.name = 'Linear'

displacementModif = mountainPlaneObj.modifiers.new("Displace", type='DISPLACE')
displacementModif.texture = heightTexture

bpy.ops.object.shade_smooth()



#Editmode für Subdivide und Texture


bpy.ops.object.editmode_toggle()

bpy.ops.mesh.subdivide(number_cuts=100)
bpy.ops.mesh.subdivide(number_cuts=2)

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

textImage.image = bpy.data.images.load(filepath=hightmapPath)
textImage.image.colorspace_settings.name = 'Linear'


mat.node_tree.links.new(disNode.outputs[0], material_output.inputs[2])
#mat.node_tree.links.new(textImage.outputs[0], disNode.inputs[0])
#mat.node_tree.links.new(textImage.outputs[0], cRamp.inputs[0])
#mat.node_tree.links.new(textImage.outputs[0], colorRamp.inputs[0])
mat.node_tree.links.new(cRamp.outputs[0], allNodes["Principled BSDF"].inputs[0])
mat.node_tree.links.new(colorRamp.outputs[0], allNodes["Principled BSDF"].inputs[9])
bpy.context.active_object.data.materials.append(mat)
cRamp.color_ramp.elements[0].position = (0.600)
cRamp.color_ramp.elements[0].color = (0.33,0.1,0,1)
cRamp.color_ramp.elements[1].position = (0.950)

colorRamp.color_ramp.elements[0].position = (0.027)
colorRamp.color_ramp.elements[1].position = (0.482)

disNode.inputs[2].default_value = 3.3
disNode.inputs[1].default_value = 0



bpy.ops.object.editmode_toggle()

bpy.ops.import_scene.obj(filepath=sceneryTree1Path)
bpy.ops.import_scene.obj(filepath=sceneryTree2Path)
bpy.ops.import_scene.obj(filepath=sceneryGrassPath)

bpy.ops.object.select_all(action='DESELECT')

Tree1 = bpy.data.objects["Tree_1"]
Tree2 = bpy.data.objects["Tree_2"]
Grass = bpy.data.objects["High_Grass"]

Tree1.scale = (treeScale, treeScale, treeScale)

def add_Particle_Scenery(name, number, amount, particleObject):
    mountainPlaneObj.modifiers.new(name, type='PARTICLE_SYSTEM')
    ps = mountainPlaneObj.particle_systems[number].settings
    ps.type ='HAIR'
    ps.use_advanced_hair = True
    ps.render_type = 'OBJECT'
    ps.instance_object = particleObject
    ps.count = amount
    bpy.context.object.particle_systems[name].seed = random.randint(0, 100)

add_Particle_Scenery("treeParticles", 0, 1000, Tree1)
add_Particle_Scenery("grassParticles", 1, 1000, Grass)

Tree1.hide_set(state=True)
Tree2.hide_set(state=True)
Grass.hide_set(state=True)
