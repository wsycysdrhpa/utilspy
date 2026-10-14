from glob import glob
from os.path import join
import codecs
import jsonlines
import os
import codecs
import subprocess
from multiprocessing import Pool

from tqdm import tqdm

import torch


step = 0


# 多进程VAD处理
if step == 0:
    # in_file = '/workspace/haipeng/haipeng/work/data/indonesia/asr/to_label/marketing_20240603-20240603/audio_left.lst.100'
    in_file = '/workspace/haipeng/haipeng/work/data/indonesia/asr/to_label/marketing_20240603-20240603/audio_left.lst'

    out_file = '/workspace/haipeng/haipeng/work/data/indonesia/asr/to_label/marketing_20240603-20240603/audio_left_seged.data.list'
    dst_seg_dir = '/workspace/haipeng/haipeng/work/data/indonesia/asr/to_label/marketing_20240603-20240603/audio_left_seged'

    dur_min_threshold_s = 2.0
    dur_max_threshold_s = 30.0

    if not os.path.exists(dst_seg_dir):
        os.makedirs(dst_seg_dir)

    model_name = '/workspace/haipeng/haipeng/work/asr/silero-vad'
    SAMPLING_RATE = 8000
    USE_ONNX = True # change this to True if you want to test onnx model
    model, utils = torch.hub.load(repo_or_dir=model_name,
                                model='silero_vad',
                                source='local',
                                force_reload=False,
                                onnx=USE_ONNX)

    (get_speech_timestamps,
    save_audio,
    read_audio,
    VADIterator,
    collect_chunks) = utils

    # VAD切分函数
    def process_audio(line):
        out_dict_list = []
        wav_path = line.strip()
        # print(wav_path)
        wav = read_audio(wav_path, sampling_rate=SAMPLING_RATE)
        speech_timestamps = get_speech_timestamps(wav, model, 
                                                threshold=0.5,
                                                sampling_rate=SAMPLING_RATE, 
                                                min_speech_duration_ms=250,
                                                min_silence_duration_ms=500,
                                                window_size_samples=256,
                                                return_seconds=True)

        if speech_timestamps:
            # print(wav_path, speech_timestamps)
            basename = os.path.basename(wav_path)
            for speech_timestamp in speech_timestamps:
                start = round(max(0.0, float(speech_timestamp['start']) - 0.25), 2)
                end = round(min(len(wav)/SAMPLING_RATE, float(speech_timestamp['end']) + 0.25), 2)
                dur = round(end-start, 2)

                if (dur >= dur_min_threshold_s) and (dur <= dur_max_threshold_s):
                    out_wav_file = "{}/{}_{}_{}.wav".format(dst_seg_dir, basename[:-4], start, end)
                    cmd = "sox {} {} trim {} {}".format(wav_path, out_wav_file, start, dur)
                    # print(cmd)
                    _, _  = subprocess.getstatusoutput(cmd)

                    out_dict = {}
                    out_dict.update({'wav': out_wav_file})
                    out_dict.update({'start': round(start, 2)})
                    out_dict.update({'end': round(end, 2)})
                    out_dict.update({'duration': round(dur, 2)})

                    out_dict_list.append(out_dict)

        return out_dict_list


    with codecs.open(in_file, 'r') as in_fp, \
        jsonlines.open(out_file, 'w') as out_fp:
        lines = in_fp.readlines()

        tasks = lines
        with Pool(processes=10) as pool:
            for out_dict_list in tqdm(pool.imap(process_audio, tasks), total=len(tasks), desc='处理进度'):
                for out_dict in out_dict_list:
                    out_fp.write(out_dict)
