import argparse
import pathlib
import pysuerga


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Static site generator for open source projects')
    parser.add_argument('source_path', help='path to the source directory containing config.yml')
    parser.add_argument('--target-path', default='build', help='directory to write the output')
    parser.add_argument('--base-url', default='', help='base url where the website is served from')
    parser.add_argument('--remove-target', action='store_true',
                        help='remove the content of the target directory')
    args = parser.parse_args()
    pysuerga.main(pathlib.Path(args.source_path),
                  pathlib.Path(args.target_path),
                  args.base_url,
                  args.remove_target)
