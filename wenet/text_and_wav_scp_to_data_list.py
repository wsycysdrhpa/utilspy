import codecs
import json


in_text_file = '/workspace/haipeng/haipeng/work/data/en/asr/cv/cv_230914/cv-corpus-15.0-2023-09-08/en/test_processed/text_h3k'
in_wav_scp_file = '/workspace/haipeng/haipeng/work/data/en/asr/cv/cv_230914/cv-corpus-15.0-2023-09-08/en/test_processed/wav_16k_h3k.scp'

out_data_list_file = '/workspace/haipeng/haipeng/work/data/en/asr/cv/cv_230914/cv-corpus-15.0-2023-09-08/en/test_processed/data.list'


with codecs.open(in_text_file, 'r') as in_text_fp, \
    codecs.open(in_wav_scp_file, 'r') as in_wav_scp_fp, \
    codecs.open(out_data_list_file, 'w') as out_data_list_fp:
    text_data = in_text_fp.readlines()
    wav_scp_data = in_wav_scp_fp.readlines()
    for t_data, w_data in zip(text_data, wav_scp_data):
        key = t_data.strip().split()[0]
        text = ' '.join(t_data.strip().split()[1:])
        text = text.upper()
        wav = w_data.strip().split()[1]
        json_data = {"key": key,
                    "wav": wav,
                    "txt": text}
        str_data = json.dumps(json_data, ensure_ascii=False)
        out_data_list_fp.write("%s\n" % (str_data))
