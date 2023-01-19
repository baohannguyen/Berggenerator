import bpy
import mathutils
import random

import numpy as np

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

#hightmapPath = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\ruap.png"
hightmapPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\ruap.png"

#sceneryTree1Path = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\smalltree.obj"
sceneryTree1Path = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\smalltree.obj"

#sceneryTree2Path = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\smalltree2.obj"
sceneryTree2Path = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\smalltree2.obj"

#sceneryGrassPath = "D:\\Programme\\GitHub\\Repository\\Berggenerator\\High_Grass.obj"
sceneryGrassPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\High_Grass.obj"

rockNormalPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\rock_normal.jpg"

rockRoughnessPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\rock_roughness.jpg"

rockBaseColorPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\rock_basecolor.jpg"

rockambOcclusionPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\rock_ambientOcclusion.jpg"

snowNormalPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\snow_normal.jpg"

snowRoughnessPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\snow_roughness.jpg"

snowBaseColorPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\snow_basecolor.jpg"

snowambOcclusionPath = "C:\\Users\\ducha\\OneDrive\\Dokumente\\GitHub\\Berggenerator\\snow_ambientOcclusion.jpg"

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


bpy.ops.object.editmode_toggle()

bpy.ops.mesh.subdivide(number_cuts=100)
bpy.ops.mesh.subdivide(number_cuts=2)


heightmapImage = heightTexture.image
pixels = np.array(heightmapImage.pixels)
heightmap = np.reshape(pixels, (heightmapImage.size[1], heightmapImage.size[0], -1))
gradients = np.gradient(heightmap)


vertex_group = mountainPlaneObj.vertex_groups.new(name="Gradient")

threshold = 0.5


print("WWWWWWWWWWWWWWWW")
print(heightmap)

mat = bpy.data.materials.new(name="mountainTexture")
mat.use_nodes = True
mat.cycles.displacement_method = 'DISPLACEMENT'
allNodes = mat.node_tree.nodes


#Code fÃ¼r die Farbe
#mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0143394, 0.207794, 0.8, 1)

principledRock = allNodes.new(type="ShaderNodeBsdfPrincipled")
principledSnow = allNodes.new(type="ShaderNodeBsdfPrincipled")
material_output = allNodes.new(type="ShaderNodeOutputMaterial")
materialRock = allNodes.new(type="ShaderNodeOutputMaterial")
materialSnow = allNodes.new(type="ShaderNodeOutputMaterial")
textImage = allNodes.new(type="ShaderNodeTexImage")
rockNormal = allNodes.new(type="ShaderNodeTexImage")
rockRoughness = allNodes.new(type="ShaderNodeTexImage")
rockBaseColor = allNodes.new(type="ShaderNodeTexImage")
rockambOcclusion = allNodes.new(type="ShaderNodeTexImage")
snowNormal = allNodes.new(type="ShaderNodeTexImage")
snowRoughness = allNodes.new(type="ShaderNodeTexImage")
snowBaseColor = allNodes.new(type="ShaderNodeTexImage")
snowambOcclusion = allNodes.new(type="ShaderNodeTexImage")
cRamp = allNodes.new(type="ShaderNodeValToRGB")
#colorRamp = allNodes.new(type="ShaderNodeValToRGB")
bump = allNodes.new(type="ShaderNodeBump")
separateColor = allNodes.new(type="ShaderNodeSeparateColor")
mixShader = allNodes.new(type="ShaderNodeMixShader")
texCoordinateRock = allNodes.new(type="ShaderNodeTexCoord")
texCoordinateSnow = allNodes.new(type="ShaderNodeTexCoord")
mappingRock = allNodes.new(type="ShaderNodeMapping")
mappingSnow = allNodes.new(type="ShaderNodeMapping")
normalMapRock = allNodes.new(type="ShaderNodeNormalMap")
normalMapSnow = allNodes.new(type="ShaderNodeNormalMap")
mixColorRock = allNodes.new(type="ShaderNodeMix")
mixColorSnow = allNodes.new(type="ShaderNodeMix")


rockNormal.image = bpy.data.images.load(filepath=rockNormalPath)
rockNormal.image.colorspace_settings.name = 'Non-Color'
rockRoughness.image = bpy.data.images.load(filepath=rockRoughnessPath)
rockRoughness.image.colorspace_settings.name = 'Non-Color'
rockBaseColor.image = bpy.data.images.load(filepath=rockBaseColorPath)
rockBaseColor.image.colorspace_settings.name = 'sRGB'
rockambOcclusion.image = bpy.data.images.load(filepath=rockambOcclusionPath)
rockambOcclusion.image.colorspace_settings.name = 'Non-Color'

snowNormal.image = bpy.data.images.load(filepath=snowNormalPath)
snowNormal.image.colorspace_settings.name = 'Non-Color'
snowRoughness.image = bpy.data.images.load(filepath=snowRoughnessPath)
snowRoughness.image.colorspace_settings.name = 'Non-Color'
snowBaseColor.image = bpy.data.images.load(filepath=snowBaseColorPath)
snowBaseColor.image.colorspace_settings.name = 'sRGB'
snowambOcclusion.image = bpy.data.images.load(filepath=snowambOcclusionPath)
snowambOcclusion.image.colorspace_settings.name = 'Non-Color'

textImage.image = bpy.data.images.load(filepath=hightmapPath)
textImage.image.colorspace_settings.name = 'Linear'

