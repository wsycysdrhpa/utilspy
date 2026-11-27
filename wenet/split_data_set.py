import argparse
import os


FILES = ("data.list", "text", "wav.scp")


def parse_split(split, total):
    """把切分参数转成第一份的行数。

    支持：
    - 正整数：第一份的具体行数，例如 1000
    - (0, 1) 的小数：第一份占比，例如 0.9
    - 百分数：例如 90%
    - 比例：例如 9:1
    """
    text = str(split).strip()
    if not text:
        raise ValueError("切分数量不能为空")

    if ":" in text:
        left, right = text.split(":", 1)
        a = float(left)
        b = float(right)
        if a <= 0 or b <= 0:
            raise ValueError("比例两边都必须大于 0，例如 9:1")
        n1 = int(round(total * a / (a + b)))
    elif text.endswith("%"):
        ratio = float(text[:-1]) / 100.0
        if not 0 < ratio < 1:
            raise ValueError("百分比必须在 0% 和 100% 之间，例如 90%")
        n1 = int(round(total * ratio))
    elif "." in text:
        ratio = float(text)
        if not 0 < ratio < 1:
            raise ValueError("小数比例必须在 0 和 1 之间，例如 0.9")
        n1 = int(round(total * ratio))
    else:
        n1 = int(text)
        if n1 <= 0:
            raise ValueError("切分行数必须是正整数")

    if n1 <= 0 or n1 >= total:
        raise ValueError(
            "切分后两份都不能为空：总行数 %d，第一份得到 %d" % (total, n1)
        )
    return n1


def read_lines(path):
    with open(path, "r", encoding="utf-8") as fp:
        return fp.readlines()


def write_lines(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        fp.writelines(lines)


def split_dataset(in_dir, out_dir, name1, name2, split):
    if name1 == name2:
        raise ValueError("两个输出文件夹名不能相同")

    groups = {}
    for name in FILES:
        path = os.path.join(in_dir, name)
        if not os.path.isfile(path):
            raise FileNotFoundError("找不到输入文件: %s" % path)
        groups[name] = read_lines(path)

    counts = {name: len(lines) for name, lines in groups.items()}
    total = counts[FILES[0]]
    if len(set(counts.values())) != 1:
        detail = ", ".join("%s=%d" % (name, counts[name]) for name in FILES)
        raise ValueError("三个文件行数不一致: %s" % detail)
    if total == 0:
        raise ValueError("输入文件为空")

    n1 = parse_split(split, total)
    n2 = total - n1

    for name, lines in groups.items():
        write_lines(os.path.join(out_dir, name1, name), lines[:n1])
        write_lines(os.path.join(out_dir, name2, name), lines[n1:])

    print(
        "总行数 %d，%s %d 行，%s %d 行，输出到 %s"
        % (total, name1, n1, name2, n2, out_dir)
    )


def main():
    parser = argparse.ArgumentParser(
        description="按行对齐切分 data.list、text、wav.scp"
    )
    parser.add_argument("--in_dir", type=str, required=True,
                        help="输入目录，内含 data.list、text、wav.scp")
    parser.add_argument("--out_dir", type=str, required=True,
                        help="输出根目录")
    parser.add_argument("--names", nargs=2, metavar=("NAME1", "NAME2"),
                        required=True,
                        help="切分后的两个文件夹名，例如 train dev")
    parser.add_argument("--split", type=str, required=True,
                        help="第一份的切分数量：行数(1000)、比例(0.9 / 90%% / 9:1)")
    args = parser.parse_args()
    split_dataset(args.in_dir, args.out_dir, args.names[0], args.names[1], args.split)


if __name__ == "__main__":
    main()
