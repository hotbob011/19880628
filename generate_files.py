#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from datetime import datetime


def format_current_time() -> str:
	# Use YYYY/M/D HH:MM:SS with non-padded month/day
	now = datetime.now()
	return f"{now.year}/{now.month}/{now.day} {now.strftime('%H:%M:%S')}"


def load_input_json(path: str) -> dict:
	with open(path, 'r', encoding='utf-8') as f:
		return json.load(f)


def transform_group(group_items):
	"""Transform input accounts into the required minimal schema.

	Each output item has: id, fullEmail, password, checkTime(now), status(正常), regionName(美国)
	The id is reassigned sequentially as 1-n.
	"""
	output_items = []
	current_time = format_current_time()
	for index, item in enumerate(group_items, start=1):
		full_email = item.get('fullEmail', '')
		password = item.get('password', '')
		output_items.append({
			'id': f'1-{index}',
			'fullEmail': full_email,
			'password': password,
			'checkTime': current_time,
			'status': '正常',
			'regionName': '美国',
		})
	return output_items


def write_txt(groups, txt_output_path: str):
	lines = []
	for item in groups:
		lines.append(f"\"id\": \"{item['id']}\"")
		lines.append(item.get('fullEmail', ''))
		lines.append(item.get('password', ''))
		lines.append(item.get('checkTime', ''))
		lines.append('')  # blank line to ensure two newlines between groups when joined
	# Join with newline; an extra blank ensures two consecutive newlines between groups
	content = "\n".join(lines).strip() + "\n"
	with open(txt_output_path, 'w', encoding='utf-8') as f:
		f.write(content)


def write_json(groups, json_output_path: str):
	payload = {
		'timestamp': int(time.time()),
		'data': {
			'accounts': {
				'group1': groups
			}
		}
	}
	with open(json_output_path, 'w', encoding='utf-8') as f:
		json.dump(payload, f, ensure_ascii=False, indent=4)


def main():
	parser = argparse.ArgumentParser(description='Transform accounts JSON into TXT and formatted JSON outputs')
	parser.add_argument('--input', required=True, help='Path to input JSON file containing data.accounts.group1')
	parser.add_argument('--txt-output', default='/workspace/accounts_group1.txt', help='Path to write TXT output')
	parser.add_argument('--json-output', default='/workspace/accounts_group1_formatted.json', help='Path to write JSON output')
	args = parser.parse_args()

	data = load_input_json(args.input)
	group_items = (((data or {}).get('data') or {}).get('accounts') or {}).get('group1') or []
	groups = transform_group(group_items)
	write_txt(groups, args.txt_output)
	write_json(groups, args.json_output)
	print(f"Wrote TXT -> {args.txt_output}")
	print(f"Wrote JSON -> {args.json_output}")


if __name__ == '__main__':
	main()