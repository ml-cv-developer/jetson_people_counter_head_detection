import sys
sys.path.append('../')
import os
import logging
import datetime
from utils_machine import videos_output
from utils_ken.log.getlog import get_logger

logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-12s : %(name)-5s : [%(levelname)-5s] : %(message)5s')


clear_video = get_logger('clear_video_', './logs/clear_video_.log')


# ROOT_PATH = '/home/ken/workspace/nano_package'
# ------------------------------------------------------------------------------------
# pose video recored to server
# ------------------------------------------------------------------------------------

def get_size(start_path):
    total_size = 0
    list_file  = []
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            # print(filenames)
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                list_file.append(fp)
                total_size += os.path.getsize(fp)
    
    size_gibike = int(total_size/(1024*1024*1024))
    list_file.sort()
    return size_gibike, list_file



def main_processing(video_folder, max_size=10) :

    size_gibike, list_file =  get_size(video_folder)
    clear_video.info('foldel : {} total size : {} Gb'.format(video_folder, size_gibike))

    for file_1 in list_file :
        clear_video.info(file_1)
	
    # try :
    if len(list_file) > 0 :
        last_file = list_file[0]
        if size_gibike >= max_size :
            clear_video.info('deleted file'.format(last_file))
            os.remove(last_file)

    # except :
    #     clear_video.info('folder empty'.format(video_folder))

if __name__ == '__main__' :
    # main_processing(video_folder = './a')
    main_processing(video_folder = videos_output)
