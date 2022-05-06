import time
import io
import splitfolders


def split_folders(target_folder, ratio, 
                  group_prefix=None, move=False, output_folder='images', seed=123):
    target_folder = target_folder #'images/nottingham_forest'
    output_folder = output_folder #'images'
    splitfolders.ratio(target_folder, output_folder, 
                    seed=seed, ratio=(ratio), 
                    group_prefix=group_prefix, move=move)


split_folders('images/nottingham_forest', (0.85, 0.10, 0.05))



