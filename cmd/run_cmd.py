#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程执行shell命令脚本
支持从文件读取命令列表，多线程并发执行，超时机制
"""

import os
import sys
import time
import threading
import subprocess
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple


class CommandExecutor:
    """命令执行器类"""

    def __init__(self, timeout: int = 15, max_workers: int = 10):
        """
        初始化命令执行器

        Args:
            timeout: 命令执行超时时间（秒）
            max_workers: 最大线程数
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.results = []
        self.lock = threading.Lock()

        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('command_execution.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def execute_command(self, command: str, index: int) -> Tuple[int, str, str, bool, float]:
        """
        执行单个命令

        Args:
            command: 要执行的命令
            index: 命令索引

        Returns:
            (索引, 命令, 输出, 是否成功, 执行时间)
        """
        start_time = time.time()
        self.logger.info(f"开始执行命令 {index}: {command}")

        try:
            # 使用subprocess执行命令，设置超时
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding='utf-8'
            )

            execution_time = time.time() - start_time

            if result.returncode == 0:
                self.logger.info(f"命令 {index} 执行成功，耗时: {execution_time:.2f}秒")
                return (index, command, result.stdout, True, execution_time)
            else:
                self.logger.warning(f"命令 {index} 执行失败，返回码: {result.returncode}")
                return (index, command, result.stderr, False, execution_time)

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            self.logger.error(f"命令 {index} 执行超时 ({self.timeout}秒)")
            return (index, command, f"命令执行超时 ({self.timeout}秒)", False, execution_time)

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"命令执行异常: {str(e)}"
            self.logger.error(f"命令 {index} 执行异常: {error_msg}")
            return (index, command, error_msg, False, execution_time)

    def execute_commands_from_file(self, file_path: str) -> List[Tuple[int, str, str, bool, float]]:
        """
        从文件读取命令并多线程执行

        Args:
            file_path: 包含命令的文件路径

        Returns:
            执行结果列表
        """
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在: {file_path}")
            return []

        # 读取命令列表
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                commands = [line.strip() for line in f if line.strip()]

            if not commands:
                self.logger.warning("文件中没有找到有效的命令")
                return []

            self.logger.info(f"从文件 {file_path} 读取到 {len(commands)} 个命令")

        except Exception as e:
            self.logger.error(f"读取文件失败: {str(e)}")
            return []

        # 多线程执行命令
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_index = {
                executor.submit(self.execute_command, cmd, i): i
                for i, cmd in enumerate(commands)
            }

            # 收集结果
            for future in as_completed(future_to_index):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    index = future_to_index[future]
                    self.logger.error(f"获取命令 {index} 结果时发生异常: {str(e)}")
                    results.append((index, commands[index], f"获取结果异常: {str(e)}", False, 0.0))

        # 按索引排序结果
        results.sort(key=lambda x: x[0])
        return results

    def print_summary(self, results: List[Tuple[int, str, str, bool, float]]):
        """
        打印执行摘要

        Args:
            results: 执行结果列表
        """
        if not results:
            self.logger.info("没有执行结果")
            return

        total_commands = len(results)
        successful_commands = sum(1 for _, _, _, success, _ in results if success)
        failed_commands = total_commands - successful_commands
        total_time = sum(time for _, _, _, _, time in results)
        avg_time = total_time / total_commands if total_commands > 0 else 0

        self.logger.info("=" * 60)
        self.logger.info("执行摘要:")
        self.logger.info(f"总命令数: {total_commands}")
        self.logger.info(f"成功执行: {successful_commands}")
        self.logger.info(f"执行失败: {failed_commands}")
        self.logger.info(f"总耗时: {total_time:.2f}秒")
        self.logger.info(f"平均耗时: {avg_time:.2f}秒")
        self.logger.info("=" * 60)

        # 打印失败的命令
        if failed_commands > 0:
            self.logger.info("失败的命令:")
            for index, command, output, success, exec_time in results:
                if not success:
                    self.logger.info(f"  {index}: {command}")
                    self.logger.info(f"    错误: {output}")
                    self.logger.info(f"    耗时: {exec_time:.2f}秒")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='多线程执行shell命令')
    parser.add_argument('file', help='包含命令的文件路径')
    parser.add_argument('-t', '--timeout', type=int, default=60,
                       help='命令执行超时时间（秒），默认60秒')
    parser.add_argument('-w', '--workers', type=int, default=10,
                       help='最大线程数，默认10')
    parser.add_argument('-o', '--output', help='结果输出文件路径（可选）')

    args = parser.parse_args()

    # 创建命令执行器
    executor = CommandExecutor(timeout=args.timeout, max_workers=args.workers)

    # 执行命令
    results = executor.execute_commands_from_file(args.file)

    # 打印摘要
    executor.print_summary(results)

    # 保存详细结果到文件
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write("命令执行详细结果\n")
                f.write("=" * 60 + "\n")
                for index, command, output, success, exec_time in results:
                    f.write(f"命令 {index}: {command}\n")
                    f.write(f"状态: {'成功' if success else '失败'}\n")
                    f.write(f"耗时: {exec_time:.2f}秒\n")
                    f.write(f"输出:\n{output}\n")
                    f.write("-" * 40 + "\n")
            executor.logger.info(f"详细结果已保存到: {args.output}")
        except Exception as e:
            executor.logger.error(f"保存结果文件失败: {str(e)}")


if __name__ == "__main__":
    main()
