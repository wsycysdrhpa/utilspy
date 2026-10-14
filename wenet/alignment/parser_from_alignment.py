import os
import json
from textgrid import TextGrid, IntervalTier
import soundfile as sf
from tqdm import tqdm


def generator_textgrid(maxtime, lines, output):
    # Download Praat: https://www.fon.hum.uva.nl/praat/
    interval = maxtime / (len(lines) + 1)
    margin = 0.0001

    tg = TextGrid(maxTime=maxtime)
    linetier = IntervalTier(name="line", maxTime=maxtime)

    i = 0
    for l in lines:
        w, s, e = l
        linetier.add(minTime=float(s) + margin, maxTime=min(float(e), maxtime), mark=w)

    tg.append(linetier)
    # print("successfully generator {}".format(output))
    tg.write(output)


def get_timestamp(alignment:list, vocab_map=None, subsample=6):
    timestamp = []
    length = len(alignment)
    start, end = 0, 0
    while start < length:
        if alignment[start] in [0, 364, 1]:
            start += 1
            continue
        left = start - 4
        right = start + 4
        left = max(left, 0)
        right = min(right, length)
        timestamp.append((vocab_map[alignment[start]], start, left, right))
        # print(alignment[start], vocab_map[alignment[start]])
        start += 1
    i = 0
    now_alignment = timestamp[i]
    result = []
    i = 1
    while i < len(timestamp):
        while i < len(timestamp) and now_alignment[-1] >= timestamp[i][2]-5:
            alignment = now_alignment[0] + timestamp[i][0]
            left = now_alignment[-2]
            right = timestamp[i][-1]
            now_alignment = (alignment, now_alignment[1], left, right)
            i += 1
        if i == len(timestamp):
            # result.append(now_alignment)
            break
        result.append(now_alignment)

        now_alignment = timestamp[i]
        i += 1
    result.append(now_alignment)
    result_time = []
    for text, start, left, right in result:
        start_time = left * subsample * 10 /1000
        end_time = right * subsample * 10 /1000
        text = text.replace('▁', ' ')
        result_time.append((text, start_time, end_time))
    return result, result_time


def get_vocab_map(file):
    vocab_map = {}
    with open(file, 'r', encoding='utf8') as fp:
        for line in fp:
            arr = line.strip().split(' ')
            vocab_map[int(arr[1])] = arr[0]
    return vocab_map


def parser_from_alignmet_file(input_file, vocab_file, out_dir):
    vocab_map = get_vocab_map(vocab_file)
    times_map = {}
    with open(input_file, 'r', encoding='utf8') as fp:
        for line in fp:
            arr = line.strip().split()
            key = arr[0]
            out_file = os.path.join(out_dir, key+'.TextGrid')
            out_lab = os.path.join(out_dir, key+'.lab')
            val = " ".join(arr[1:])
            alignment = json.loads(val)
            result, result_time = get_timestamp(alignment, vocab_map, subsample)
            times_map[key] = result_time
            generator_textgrid(len(alignment) * 0.01 * subsample, result_time, out_file)
            fp_o = open(out_lab, 'w', encoding='utf8')
            for w, s, e in result_time:
                fp_o.write("{}\t{}\t{}\n".format(s, e, w))
            fp_o.close()
    return times_map


def generate_align_auido_and_datalist(data_list, out_data_list, out_voice_dir, times_map):
    fp_i = open(data_list, 'r', encoding='utf8')
    fp_o = open(out_data_list, 'w', encoding='utf8')
    for line in tqdm(fp_i):
        data = json.loads(line)
        key = data['key']
        wav_file = data['wav']
        if key not in times_map: continue
        times_list = times_map[key]
        audio, fq = sf.read(wav_file)
        for w, s, e in times_list:
            start, end = int(s*fq), int(e*fq)
            slice_audio = audio[start:end+1]
            new_key = key.replace('.wav', '').replace('.mp3', '')
            new_key = new_key + '_' + str(s) + '_' + str(e) + '.mp3'
            out_file = os.path.join(out_voice_dir, new_key)
            sf.write(out_file, slice_audio, fq)
            new_data = {'key': new_key, 'wav': out_file, 'txt': w}
            fp_o.write(json.dumps(new_data, ensure_ascii=False) + '\n')
    fp_i.close()
    fp_o.close()


if __name__ == '__main__':
    vocab_file = '/home/yangsen/work/asr/wenet-v2.2.0/examples/opay_urdu/s0_run/data/lang_char_cv_cuishou_20230425_3k/unigram3000_units.txt'
    vocab_map = get_vocab_map(vocab_file)
    subsample = 6
    date = '20230510'
    align_file = "/home/yangsen/data/raw/dx/20230501_20230520/wiz_text_alignment/%s/result/align.txt" % date
    data_list = "/home/yangsen/data/raw/dx/20230501_20230520/wiz_text_alignment/%s/data.list" % date
    praat_dir = "/home/yangsen/data/raw/dx/20230501_20230520/wiz_text_alignment/%s/praat" % date
    out_data_list = "/home/yangsen/data/raw/dx/20230501_20230520/wiz_text_alignment/%s/parser_result/data.list" % date
    out_voice_dir = "/home/yangsen/data/raw/dx/20230501_20230520/wiz_text_alignment/%s/mp3_align" % date
    os.makedirs(praat_dir, exist_ok=True)
    os.makedirs(out_voice_dir, exist_ok=True)
    os.makedirs(os.path.dirname(out_data_list), exist_ok=True)

    times_map = parser_from_alignmet_file(align_file, vocab_file, praat_dir)
    generate_align_auido_and_datalist(data_list, out_data_list, out_voice_dir, times_map)


