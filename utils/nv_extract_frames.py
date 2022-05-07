""" code reference to
    - 'https://github.com/ahmetgunduz/Real-time-GesRec/blob/master/utils/nv_prepare.py'
    - 'https://drive.google.com/drive/folders/0ByhYoRYACz9cMUk0QkRRMHM3enc?resourcekey=0-cJe9M3PZy2qCbfGmgpFrHQ' 
"""
import os.path as osp 
import glob 
from pathlib import Path 
from subprocess import call

import click


@click.command()
@click.option('--project_root', required=True, 
                default=osp.join('/home/ubuntu/phD_workspace/video-modeling/nvGesture-tutorial'),
                help="Root path for dataset")
@click.option('--sensors', required=True,
                type=click.STRING, multiple=True,
                default=["color", "depth", "duo_left", "duo_right", "duo_disparity"],
                help="video data modality")                          
def main(project_root:str,
        sensors:list
        ):
    click.echo(project_root)
    click.echo(sensors)

    dataset_root = osp.join(project_root, 'dataset','mini_nvGesture')


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


if __name__ == "__main__":
    main()