import codecs
import re
import sys

'''
format:
utt_id1&&utt_id2&&utt_id3 text1 text2 text3
'''

# ng
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_no-dy/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_no-dy/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_bt0.7/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_bt0.8/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_bt0.9/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1080_bt0.6/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1080_bt0.8/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1200_bt0.6/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1200_bt0.8/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_1.5s_base/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_1s_base/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_1s_base_no-dy/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_1s_base_ts1080_bt0.6/text_long'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1000_bt0.6/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1000_bt0.6_mod/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_joint_sil_2s_base_ts1000_bt0.6_no-dy/text_long'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_2s_base/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_2s_base_no-dy/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_2s_base_ts1080_bt0.6/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_1.5s_base/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_1s_base/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_1s_base_no-dy/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_joint_sil_1s_base_ts1080_bt0.6/text_long'


# urdu
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/urdu-marketing/ng_customer_joint_sil_1s_base_ts960_bt0.6/text_long'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/urdu-marketing/ng_customer_joint_sil_2s_base_ts960_bt0.6/text_long'


src_file = sys.argv[1]


# re_sil = re.compile('<silence>')
# re_muti_sil = re.compile('(<silence> )+')

# total_long = 0
# correct_long = 0
# total_short = 0
# correct_short = 0
# with codecs.open(src_file, 'r') as src_fp:
#     for line in src_fp:
#         line = line.strip()
#         key_long, text_long = line.split('\t')
#         keys = key_long.split('&&')
#         step = len(keys)
#         total_long += 1
#         total_short += step

#         text_long = re_muti_sil.sub('<silence> ', text_long)

#         texts = re_sil.split(text_long)
#         texts = [text.strip() for text in texts]

#         if len(keys) == len(texts):
#             correct_long += 1
#             correct_short += len(keys)
#         elif len(keys) > len(texts):
#             # print(keys)
#             diff = len(keys) - (len(keys) - len(texts)) - 1
#             # diff = len(keys) - (len(keys) - len(texts))
#             score = diff if diff > 0 else 0
#             correct_short += score
#         else:
#             diff = len(keys) - (len(texts) - len(keys))
#             score = diff if diff > 0 else 0
#             correct_short += score

#         # break

# print('{}/{}={}'.format(correct_long, total_long, correct_long/total_long))
# print('{}/{}={}'.format(correct_short, total_short, correct_short/total_short))


# print('-' * 50)
# long text with '|', for splitting to short text
src_file = src_file[:-5]

total_long = 0
correct_long = 0
total_short = 0
correct_short = 0
small = 0
big = 0
with codecs.open(src_file, 'r') as src_fp:
    for line in src_fp:
        line = line.strip()
        key_long, text_long = line.split('\t')
        keys = key_long.split('&&')
        step = len(keys)
        total_long += 1
        total_short += step

        # print(text_long)

        texts = text_long.split('|')
        # print(texts)
        texts = [text.strip() for text in texts if text.strip() != '<silence>']
        # print(texts)

        if len(keys) == len(texts):
            correct_long += 1
            correct_short += step
        elif len(keys) > len(texts):
            # print(keys)
            # print(texts)
            # print(text_long)
            small += 1
            diff = len(keys) - (len(keys) - len(texts)) - 1
            # diff = len(keys) - (len(keys) - len(texts))
            score = diff if diff > 0 else 0
            correct_short += score
        else:
            # print(keys)
            # print(texts)
            # print(text_long)
            big += 1
            diff = len(keys) - (len(texts) - len(keys))
            score = diff if diff > 0 else 0
            correct_long += 1
            correct_short += score

        # break

print('long_score: {}/{}={}'.format(correct_long, total_long, round(correct_long/total_long, 4)*100))
# print('{}/{}={}'.format(correct_short, total_short, correct_short/total_short))
# print(small, big)
