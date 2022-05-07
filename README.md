# Mini nvGesture 

## 1. Prerequisite
* installing FFmpeg 
```bash 
sudo apt update 
sudo apt install ffmpeg 

# check 
ffmpeg -version 
```
* installing python packages 
```bash 
pip install -r requirements.txt
```



## 2. Usage 
(step1) Generate annotation file in ```csv```. 
```bash
# === Training === # 
# class types (all) - set background as 26 
python utils/nv_prepare.py --subset_type=training --file_name=trainlistall.txt --class_types=all --sensors=color

# class types (all but None)
python utils/nv_prepare.py --subset_type=training --file_name=trainlistall_but_None.txt --class_types=all_but_None --sensors=color 

# class types (binary) 
python utils/nv_prepare.py --subset_type=training --file_name=trainlistbinary.txt --class_types=binary --sensors=color 
```
```bash
# === Validation === # 
# class types (all) - set background as 26 
python utils/nv_prepare.py --subset_type=validation --file_name=vallistall.txt --class_types=all --sensors=color

# class types (all but None)
python utils/nv_prepare.py --subset_type=validation --file_name=vallistall_but_None.txt --class_types=all_but_None --sensors=color 

# class types (binary)
python utils/nv_prepare.py --subset_type=validation --file_name=vallistbinary.txt --class_types=binary --sensors=color 

```


<br/>

(step2) Generate annotation file in ```json```  format similar to ActivityNet.
``` bash
python utils/nv_json.py 
```

<br>

(step3) Extract frames of video data. 
``` bash
# color only 
python utils/nv_extract_frames.py --sensors=color

# both color and depth 
python utils/nv_extract_frames.py --sensors=color --sensors=depth
```