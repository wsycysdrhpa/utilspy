使用wenet/tools/alignment.sh脚本第-1步数据准备需要再用下面脚本转换，也可以直接用data.list:
ali_tmp_file_to_list.py

生成对齐标签后需要特殊处理下，生成时间戳：
parser_from_alignment.py

注：
长语音每个句子用<unk>进行分割
