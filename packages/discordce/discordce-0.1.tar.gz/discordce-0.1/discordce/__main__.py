import argparse
import os
from shutil import copy

from discordce import exceptions


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--output', nargs="*", help="URL.", required=False)
	return parser.parse_args()


def verify_cache():
	path = os.path.join(os.getenv("APPDATA"), "discord", "Cache")
	if os.path.exists(path):
		return path
	else:
		raise exceptions.CacheNotFound("Cache was not found in the expected location: {}".format(path))


def export(cache_folder, output_folder):
	if output_folder is None:
		export_path = os.getcwd()
	else:
		export_path = output_folder[0]
	for file in os.listdir(cache_folder):
		if file.startswith("data"):
			print("Passing {}".format(file))
			pass
		elif file.startswith("index"):
			print("Passing {}".format(file))
			pass
		else:
			try:
				copy(os.path.join(cache_folder, file), os.path.join(export_path, "{}.png".format(file)))
				print("Exported {}.png".format(file))
			except FileNotFoundError:
				print("Creating directory {}".format(export_path))
				os.mkdir(export_path)
				copy(os.path.join(cache_folder, file), os.path.join(export_path, "{}.png".format(file)))
				print("Exported {}.png".format(file))


def main():
	args = get_args()
	cache_folder = verify_cache()
	export(cache_folder, args.output)


if __name__ == '__main__':
	main()
