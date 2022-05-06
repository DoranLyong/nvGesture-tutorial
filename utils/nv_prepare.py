""" code reference to
    - 'https://github.com/ahmetgunduz/Real-time-GesRec/blob/master/utils/nv_prepare.py'
    - 'https://drive.google.com/drive/folders/0ByhYoRYACz9cMUk0QkRRMHM3enc?resourcekey=0-cJe9M3PZy2qCbfGmgpFrHQ' 
"""
import os.path as osp 
import glob 
from pathlib import Path 
from subprocess import call

import numpy as np 
import click
from tqdm import tqdm


@click.command()
@click.option('--project_root', required=True, 
                default=osp.join('/home/ubuntu/phD_workspace/video-modeling/nvGesture-tutorial'),
                help="Root path for dataset")
@click.option('--subset_type', required=True,
                type=click.Choice(['training', 'validation']),
                help="set the subset type")
@click.option('--file_name', required=True, 
                help="annotation file name")
@click.option('--class_types', required=True, 
                help="action class types") 
@click.option('--sensors', required=True,
                type=click.STRING, multiple=True,
                default=["color", "depth", "duo_left", "duo_right", "duo_disparity"],
                help="video data modality")                          
def main(project_root:str,
        subset_type:str,
        file_name:str,
        class_types:str,
        sensors:list
        ):
    click.echo(project_root)
    click.echo(subset_type)
    click.echo(file_name)
    click.echo(class_types)
    click.echo(sensors)

    dataset_root = osp.join(project_root, 'dataset','mini_nvGesture')


    if subset_type == "training": 
        anno_list =  "nvgesture_train_correct_cvpr2016_v2_mini.lst"
    elif subset_type == "validation": 
        anno_list = "nvgesture_test_correct_cvpr2016_v2.lst"

    file_lists = {}
    subset_list = [] 

    # read line-by-line from "nvgesture_train_correct_cvpr2016_v2_mini.lst"
    # ----------------------------
    subset_list = load_split_nvgesture(dataset_root, anno_list, subset_list) 

    # 
    # ----------------------
    print(f"Processing Training List")
    new_lines = []
    for idx, sample in tqdm(enumerate(subset_list), desc="create_lists", total=len(subset_list)): 
        temp_list = create_list(sample, sensor=sensors[0], class_types = class_types) 
        new_lines.extend(temp_list)

    # Writing to the file 
    # -----------------------
    print(f"writing to the file ...")
    project_path = f'/home/ubuntu/phD_workspace/video-modeling/nvGesture-tutorial'
    Path(osp.join(project_path,'annotation_nvGesture')).mkdir(parents=True, exist_ok=True)

    file_path = osp.join(project_path,'annotation_nvGesture', file_name)
    with open(file_path, 'w') as f: 
        for line in new_lines: 
            f.write(line)
            f.write('\n') 
    print(f"Succesfully wrote file to: {file_path}")


    # Extract frames 
    # -----------------
    extract_frames(dataset_root, sensors=sensors)
    



# =================
# -----------------
def extract_frames(dataset_root, sensors=["color", "depth"]):
    """ Extract frames of .avi files. 

    Parameters 
    -----------
    modalities: list of str ; ["color", "depth", "duo_left", "duo_right", "duo_disparity"]
    """
    for vt in sensors: 
        files = glob.glob(osp.join(dataset_root, "Video_data", '*', '*', f"sk_{vt}.avi")) # read all video file paths

        for file in files: 
            print(f"Extracting frames for [{file}]")
            saving_path = f"{file.split('.')[0]}_all" # path for saving frames 
            Path(saving_path).mkdir(parents=True, exist_ok=True)

            call(["ffmpeg", "-i",  file, osp.join(saving_path, "%05d.png"), "-hide_banner"]) 


