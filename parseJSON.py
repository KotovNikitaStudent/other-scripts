import os
import json
import subprocess
import matplotlib.pyplot as plt

# # list of command
# def ListOfCommand(path):
#     list1 = []
#     for folder in os.listdir(path):
#         if (not folder.endswith(".mp4")) and (not folder.endswith(".MP4")):
#             list1.append(folder)
#     j = 1
#     for i in list1:
#         print(f"{j}) bin\OpenPoseDemo.exe --video D:\Точка_Зрения\Проект_по_спорту\Video\exercises\{i}.MP4"
#               f" --net_resolution 320x-1 --write_json D:\Точка_Зрения\Проект_по_спорту\Video\exercises\{i}"
#               f" --part_candidates")
#         j += 1

# get list of files in current directory
def ListOfDirectory(path):
    list_files = []
    for file in os.listdir(path):
        if file.endswith('.MP4') or file.endswith('.mov'):
            list_files.append(file)
    return list_files

# get file name in current directory
def get_name_file(path, list_files):
    file_name = []
    for file in list_files:
        base = os.path.basename(os.path.join(path, file))
        file_name.append(os.path.splitext(base)[0])
    return file_name

def get_list_dir(path):
    list_files = []
    for file in os.listdir(path):
        if file.endswith('.json'):
            list_files.append(file)
    return list_files

# create directory with names of files
def CreateDirectory(path, file_name):
    for file in file_name:
        if not os.path.exists(os.path.join(path, file)):
            os.mkdir(os.path.join(path, file))

# converted file.mov to file.MP4
def ConvertMovToMp4(path, list_files):
    os.system('cd D:\\Точка_Зрения\\Проект_по_спорту\\openpose-1.7.0_gpu')
    for file in list_files:
        if file.endswith('.mov'):
            os.system(f'ffmpeg -i D:\\Точка_Зрения\\Проект_по_спорту\\Video\\exercises\\{file} '
                      f'D:\\Точка_Зрения\\Проект_по_спорту\\Video\\exercises'
                      f'\\{os.path.splitext(os.path.basename(os.path.join(path, file)))[0]}.MP4')

# delete all files with .mov
def DeleteMov(path, list_files):
    for file in list_files:
        if file.endswith('.mov'):
            os.remove(os.path.join(path, file))

# run detection and writing data in .json files
def RunDetectAndWriting(file_name):
    for file in file_name:
        os.system('PowerShell.exe')
        os.system('cd D:\\Точка_Зрения\\Проект_по_спорту\\openpose-1.7.0_gpu')
        os.system(f'bin\\OpenPoseDemo.exe --video D:\\Точка_Зрения\\Проект_по_спорту\\Video\\exercises\\{file}.MP4'
                        f' --net_resolution 320x-1 --write_json D:\\Точка_Зрения\\Проект_по_спорту\\Video\\exercises\\{file}')

# parsing extract data and writing all .json files in one .json file
def ParsingWritingInOneFile(path):
    lines = []
    for folder in os.listdir(path):
        if (not folder.endswith(".mp4")) and (not folder.endswith(".MP4")):
            for file in os.listdir(os.path.join(path, folder)):
                with open(path + '/' + folder + '/' + file) as f:
                    lines.append(json.load(f))
                f.close()
            with open(path + '/' + folder + '/' + 'result.json', 'w') as out_file:
                json.dump(lines, out_file, indent=4)
                lines.clear()

def ParsingJSON(path, fold):
    keypoints = []
    list1 = []
    for folder in os.listdir(path):
        if (not folder.endswith(".mp4")) and (not folder.endswith(".MP4")):
            for file in os.listdir(path + '/' + str(fold)):
                if file.startswith("result"):
                    with open(path + '/' + str(fold) + '/' + file) as f:
                        keypoints.append(json.load(f))
                    f.close()
            for i in keypoints[0]:
                if isinstance(i, dict):
                    list1.append(i["part_candidates"][0])
                else:
                    continue
            return list1
            # with open(path + '/' + fold + '/' + 'result_parse.json', 'w') as out_file:
            #     json.dump(list1, out_file, indent=4)
            #     list1.clear()
            # out_file.close()

if __name__ == "__main__":

    path1 = 'D:/Точка_Зрения/Проект_по_спорту/Video/exercises'
    # path = 'D:/Точка_Зрения/Проект_по_спорту/Video/domical_videos'
    # print(ParsingJSON(path1, "_0032")[0][2]["part_candidates"][0])

    # for folder in os.listdir(path1):
    #     if (not folder.endswith(".mp4")) and (not folder.endswith(".MP4")):
    #         ParsingJSON(path1, folder)

    # intersection of points 4 and 2
    y_coord_4 = []
    y_coord_2 = []
    for i in ParsingJSON(path1, "_0032"):
        if len(i["4"]) != 0 and len(i["2"]) != 0:
            y_coord_4.append(i["4"][1])
            y_coord_2.append(i["2"][1])
        else:
            continue

    x_coord = [i for i in range(len(y_coord_4))]

    plt.scatter(x_coord, y_coord_4)
    plt.scatter(x_coord, y_coord_2)
    plt.legend(["point 4", "point 2"])
    plt.xlabel('frame')
    plt.ylabel(f'y coordinate of point number by {4} and {2}')
    plt.show()