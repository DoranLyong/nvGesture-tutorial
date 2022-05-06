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

#        elif class_type == 'all_but_None':
#            class_ind_file = 'classIndAllbutNone.txt'
#
#        elif class_type == 'binary':
#            class_ind_file = 'classIndBinary.txt'            
    

        label_csv_path = osp.join(anno_dir, class_ind_file)
        train_csv_path = osp.join(anno_dir, f"trainlist{class_type}.txt")
#        val_csv_path  = osp.join(anno_dir, f"vallist{class_type}.txt")
        val_csv_path:str = None

        dst_json_path = osp.join(anno_dir, f"nv{class_type}.json")


        # convert to .json format 
        # ----------------------
        convert_nv_csv_to_activitynet_json(label_csv_path, train_csv_path, val_csv_path, dst_json_path)




# ================
# ----------------
def convert_nv_csv_to_activitynet_json(label_csv_path, train_csv_path, val_csv_path, 
                                        dst_json_path):
    label = load_labels(label_csv_path)


# ================
# ----------------
def load_labels(label_csv_path):
    data = pd.read_csv(label_csv_path,  delimiter=' ', header=None)
    labels = []











if __name__ == "__main__":
    main() 