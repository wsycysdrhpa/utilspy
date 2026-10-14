#!/usr/bin/env python
# coding: utf-8
"""统计指定目录下音频文件的总时长。"""

import argparse
import os
import sys
from os.path import dirname

from tqdm import tqdm
import librosa

CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_PROJECT_PATH = dirname(dirname(CURRENT_FILE_PATH))
sys.path.append(CURRENT_PROJECT_PATH)


AUDIO_EXTENSIONS = {
    '.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac',
    '.wma', '.opus', '.amr', '.webm', '.mp4',
}


def get_file_duration(file):
    return librosa.get_duration(filename=file)


def format_duration(seconds):
    """将秒数格式化为 HH:MM:SS.xxx。"""
    if seconds < 0:
        seconds = 0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def collect_audio_files(audio_dir, recursive=True):
    """收集目录下的音频文件路径。"""
    audio_files = []
    if recursive:
        for root, _, files in os.walk(audio_dir):
            for name in files:
                ext = os.path.splitext(name)[1].lower()
                if ext in AUDIO_EXTENSIONS:
                    audio_files.append(os.path.join(root, name))
    else:
        for name in os.listdir(audio_dir):
            path = os.path.join(audio_dir, name)
            if not os.path.isfile(path):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in AUDIO_EXTENSIONS:
                audio_files.append(path)
    return sorted(audio_files)


def main():
    parser = argparse.ArgumentParser(description='统计音频目录总时长')
    parser.add_argument('audio_dir', type=str, help='音频目录路径')
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='不递归子目录，只统计当前目录',
    )
    parser.add_argument(
        '--detail',
        action='store_true',
        help='打印每个文件的时长',
    )
    args = parser.parse_args()

    audio_dir = os.path.abspath(args.audio_dir)
    if not os.path.isdir(audio_dir):
        print(f'错误: 目录不存在: {audio_dir}', file=sys.stderr)
        sys.exit(1)

    audio_files = collect_audio_files(audio_dir, recursive=not args.no_recursive)
    if not audio_files:
        print(f'未找到音频文件: {audio_dir}')
        sys.exit(0)

    total_duration = 0.0
    failed = []

    for path in tqdm(audio_files, desc='统计时长', unit='file'):
        try:
            duration = get_file_duration(path)
            total_duration += duration
            if args.detail:
                rel = os.path.relpath(path, audio_dir)
                print(f'{rel}\t{duration:.3f}s\t{format_duration(duration)}')
        except Exception as e:
            failed.append((path, str(e)))

    print('=' * 50)
    print(f'目录: {audio_dir}')
    print(f'音频文件数: {len(audio_files)}')
    print(f'成功: {len(audio_files) - len(failed)}')
    print(f'失败: {len(failed)}')
    print(f'总时长(秒): {total_duration:.3f}')
    print(f'总时长: {format_duration(total_duration)}')
    if total_duration >= 3600:
        print(f'总时长(小时): {total_duration / 3600:.3f} h')

    if failed:
        print('-' * 50)
        print('失败文件:')
        for path, err in failed:
            print(f'  {path}: {err}')


if __name__ == '__main__':
    main()
