#!/bin/bash

# Copyright 2019 Mobvoi Inc. All Rights Reserved.
. ./path.sh || exit 1;

stage=0 # start from 0 if you need to start from data preparation
stop_stage=0

nj=16
feat_dir=raw_wav
dict=data/lang_char_cv_cuishou_20230425_3k_qb/unigram3000_units.txt
bpe_model=data/lang_char_cv_cuishou_20230425_3k_qb/unigram3000.model

dir=exp/pak_8k_wiz_annot_20230217_8k_spec_aug_+cv_pak_wiz_so_20230425_dict_3k_speed_pertub_musan_sythese_slang_semi-150h_2
checkpoint=$dir/final.pt
config=$dir/train.yaml
# set=test_10
# set=test_long_3
set=test_long_3_no_unk
ali_format=$feat_dir/$set/data.list
ali_result_dir=$feat_dir/$set/result
ali_result=$ali_result_dir/ali

mkdir -p $ali_result_dir

. tools/parse_options.sh || exit 1;

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
    # Test model, please specify the model you want to use by --checkpoint
        python wenet/bin/alignment.py \
            --gpu -1 \
            --config $config \
            --input_file $ali_format \
            --checkpoint $checkpoint \
            --batch_size 1 \
            --dict $dict \
            --result_file $ali_result \
            --bpe_model $bpe_model \
            --gen_praat
fi
