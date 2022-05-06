# Mini nvGesture 


```bash
# color only 
python utils/nv_prepare.py --subset_type=training --file_name=trainlistall.txt --class_types=all --sensors=color

# both color and depth 
python utils/nv_prepare.py --subset_type=training --file_name=trainlistall.txt --class_types=all --sensors=color --sensors=depth
```