mixColorRock.data_type = 'RGBA'
mixColorRock.blend_type = 'ADD'
mixColorRock.inputs[6].default_value = (0.049, 0.049, 0.049, 1)

mixColorSnow.data_type = 'RGBA'
mixColorSnow.blend_type = 'ADD'
mixColorSnow.inputs[6].default_value = (0.367, 0.367, 0.367, 1)


#mat.node_tree.links.new(textImage.outputs[0], cRamp.inputs[0])
#mat.node_tree.links.new(textImage.outputs[0], colorRamp.inputs[0])
#mat.node_tree.links.new(cRamp.outputs[0], allNodes["Principled BSDF"].inputs[0])
#mat.node_tree.links.new(colorRamp.outputs[0], allNodes["Principled BSDF"].inputs[9])

#Mountain Texture
mat.node_tree.links.new(separateColor.outputs[2], cRamp.inputs[0])
mat.node_tree.links.new(bump.outputs[0], separateColor.inputs[0])
mat.node_tree.links.new(cRamp.outputs[0], mixShader.inputs[0])
mat.node_tree.links.new(mixShader.outputs[0], material_output.inputs[0])

mat.node_tree.links.new(texCoordinateRock.outputs[0], mappingRock.inputs[0])
mat.node_tree.links.new(mappingRock.outputs[0], rockNormal.inputs[0])
mat.node_tree.links.new(rockNormal.outputs[0], normalMapRock.inputs[1])
mat.node_tree.links.new(normalMapRock.outputs[0], principledRock.inputs[22])
mat.node_tree.links.new(mappingRock.outputs[0], rockRoughness.inputs[0])
mat.node_tree.links.new(rockRoughness.outputs[0], principledRock.inputs[9])
mat.node_tree.links.new(principledRock.outputs[0], materialRock.inputs[0])
mat.node_tree.links.new(mappingRock.outputs[0], rockBaseColor.inputs[0])
mat.node_tree.links.new(mappingRock.outputs[0], rockambOcclusion.inputs[0])
mat.node_tree.links.new(rockBaseColor.outputs[0], mixColorRock.inputs[7])
mat.node_tree.links.new(rockambOcclusion.outputs[0], mixColorRock.inputs[0])
mat.node_tree.links.new(mixColorRock.outputs[2], principledRock.inputs[0])
mat.node_tree.links.new(principledRock.outputs[0], mixShader.inputs[1])

mat.node_tree.links.new(texCoordinateSnow.outputs[0], mappingSnow.inputs[0])
mat.node_tree.links.new(mappingSnow.outputs[0], snowNormal.inputs[0])
mat.node_tree.links.new(snowNormal.outputs[0], normalMapSnow.inputs[1])
mat.node_tree.links.new(normalMapSnow.outputs[0], principledSnow.inputs[22])
mat.node_tree.links.new(mappingSnow.outputs[0], snowRoughness.inputs[0])
mat.node_tree.links.new(snowRoughness.outputs[0], principledSnow.inputs[9])
mat.node_tree.links.new(principledSnow.outputs[0], materialSnow.inputs[0])
mat.node_tree.links.new(mappingSnow.outputs[0], snowBaseColor.inputs[0])
mat.node_tree.links.new(mappingSnow.outputs[0], snowambOcclusion.inputs[0])
mat.node_tree.links.new(snowBaseColor.outputs[0], mixColorSnow.inputs[7])
mat.node_tree.links.new(snowambOcclusion.outputs[0], mixColorSnow.inputs[0])
mat.node_tree.links.new(mixColorSnow.outputs[2], principledSnow.inputs[0])
mat.node_tree.links.new(principledSnow.outputs[0], mixShader.inputs[2])
bpy.context.active_object.data.materials.append(mat)

cRamp.color_ramp.elements[0].position = (0.645)
cRamp.color_ramp.elements[0].color = (0.077,0.078,0.079,1)
cRamp.color_ramp.elements[1].position = (0.905)

mappingRock.inputs[3].default_value[0] = 12
mappingRock.inputs[3].default_value[1] = 12
mappingRock.inputs[3].default_value[2] = 12

mappingSnow.inputs[3].default_value[0] = 3
mappingSnow.inputs[3].default_value[1] = 3
mappingSnow.inputs[3].default_value[2] = 3

#colorRamp.color_ramp.elements[0].position = (0.027)
#colorRamp.color_ramp.elements[1].position = (0.482)

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

Tree1.scale = (treeScale, treeScale, treeScale)


class MoreSnow (bpy.types.Operator):
    bl_idname = "wm.moresnow"
    bl_label = "MoreSnow"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        cRamp.color_ramp.elements[0].position = cRamp.color_ramp.elements[0].position - 0.1

        return {'FINISHED'}

class LessSnow (bpy.types.Operator):
    bl_idname = "wm.lesssnow"
    bl_label = "Less Snow"

    def execute(self, context):
        # Report "Hello World" to the Info Area
        cRamp.color_ramp.elements[0].position = cRamp.color_ramp.elements[0].position + 0.1

        return {'FINISHED'}

add_Particle_Scenery("treeParticles", 0, 1000, Tree1)
add_Particle_Scenery("grassParticles", 1, 1000, Grass)

bpy.utils.register_class(MoreSnow)
bpy.utils.register_class(LessSnow)

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text= "Snow")
        myrow = layout.row()
        myrow.operator('wm.moresnow') 
        myrow.operator('wm.lesssnow') 

def register():
    bpy.utils.register_class(LayoutDemoPanel)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()
