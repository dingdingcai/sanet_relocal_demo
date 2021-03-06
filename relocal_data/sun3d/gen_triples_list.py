import sys
import os
from tqdm import tqdm
from relocal_data.sun3d.random_sel_module import sel_triple_sun3d
from frame_seq_data import FrameSeqData
import torch as T
import pickle
import random

''' Configuration ------------------------------------------------------------------------------------------------------
'''
trans_thres = 0.2

overlap_threshold = (0.5, 0.8)

max_triple_num = 100

num_sample_per_triple = 20

shuffle_list = False

''' Utilities ----------------------------------------------------------------------------------------------------------
'''
def check_file_exist(basedir, frames:FrameSeqData):
    exist_flag = True
    for frame in frames.frames:
        img_name = frame['file_name']
        depth_name = frame['depth_file_name']
        if not os.path.exists(os.path.join(basedir, img_name)):
            exist_flag = False
            break
        if not os.path.exists(os.path.join(basedir, depth_name)):
            exist_flag = False
            break
    return exist_flag


''' Script -------------------------------------------------------------------------------------------------------------
'''
if __name__ == '__main__':

    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/mnt/Exp_2/SUN3D'
    out_bin_file = sys.argv[2] if len(sys.argv) > 2 else '/mnt/Exp_2/SUN3D/relocal_train.bin'

    # Read list
    list_file = os.path.join(base_dir, 'SUN3Dv1_train.txt')
    seq_lists = []
    with open(list_file, 'r') as list_f:
        for seq_name in list_f:
            seq_name = seq_name.strip()
            seq_lists.append(seq_name)

    total_sub_seq_list = []
    for seq_name in tqdm(seq_lists):
        in_frame_path = os.path.join(base_dir, seq_name, 'seq.json')
        if os.path.exists(in_frame_path):
            frames = FrameSeqData(in_frame_path)
            if check_file_exist(base_dir, frames) is False:
                print('None Exist on %s', seq_name)
            else:
                sub_frames_list = sel_triple_sun3d(base_dir=base_dir,
                                                   scene_frames=frames,
                                                   max_triple_num=max_triple_num,
                                                   num_sample_per_triple=num_sample_per_triple,
                                                   trans_thres=trans_thres,
                                                   overlap_thres=overlap_threshold)
                total_sub_seq_list += sub_frames_list


    with open(out_bin_file, 'wb') as out_f:
        if shuffle_list:
            random.shuffle(total_sub_seq_list)
        pickle.dump(total_sub_seq_list, out_f)
        print('Total:', len(total_sub_seq_list))
        print('Done, saved to %s' % out_bin_file)



