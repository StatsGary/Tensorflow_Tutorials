import time
import io
import splitfolders
import typing


def split_folders(target_folder, ratio, 
                  group_prefix=None, move=False, output_folder='images', seed=123):

    train_ratio, val_ratio, test_ratio = ratio[0], ratio[1], ratio[2]
    print(f'[SPLIT INITIALISING] Initialising folder split on folder: {target_folder} with train ratio: {train_ratio} validation ratio: {val_ratio} and testing ratio: {test_ratio}.')
    target_folder = target_folder #'images/nottingham_forest'
    output_folder = output_folder #'images'
    splitfolders.ratio(target_folder, output_folder, 
                    seed=seed, ratio=(ratio), 
                    group_prefix=group_prefix, move=move)
    print(f'[SPLIT COMPLETE] Split of images complete and can be found in folder: {output_folder}')



if __name__ =='__main__':
    split_folders(target_folder='images/nottingham_forest',
                  ratio=(0.85, 0.10, 0.05))



