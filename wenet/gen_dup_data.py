import jsonlines


in_file = '/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_1_10h/merged_10h/data.list'
dst_file = '/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_1_10h/merged_10h/data.list.dup6'
dup_num = 6

# in_file = '/workspace/hongjie/work/wenet/examples/urdu/s0/data/pak_8k_wiz_annot_20230217/data.list'
# dst_file = '/workspace/hongjie/work/wenet/examples/urdu/s0/data/pak_8k_wiz_annot_20230217/data.list.dup6'
# dup_num = 6

with jsonlines.open(in_file, "r") as src_fp, \
    jsonlines.open(dst_file, 'w') as dst_fp:
    for line in src_fp:
        for i in range(dup_num):
            res = line.copy()
            res['key'] = "%s_%s_%s" % (line['key'], 'duplicates', i)
            dst_fp.write(res)
