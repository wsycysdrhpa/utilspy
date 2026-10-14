import codecs
import sys


# ng
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_no-dy/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_bt0.7/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_bt0.8/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_bt0.9/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_ts1000_bt0.6/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_ts1000_bt0.6_mod/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_ts1080/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_ts1080_bt0.8/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_428_base_ts1200_bt0.8/text'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_robot_base/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_robot_base_no-dy/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_robot_base_ts1000/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-v1.2.0/ng_robot_base_ts1080/text'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_base/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_base_no-dy/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_428_base_ts1080_bt0.6/text'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_robot_base/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_robot_base_no-dy/text'
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/ng-bpe-3k/ng_robot_base_ts1080_bt0.6/text'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/urdu_3553_base_bt0.6/text'


# urdu
# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/urdu-marketing/ng_robot_base_ts960_bt0.6/text'

# src_file = '/workspace/haipeng/haipeng/work/asr/engine/occ_wenet/runtime/onnxruntime/script/log/urdu-marketing/ng_customer_base_ts960_bt0.6/text'


src_file = sys.argv[1]


utt_sil_count = 0
utt_seg_count = 0
num = 0
with codecs.open(src_file, 'r') as src_fp:
    for line in src_fp:
        line = line.strip()
        key, text = line.split('\t')
        # if text.startswith('<silence>') or text.endswith('<silence>'):
        #     pass
        text = text.lstrip('<silence>|')
        text = text.rstrip('|<silence>')
        text = text.strip('<silence>')
        if '<silence>' in text:
            # print(key, text)
            utt_sil_count += 1
        if '|' in text:
            # print("{}: {}".format(key, text))
            utt_seg_count += 1
        num += 1

# print(utt_sil_count)
print('short_score: {}/{}={}'.format(num-utt_seg_count, num, round((num-utt_seg_count)/num, 4)*100))