# =================
# -----------------
def create_list(sample_config:dict, sensor:str, class_types:str="all") -> list:
    dir_path = f"{sample_config[sensor]}_all" # path where to save image frames 
    n_images = len(glob.glob(osp.join(dir_path, '*.png')))

    label = sample_config['label'] + 1  # we made label starting from 0 in 'load_split_nvgesture()' 
                                        # , but it originally starts from 1.

    start_frame = sample_config[f"{sensor}_start"] # frame number where action starts
    end_frame = sample_config[f"{sensor}_end"]

    frame_indices = np.array([[start_frame, end_frame ]])
    len_lines = frame_indices.shape[0]
    
    start = 1 # number of starting frame 
    anno_lines = []
    for i in range(len_lines): 
        line = frame_indices[i, :] # (start_frame, end_frame )

        if class_types == "all": 
            if (line[0] - start) >= 8: # Some action starts right away so I do not add 'None' label. 
                anno_lines.append(f"{dir_path} {26} {start} {line[0]-1}") # set label as 26. 
            anno_lines.append(f"{dir_path} {label} {line[0]} {line[1]}") # 'Frames_path' 'Action_label' 'start_frame' 'end_frame' 

        elif class_types == "all_but_None": 
            anno_lines.append(f"{dir_path} {label} {line[0]} {line[1]}")

        elif class_types == "binary": 
            if (line[0] - start) >= 8 :  # Some action starts right away so I do not add 'None' label.
                anno_lines.append(f"{dir_path} {1} {start} {line[0]-1}") # set label as 1. 
            anno_lines.append(f"{dir_path} {2} {line[0]} {line[1]}")
        
        start = line[1] + 1 # end_frame + 1 
    
    if (n_images - start > 4): 
        if class_types == "all":
            anno_lines.append(f"{dir_path} {26} {start} {n_images}")
        elif class_types == "binary": 
            anno_lines.append(f"{dir_path} {1} {start} {n_images}")

    return anno_lines
    
    


# =================
# -----------------
def load_split_nvgesture(root:str,
                        file_with_split = 'nvgesture_train_correct.lst',
                        subset_list=[]) -> list:

    """ return 'subset_list' filled with: 
        [{'dataset': 'nvgesture', 'depth': './Video_data/class_01/subject3_r0/sk_depth', 'depth_start': 146, 'depth_end': 226, 'color': './Video_data/class_01/subject3_r0/sk_color', 'color_start': 146, 'color_end': 226, 'duo_left': './Video_data/class_01/subject3_r0/duo_left', 'duo_left_start': 170, 'duo_left_end': 263, 'label': 0, 'duo_right': './Video_data/class_01/subject3_r0/duo_right', 'duo_right_start': 170, 'duo_right_end': 263, ...},
        {'dataset': 'nvgesture', 'depth': './Video_data/class_01/subject3_r1/sk_depth', 'depth_start': 160, 'depth_end': 240, 'color': './Video_data/class_01/subject3_r1/sk_color', 'color_start': 160, 'color_end': 240, 'duo_left': './Video_data/class_01/subject3_r1/duo_left', 'duo_left_start': 188, 'duo_left_end': 281, 'label': 0, 'duo_right': './Video_data/class_01/subject3_r1/duo_right', 'duo_right_start': 188, 'duo_right_end': 281, ...},
        ...
        ]
    """

    file_with_split = osp.join(root, file_with_split)

    with open(file_with_split, 'rb') as f: 
        file_name  = file_with_split[file_with_split.rfind('/')+1 :] # get file name as 'nvgesture_train_correct_cvpr2016_v2.lst' or else.
        dict_name  = file_name[:file_name.find('_')] # get name as 'nvgesture'


        for line in f: # read line by line 
            params = line.decode().split(' ') 
            params_dict = {} 

            params_dict['dataset'] = dict_name

            path = params[0].split(':')[1] # (ex) path:./Video_data/class_01/subject4_r0 -> ./Video_data/class_01/subject4_r0
            for param in params[1:]:
                parsed = param.split(':')
                key = parsed[0]   # depth, color, duo_left, label 

                if key == "label": 
                    # make label start from 0 
                    label = int(parsed[1]) - 1 
                    params_dict['label'] = label

                elif key in ('depth','color','duo_left'):
                    #othrwise only sensors format: <sensor name>:<folder>:<start frame>:<end frame>
                    sensor_name = key
                    #first store path
                    params_dict[key] = osp.join(path, parsed[1]) # video path 
                    #store start and frame
                    params_dict[key+'_start'] = int(parsed[2])
                    params_dict[key+'_end'] = int(parsed[3])

            params_dict['duo_right'] = params_dict['duo_left'].replace('duo_left', 'duo_right') # IR cam path 
            params_dict['duo_right_start'] = params_dict['duo_left_start']
            params_dict['duo_right_end'] = params_dict['duo_left_end']  

            params_dict['duo_disparity'] = params_dict['duo_left'].replace('duo_left', 'duo_disparity')
            params_dict['duo_disparity_start'] = params_dict['duo_left_start']
            params_dict['duo_disparity_end'] = params_dict['duo_left_end'] 

            subset_list.append(params_dict)

    return  subset_list



if __name__ == "__main__":
    main()