#!/usr/bin/env python
# coding: utf-8
"""统计音频总时长。

支持：
  - 音频目录（递归/非递归）
  - wav_list：一行一个音频路径
  - wav_scp：Kaldi 风格 `utt_id path`
  - data_list：jsonlines，含 start/end 则用 end-start，否则读 wav 字段算时长

时长计算优先读文件头，避免解码整段音频。
实测（20 个 wav，occ_asr 环境）约：
  wave       ~0.02 ms/file
  soundfile  ~0.14 ms/file
  librosa    ~0.50 ms/file
  soxi       ~4.6  ms/file
  sox-stat   ~5.3  ms/file
排序：wave ≈ soundfile >> librosa >> soxi ≈ sox-stat
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import wave
from concurrent.futures import ProcessPoolExecutor, as_completed
from os.path import dirname

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    def tqdm(iterable, **kwargs):
        return iterable

CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_PROJECT_PATH = dirname(dirname(CURRENT_FILE_PATH))
sys.path.append(CURRENT_PROJECT_PATH)

AUDIO_EXTENSIONS = {
    '.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac',
    '.wma', '.opus', '.amr', '.webm', '.mp4',
}

# 可选依赖：有则用更快/更通用的后端
try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except Exception:
    HAS_SOUNDFILE = False

try:
    import librosa
    HAS_LIBROSA = True
except Exception:
    HAS_LIBROSA = False


def format_duration(seconds: float) -> str:
    """将秒数格式化为 HH:MM:SS.xxx。"""
    if seconds < 0:
        seconds = 0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def duration_wave(path: str) -> float:
    with wave.open(path, 'rb') as w:
        return w.getnframes() / float(w.getframerate())


def duration_soundfile(path: str) -> float:
    return float(sf.info(path).duration)


def duration_soxi(path: str) -> float:
    result = subprocess.run(
        ['soxi', '-D', path],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def duration_sox(path: str) -> float:
    """兼容旧脚本 `sox file -n stat` 的 Length 输出。"""
    result = subprocess.run(
        ['sox', path, '-n', 'stat'],
        capture_output=True,
        text=True,
    )
    for line in (result.stderr or '').splitlines():
        if 'Length' in line and ':' in line:
            return float(line.split(':', 1)[1].strip())
    raise RuntimeError(f'sox 未返回 Length: {path}')


def duration_librosa(path: str) -> float:
    # librosa 0.10+ 用 path=；旧版用 filename=
    try:
        return float(librosa.get_duration(path=path))
    except TypeError:
        return float(librosa.get_duration(filename=path))


def _which(cmd: str) -> bool:
    from shutil import which
    return which(cmd) is not None


def resolve_backend(preferred: str = 'auto') -> str:
    """选择时长计算后端标签（用于日志）。auto 实际按文件后缀动态择优。"""
    if preferred != 'auto':
        return preferred
    # 实测约 ms/file：wave 0.02 / soundfile 0.14 / librosa 0.50 / soxi 4.6 / sox 5.3
    if HAS_SOUNDFILE:
        return 'auto(wave|soundfile)'
    return 'auto(wave|soxi|sox)'


BACKEND_FUNCS = {
    'soundfile': duration_soundfile,
    'wave': duration_wave,
    'soxi': duration_soxi,
    'sox': duration_sox,
    'librosa': duration_librosa,
}


def _backend_order(path: str, preferred: str) -> list:
    ext = os.path.splitext(path)[1].lower()
    if preferred != 'auto':
        order = [preferred]
    elif ext == '.wav':
        # wav：stdlib wave 最快，无需第三方
        order = ['wave', 'soundfile', 'librosa', 'soxi', 'sox']
    else:
        order = ['soundfile', 'librosa', 'soxi', 'sox', 'wave']

    for cand in ('wave', 'soundfile', 'librosa', 'soxi', 'sox'):
        if cand not in order:
            order.append(cand)
    return order


def get_file_duration(path: str, backend: str = 'auto') -> float:
    """按 backend 计算时长；失败时自动回退。"""
    errors = []
    ext = os.path.splitext(path)[1].lower()

    for cand in _backend_order(path, backend):
        if cand == 'soundfile' and not HAS_SOUNDFILE:
            continue
        if cand == 'librosa' and not HAS_LIBROSA:
            continue
        if cand == 'wave' and ext not in ('.wav',):
            continue
        if cand == 'soxi' and not _which('soxi'):
            continue
        if cand == 'sox' and not _which('sox'):
            continue
        try:
            return BACKEND_FUNCS[cand](path)
        except Exception as e:
            errors.append(f'{cand}: {e}')
            continue
    raise RuntimeError('; '.join(errors) if errors else '无可用后端')


def _worker(args):
    path, backend = args
    try:
        return path, get_file_duration(path, backend), None
    except Exception as e:
        return path, None, str(e)


def collect_audio_files(audio_dir: str, recursive: bool = True) -> list:
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


def load_wav_list(list_file: str) -> list:
    """一行一个音频路径；空行与 # 注释忽略。"""
    paths = []
    with open(list_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            paths.append(line)
    return paths


def load_wav_scp(scp_file: str) -> list:
    """Kaldi wav.scp：`utt_id path`，取第二列及之后拼回路径。"""
    paths = []
    with open(scp_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
            paths.append(parts[1].strip())
    return paths


def load_data_list(list_file: str) -> list:
    """加载 data.list（jsonlines）。

    返回条目列表，每项为 dict：
      - label: 显示用 key / wav
      - duration: 若已有 start/end 则为 end-start，否则 None
      - wav: 需要读文件时的路径，否则 None
    """
    items = []
    with open(list_file, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f'data_list 第 {lineno} 行 JSON 解析失败: {e}') from e

            label = obj.get('key') or obj.get('wav') or f'line_{lineno}'
            if 'start' in obj and 'end' in obj:
                items.append({
                    'label': label,
                    'duration': float(obj['end']) - float(obj['start']),
                    'wav': None,
                })
            elif 'wav' in obj:
                items.append({
                    'label': label,
                    'duration': None,
                    'wav': obj['wav'],
                })
            else:
                raise ValueError(
                    f'data_list 第 {lineno} 行缺少 start/end 或 wav: {line[:120]}'
                )
    return items


def detect_input(path: str) -> tuple:
    """返回 (mode, path)，mode in {dir, wav_list, wav_scp, data_list}。"""
    path = os.path.abspath(path)
    if os.path.isdir(path):
        return 'dir', path
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # jsonlines / data.list
            if line.startswith('{'):
                return 'data_list', path
            parts = line.split()
            if len(parts) >= 2:
                candidate = parts[-1]
                if os.path.sep in candidate or candidate.endswith(
                    tuple(AUDIO_EXTENSIONS)
                ):
                    # 若整行本身是路径则仍当 wav_list
                    if os.path.exists(line):
                        return 'wav_list', path
                    return 'wav_scp', path
            return 'wav_list', path
    return 'wav_list', path


def compute_durations(audio_files, backend='auto', workers=1, detail=False, base_dir=None):
    total_duration = 0.0
    failed = []
    backend_name = resolve_backend(backend)
    # 传给 worker 的是用户原始 backend（含 auto），便于按后缀择优
    tasks = [(p, backend) for p in audio_files]

    if workers and workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(_worker, t) for t in tasks]
            for fut in tqdm(as_completed(futures), total=len(futures), desc='统计时长', unit='file'):
                path, duration, err = fut.result()
                if err is not None:
                    failed.append((path, err))
                    continue
                total_duration += duration
                if detail:
                    label = os.path.relpath(path, base_dir) if base_dir else path
                    print(f'{label}\t{duration:.3f}s\t{format_duration(duration)}')
    else:
        for path in tqdm(audio_files, desc='统计时长', unit='file'):
            try:
                duration = get_file_duration(path, backend)
                total_duration += duration
                if detail:
                    label = os.path.relpath(path, base_dir) if base_dir else path
                    print(f'{label}\t{duration:.3f}s\t{format_duration(duration)}')
            except Exception as e:
                failed.append((path, str(e)))

    return total_duration, failed, backend_name


def compute_data_list_durations(items, backend='auto', workers=1, detail=False):
    """统计 data_list：优先用 start/end，否则读 wav。"""
    total_duration = 0.0
    failed = []
    backend_name = resolve_backend(backend)

    # 已有 start/end 的条目直接累加
    need_read = []
    for it in items:
        if it['duration'] is not None:
            total_duration += it['duration']
            if detail:
                print(f"{it['label']}\t{it['duration']:.3f}s\t{format_duration(it['duration'])}")
        else:
            need_read.append(it)

    if not need_read:
        return total_duration, failed, backend_name, len(items)

    if workers and workers > 1:
        tasks = [(it['wav'], backend) for it in need_read]
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(_worker, t) for t in tasks]
            for fut in tqdm(as_completed(futures), total=len(futures), desc='统计时长', unit='file'):
                path, duration, err = fut.result()
                if err is not None:
                    failed.append((path, err))
                    continue
                total_duration += duration
                if detail:
                    print(f'{path}\t{duration:.3f}s\t{format_duration(duration)}')
    else:
        for it in tqdm(need_read, desc='统计时长', unit='file'):
            try:
                duration = get_file_duration(it['wav'], backend)
                total_duration += duration
                if detail:
                    print(f"{it['label']}\t{duration:.3f}s\t{format_duration(duration)}")
            except Exception as e:
                failed.append((it['wav'], str(e)))

    return total_duration, failed, backend_name, len(items)


