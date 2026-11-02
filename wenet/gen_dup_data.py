import jsonlines
import argparse


def main():
    parser = argparse.ArgumentParser(description="Duplicate jsonlines data")

    parser.add_argument("--in_file", type=str, required=True,
                        help="Input jsonlines file")
    parser.add_argument("--dst_file", type=str, required=True,
                        help="Output jsonlines file")
    parser.add_argument("--dup_num", type=int, default=3,
                        help="Number of duplicates for each sample (default: 3)")

    args = parser.parse_args()

    with jsonlines.open(args.in_file, "r") as src_fp, \
            jsonlines.open(args.dst_file, "w") as dst_fp:
        for line in src_fp:
            for i in range(args.dup_num):
                res = line.copy()
                res["key"] = "%s_%s_%s" % (
                    line["key"], "duplicates", i
                )
                dst_fp.write(res)


if __name__ == "__main__":
    main()
