# 此脚本作用为构建加性噪音数据
# concat噪音数据构造参考：/workspace/haipeng/haipeng/work/asr/asr_sop/test/data_engineer/slang_concat_noise.py


import os
import codecs
import json
import jsonlines
import sys
import random
import copy

from tqdm import tqdm
from pydub import AudioSegment

def add_noise(speech_audio, noise_audio, output_audio, denoise_db=10):
    # 加载语音文件
    voice = AudioSegment.from_file(speech_audio)

    # 加载噪声文件
    noise = AudioSegment.from_file(noise_audio)

    # 调整噪声的音量（如果需要）
    noise = noise - denoise_db

    # 确保噪声文件至少和语音文件一样长
    if len(noise) < len(voice):
        noise = noise * (len(voice) // len(noise) + 1)

    # 截取与语音文件一样长的噪声
    noise = noise[:len(voice)]

    # 将噪声叠加到语音上
    combined = voice.overlay(noise)

    # 保存结果
    combined.export(output_audio, format="wav")


if __name__ == "__main__":
    # # for haitian label
    # speech_data_json = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/haitian_label.data.list'
    # noise_data_json = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/noise.list.del_airudder_cg.add_occ_id_dup12'

    # out_data_json = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/haitian_label_add_noise.data.list'
    # out_data_dir = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/haitian_label_add_noise'

    # ratio = 0.3


    # for slang
    speech_data_json = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/slang_data.list.dup6'
    noise_data_json = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/noise.list.del_airudder_cg.add_occ_id_dup12'

    out_data_json = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/slang.data.list.dup6.add_noise'
    out_data_dir = '/workspace/yangsen/data/asr/experiment/sop/indonesia/dataset/slang_data/noise_data/v6/slang_data_list_dup6_add_noise'

    ratio = 1.0


    if not os.path.exists(out_data_dir):
        os.makedirs(out_data_dir)

    speech_data_json_list = []
    with jsonlines.open(speech_data_json, 'r') as in_fp:
        for line in in_fp:
            speech_data_json_list.append(line)

    noise_data_json_list = []
    with jsonlines.open(noise_data_json, 'r') as in_fp:
        for line in in_fp:
            noise_data_json_list.append(line)

    utt_num = int(len(speech_data_json_list) * ratio)
    print('utt_num: {}'.format(utt_num))

    with jsonlines.open(out_data_json, 'w') as out_fp: 
        for i in tqdm(range(utt_num)):
            random_speech_num = random.randint(0, len(speech_data_json_list)-1)
            random_noise_num = random.randint(0, len(noise_data_json_list)-1)
            random_denoise_db = 0
            # random_denoise_db = random.randint(0, 5)

            speech_audio_j = speech_data_json_list[random_speech_num]
            noise_audio_j = noise_data_json_list[random_noise_num]

            if noise_audio_j['key'].endswith('.wav'):
                noise_audio_j['key'] = noise_audio_j['key'][:-4]
            if 'noise-free-soun' in noise_audio_j['key']:
                random_denoise_db = random.randint(5, 10)

            print('random_speech_num: {}; random_noise_num: {}; random_denoise_db: {}'.format(random_speech_num, random_noise_num, random_denoise_db))

            output_audio_name = 'speech-{}-add-noise-{}.wav'.format(speech_audio_j['key'], noise_audio_j['key'])

            output_audio = os.path.join(out_data_dir, output_audio_name)
            add_noise(speech_audio_j['wav'], noise_audio_j['wav'], output_audio, denoise_db=random_denoise_db)

            out_dict = copy.deepcopy(speech_audio_j)
            out_dict.update({'key': output_audio_name[:-4]})
            out_dict.update({'wav': output_audio})
            out_dict.update({'speech_path': speech_audio_j['wav']})
            out_dict.update({'noise_path': noise_audio_j['wav']})
            out_dict.update({'denoise_db': random_denoise_db})
            out_fp.write(out_dict)

            # break
