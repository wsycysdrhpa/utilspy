import os
import codecs
import sys


# ng
# src_wav_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt/wav.scp'
# src_txt_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt/text'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_3s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt_joint_sil_3s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_2.5s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt_joint_sil_2.5s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_2s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt_joint_sil_2s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_1.5s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt_joint_sil_1.5s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_1s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt_joint_sil_1s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_0.5s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_rm_sil_utt_joint_sil_0.5s'


# src_wav_file = '/workspace/haipeng/haipeng/work/asr/wenet/examples/gigaspeech/s0_run/data/test_pidgin_428/wav.scp'
# src_txt_file = '/workspace/haipeng/haipeng/work/asr/wenet/examples/gigaspeech/s0_run/data/test_pidgin_428/text'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_2s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_joint_sil_2s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_1.5s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_joint_sil_1.5s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/sil_wav/sil_1s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/ng/test_pidgin_428_joint_sil_1s'


# urdu
# marketing
# src_wav_file = '/workspace/haipeng/haipeng/work/asr/wenet-v2.2.0/examples/opay_urdu/s0_run/data/test_dianxiao_customer_1006/wav.scp'
# src_txt_file = '/workspace/haipeng/haipeng/work/asr/wenet-v2.2.0/examples/opay_urdu/s0_run/data/test_dianxiao_customer_1006/text'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/urdu/marketing/sil_wav/sil_1s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/urdu/marketing/test_customer_joint_sil_1s'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/urdu/marketing/sil_wav/sil_2s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/urdu/marketing/test_customer_joint_sil_2s'


# id
# collection
src_wav_file = '/workspace/haipeng/haipeng/work/asr/wenet/examples/opay_id/s0_run/data/test_collection_customer_3888/wav.scp'
src_txt_file = '/workspace/haipeng/haipeng/work/asr/wenet/examples/opay_id/s0_run/data/test_collection_customer_3888/text'

# sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/id/collection/sil_wav/sil_1s.wav'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/id/collection/test_customer_joint_sil_1s'

sil_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/id/collection/sil_wav/sil_2s.wav'
dst_dir = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/id/collection/test_customer_joint_sil_2s'


wav_scp = os.path.join(dst_dir, 'wav.scp')
txt_long = os.path.join(dst_dir, 'text_long')

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# step = 5
step = 2
joint_num = 0

key_list = []
wav_list = []
txt_list = []

with codecs.open(src_wav_file, 'r') as src_fp:
    lines = src_fp.readlines()
    for line in lines:
        line = line.strip()
        key, wav = line.split()
        key_list.append(key)
        wav_list.append(wav)

key_lists = [key_list[i:i+step] for i in range(0,len(key_list), step)]
# print(key_lists)

wav_lists = [wav_list[i:i+step] for i in range(0,len(wav_list), step)]
# print(wav_lists)

group_num = 0
with codecs.open(wav_scp, 'w') as wav_scp_fp:
    for key_list, wav_list  in zip(key_lists, wav_lists):
        key = '&&'.join(key_list)
        # print(key)
        cmd = 'sox'
        for i in range(len(wav_list)):
            if i == (len(wav_list)-1):
                cmd = cmd + ' ' + wav_list[i]
            else:
                cmd = cmd + ' ' + wav_list[i] + ' ' + sil_file
        dst_audio_dir = os.path.join(dst_dir, 'audio')
        if not os.path.exists(dst_audio_dir):
            os.makedirs(dst_audio_dir)
        audio_name = 'merged_' + str(group_num) + '.wav'
        audio_path = os.path.join(dst_audio_dir, audio_name)
        cmd = cmd + ' ' + audio_path
        # print(cmd)
        if not os.path.exists(audio_path):
            os.system(cmd)
        wav_scp_fp.write(key + ' ' + audio_path + '\n')
        group_num += 1

        # break

# 输出text text_long
with codecs.open(src_txt_file, 'r') as src_fp:
    lines = src_fp.readlines()
    for line in lines:
        line = line.strip()
        # key= line.split()[0]
        txt = ' '.join(line.split()[1:])
        # key_list.append(key)
        txt_list.append(txt)

txt_lists = [txt_list[i:i+step] for i in range(0,len(txt_list), step)]
# print(txt_lists)

with codecs.open(txt_long, 'w') as txt_long_fp:
    for key_list, txt_list  in zip(key_lists, txt_lists):
        key = '&&'.join(key_list)
        text_long = ' '.join(txt_list)
        txt_long_fp.write(key + ' ' + text_long + '\n')
