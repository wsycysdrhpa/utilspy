import codecs
import sys
import jsonlines


def ali_tmp_file_to_list(src_file, out_file):
    with codecs.open(src_file) as fin_fp, \
        jsonlines.open(out_file, 'w') as out_fp:
        for line in fin_fp:
            res = dict()
            line = line.strip()
            if line:
                infos = line.split('\t')
                for info in infos:
                    key, value = info.split(':')
                    if key == 'utt':
                        key = 'key'
                    if key == 'feat':
                        key = 'wav'
                    if key == 'text':
                        key = 'txt'
                    res[key] = value
                out_fp.write(res)


if __name__ == "__main__":
    pass
    src_file = "/home/haipeng/work/asr/wenet-v2.2.0/examples/opay_urdu/s0_run/raw_wav/test_10/format.data.tmp"
    out_file = '/home/haipeng/work/asr/wenet-v2.2.0/examples/opay_urdu/s0_run/raw_wav/test_10/format.data'
    ali_tmp_file_to_list(src_file, out_file)