def _print_summary(src, mode, backend_name, total_count, failed, total_duration):
    print('=' * 50)
    print(f'输入: {src}')
    print(f'模式: {mode}')
    print(f'后端: {backend_name}')
    print(f'条目数: {total_count}')
    print(f'成功: {total_count - len(failed)}')
    print(f'失败: {len(failed)}')
    print(f'总时长(秒): {total_duration:.3f}')
    print(f'总时长: {format_duration(total_duration)}')
    # 兼容旧 shell / data_list 脚本输出
    print(f'{total_duration}s')
    print(f'{total_duration / 3600}h')
    if total_duration >= 3600:
        print(f'总时长(小时): {total_duration / 3600:.3f} h')

    if failed:
        print('-' * 50)
        print('失败文件:')
        for path, err in failed:
            print(f'  {path}: {err}')


def _run_bench(audio_files):
    import time

    candidates = []
    if HAS_SOUNDFILE:
        candidates.append('soundfile')
    candidates.append('wave')
    if _which('soxi'):
        candidates.append('soxi')
    if _which('sox'):
        candidates.append('sox')
    if HAS_LIBROSA:
        candidates.append('librosa')

    sample = audio_files[: min(50, len(audio_files))]
    print(f'基准测试文件数: {len(sample)}')
    for name in candidates:
        if name == 'wave' and any(
            os.path.splitext(p)[1].lower() != '.wav' for p in sample
        ):
            print(f'{name:12s}  skip (含非 wav)')
            continue
        try:
            get_file_duration(sample[0], name)
            t0 = time.perf_counter()
            total = 0.0
            for p in sample:
                total += get_file_duration(p, name)
            elapsed = time.perf_counter() - t0
            print(
                f'{name:12s}  {elapsed*1000:8.1f} ms  '
                f'{elapsed/len(sample)*1000:6.2f} ms/file  total={total:.3f}s'
            )
        except Exception as e:
            print(f'{name:12s}  FAIL: {e}')


