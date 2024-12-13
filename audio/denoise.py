#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Test(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks


    ans = pipeline(
        Tasks.acoustic_noise_suppression,
        model='damo/speech_frcrn_ans_cirm_16k')
    result = ans(
        'https://modelscope.oss-cn-beijing.aliyuncs.com/test/audios/speech_with_noise1.wav',
        output_path='output.wav')
