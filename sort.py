"""
map the class ID to the image ID and copy images to corresponding files automatically
"""
import pandas as pd
import shutil
import os
# read the csv file using pandas with header
df = pd.read_csv('/Users/jiahuiwu/Desktop/DL_project/Pictures.csv', names=['UID', 'ID1', 'Cls1', 'ID2', 'Cls2', 'ID3', 'Cls3'])
# get the frequency of column ID1 (image )
freq1 = df.groupby('ID1').size().sort_values(ascending=False)
# get the top 10 classes with more frequency
cls_number = 10
file_num_per_class = 6000
cls_name = freq1.head(cls_number).keys()
# turn the Index dtype into a simple list
cls = []
for i in range(10):
    cls.append(cls_name[i])
# make folders according to the class
root_path = '/Users/jiahuiwu/Desktop/DL_project/sample_dataset'
for folder in cls_name:
    directory = os.path.join(root_path, str(folder))
    if not os.path.exists(directory):
        os.mkdir(directory)

# get the source directory
arr = []
for i in range(1, 10):
    arr.append(os.listdir('/Users/jiahuiwu/Desktop/DL_project/picture{}'.format(i)))
root_path1 = '/Users/jiahuiwu/Desktop/DL_project'

for i in range(1, 10):
    source_path = os.path.join(root_path1, 'picture{}'.format(i))
    for file in arr[i - 1]:
        name, extension = os.path.splitext(file)
        # locate the ID1 of the current image
        curr_class = df.loc[df['UID'] == int(name)]
        curr_class = curr_class.iloc[0]['ID1']
        # the loop will break if there's no classes to be added
        if len(cls) == 0:
            break
        if curr_class in cls:
            source = os.path.join(source_path, str(file))
            destination = os.path.join(root_path, str(curr_class))
            file_count = len(os.listdir(destination))
            # move the file from source to destination
            if file_count < file_num_per_class:
                shutil.copy(source, destination)
            # if each class has enough files, stop copy, remove the class
            else:
                cls.remove(curr_class)