def main():
    parser = argparse.ArgumentParser(
        description='统计音频总时长（目录 / wav_list / wav_scp / data_list）',
    )
    parser.add_argument(
        'input',
        type=str,
        nargs='?',
        default=None,
        help='音频目录，或 wav_list / wav_scp / data_list 文件',
    )
    parser.add_argument('--dir', dest='audio_dir', type=str, help='音频目录')
    parser.add_argument(
        '--wav-list',
        type=str,
        help='wav_list 文件：一行一个音频路径',
    )
    parser.add_argument(
        '--wav-scp',
        type=str,
        help='Kaldi wav.scp：utt_id path',
    )
    parser.add_argument(
        '--data-list',
        type=str,
        help='data.list（jsonlines）：有 start/end 用差值，否则读 wav',
    )
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='目录模式不递归子目录',
    )
    parser.add_argument(
        '--detail',
        action='store_true',
        help='打印每个文件的时长',
    )
    parser.add_argument(
        '--backend',
        type=str,
        default='auto',
        choices=['auto', 'soundfile', 'wave', 'soxi', 'sox', 'librosa'],
        help='时长计算后端（默认 auto=最快可用）',
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='并行进程数（>1 时多进程；文件很多时可加速）',
    )
    parser.add_argument(
        '--bench',
        action='store_true',
        help='对同一批文件对比各后端耗时后退出',
    )
    args = parser.parse_args()

    mode = None
    src = None
    base_dir = None

    if args.data_list:
        mode, src = 'data_list', os.path.abspath(args.data_list)
    elif args.wav_list:
        mode, src = 'wav_list', os.path.abspath(args.wav_list)
    elif args.wav_scp:
        mode, src = 'wav_scp', os.path.abspath(args.wav_scp)
    elif args.audio_dir:
        mode, src = 'dir', os.path.abspath(args.audio_dir)
    elif args.input:
        try:
            mode, src = detect_input(args.input)
        except FileNotFoundError:
            print(f'错误: 路径不存在: {args.input}', file=sys.stderr)
            sys.exit(1)
    else:
        parser.error('请指定 input，或 --dir / --wav-list / --wav-scp / --data-list')

    if mode == 'dir':
        if not os.path.isdir(src):
            print(f'错误: 目录不存在: {src}', file=sys.stderr)
            sys.exit(1)
        audio_files = collect_audio_files(src, recursive=not args.no_recursive)
        base_dir = src
        if not audio_files:
            print(f'未找到音频文件: {src}')
            sys.exit(0)
        if args.bench:
            _run_bench(audio_files)
            sys.exit(0)
        total_duration, failed, backend_name = compute_durations(
            audio_files,
            backend=args.backend,
            workers=args.workers,
            detail=args.detail,
            base_dir=base_dir,
        )
        _print_summary(src, mode, backend_name, len(audio_files), failed, total_duration)
        return

    if not os.path.isfile(src):
        print(f'错误: 文件不存在: {src}', file=sys.stderr)
        sys.exit(1)

    if mode == 'data_list':
        items = load_data_list(src)
        if not items:
            print(f'未找到条目: {src}')
            sys.exit(0)
        if args.bench:
            bench_paths = [it['wav'] for it in items if it['wav']]
            if not bench_paths:
                print('data_list 条目均含 start/end，无需读音频，跳过 --bench')
                sys.exit(0)
            _run_bench(bench_paths)
            sys.exit(0)
        total_duration, failed, backend_name, total_count = compute_data_list_durations(
            items,
            backend=args.backend,
            workers=args.workers,
            detail=args.detail,
        )
        _print_summary(src, mode, backend_name, total_count, failed, total_duration)
        return

    if mode == 'wav_list':
        audio_files = load_wav_list(src)
    else:  # wav_scp
        audio_files = load_wav_scp(src)

    if not audio_files:
        print(f'未找到音频文件: {src}')
        sys.exit(0)
    if args.bench:
        _run_bench(audio_files)
        sys.exit(0)

    total_duration, failed, backend_name = compute_durations(
        audio_files,
        backend=args.backend,
        workers=args.workers,
        detail=args.detail,
        base_dir=base_dir,
    )
    _print_summary(src, mode, backend_name, len(audio_files), failed, total_duration)


if __name__ == '__main__':
    main()
