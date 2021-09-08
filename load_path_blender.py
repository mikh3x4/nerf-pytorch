

import bpy
import json
from mathutils import Matrix

import os.path

object_to_copy = bpy.data.objects["tim_drone"]

def load_MPC(experiment_name):
    pass

def load_training(experiment_name):
    collection = bpy.data.collections.new(experiment_name +"_train")
    bpy.context.scene.collection.children.link(collection)

    save = 0
    while True:
        filepath = bpy.path.abspath('//../experiments/' + experiment_name + '/train_poses/') +str(save)+".json"
        if not os.path.isfile(filepath):
            break

        bpy.context.scene.frame_set(save)

        print("LOADING SAVE #"+str(save))
        with open(filepath) as f:
            for i, line in enumerate(f):

                name = "path_"+str(i)
                if save == 0:
                    new_object = object_to_copy.copy()
                    collection.objects.link(new_object)

                    new_object.name = name 
                else:
                    new_object = bpy.data.objects[name]

                pose = json.loads(line)
                new_object.matrix_world = Matrix(pose)
                # print(i, pose)

                new_object.keyframe_insert(data_path="location")
                if new_object.rotation_mode == "QUATERNION":
                    new_object.keyframe_insert(data_path = 'rotation_quaternion')
                else:
                    new_object.keyframe_insert(data_path = 'rotation_euler')
                
        bpy.context.view_layer.update() 
        save += 1

def get_endpoints():
    s_loc = [round(x,2) for x in bpy.data.objects['Start'].location]
    bpy.data.objects['Start'].location = Vector(s_loc)
    e_loc = [round(x,2) for x in bpy.data.objects['End'].location]
    bpy.data.objects['End'].location = Vector(e_loc)
    s = ""
    s += 'start_pos = torch.tensor(' + str( s_loc ) +")"
    s += "\n"
    s += 'end_pos = torch.tensor(' + str( e_loc ) +")"
    s += "\n"
    print(s)



experiment_name = "playground_slide"

load_training(experiment_name)
