""" code inspired by 
    - https://github.com/ahmetgunduz/Real-time-GesRec/blob/master/utils/nv_json.py
"""
import sys
import os.path as osp 
import json

import numpy as np 
import click
import pandas as pd
from tqdm import tqdm



@click.command()
@click.option('--project_root', required=True, 
                default=osp.join('/home/ubuntu/phD_workspace/video-modeling/nvGesture-tutorial'),
                help="Root path for dataset")                         
@click.option('--anno_dir', required=True, 
                default='annotation_nvGesture',
                help="annotation_nvGesture")                
def main(project_root:str,
        anno_dir:str
        ):
    click.echo(project_root)
    click.echo(anno_dir)

    anno_dir = osp.join(project_root, anno_dir)
    
    for class_type in ['all', 'all_but_None', 'binary']:
        if class_type == 'all': 
            class_ind_file = 'classIndAll.txt'

        elif class_type == 'all_but_None':
            class_ind_file = 'classIndAllbutNone.txt'

        elif class_type == 'binary':
            class_ind_file = 'classIndBinary.txt'            
    

        label_csv_path = osp.join(anno_dir, class_ind_file)
        train_csv_path = osp.join(anno_dir, f"trainlist{class_type}.txt")
        val_csv_path  = osp.join(anno_dir, f"vallist{class_type}.txt")

        dst_json_path = osp.join(anno_dir, f"nv{class_type}.json") # path to save 


        # convert to .json format 
        # ----------------------
        convert_nv_csv_to_activitynet_json(label_csv_path, train_csv_path, val_csv_path, dst_json_path)

        print(f"Successfully wrote to json : {dst_json_path}")




# ================
# ----------------
def convert_nv_csv_to_activitynet_json(label_csv_path, train_csv_path, val_csv_path, dst_json_path):
    labels = load_labels(label_csv_path)
    train_database = convert_csv_to_dict(train_csv_path, 'training', labels)
    val_database = convert_csv_to_dict(val_csv_path, 'validation', labels)

    dst_data = {}
    dst_data['labels'] = labels
    dst_data['database'] = {}
    dst_data['database'].update(train_database)
    dst_data['database'].update(val_database)

    # save them in .json 
    with open(dst_json_path, 'w') as f: 
        json.dump(dst_data, f)


# ================
# ----------------
def load_labels(label_csv_path) -> list:
    data = pd.read_csv(label_csv_path,  delimiter=' ', header=None)
    labels = []

    for i in range(data.shape[0]):
        labels.append(str(data.iloc[i, 1])) # class index 

    return labels

# =================
# -----------------
def convert_csv_to_dict(csv_path, subset, labels):
    """ return 
    {'./Video_data/class_01/subject3_r0/sk_color_all': {'subset': 'training', 'annotations': {'label': '26', 'start_frame': '1', 'end_frame': '145'}},
    './Video_data/class_01/subject3_r1/sk_color_all': {'subset': 'training', 'annotations': {'label': '26', 'start_frame': '1', 'end_frame': '159'}},
    ...
    }
    """
    data = pd.read_csv(csv_path, delimiter=' ', header=None)

    keys = [] 
    key_labels = [] 
    key_start_frame = [] 
    key_end_frame = [] 

    for i in range(data.shape[0]): 
        row = data.iloc[i, :] 

        class_name = labels[row[1]-1] # class index 

        basename = str(row[0]) # dir_path for frames 
        start_frame = str(row[2]) # num_frame where starting action 
        end_frame = str(row[3]) # num_frame where ending action 

        # 'frame_path', 'label_idx', 'start_frame', 'end_frame' 
        # ----------------------------------------------------
        keys.append(basename)
        key_labels.append(class_name)
        key_start_frame.append(start_frame)
        key_end_frame.append(end_frame)

    database = {} 
    for idx, frame_dir in enumerate(keys):
        key = frame_dir

        if key in database: # need this because I have the same folder 3  times
            key = key + '^' + str(idx) 
        
        database[key] = {}
        database[key]['subset'] = subset
        label = key_labels[idx]
        start_frame = key_start_frame[idx]
        end_frame = key_end_frame[idx]

        database[key]['annotations'] = {'label': label, 
                                        'start_frame':start_frame, 
                                        'end_frame':end_frame}

    return database


if __name__ == "__main__":
    main() 