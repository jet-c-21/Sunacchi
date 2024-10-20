import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from sunacchi.utils.network_tool.proxy import create_free_proxy_server_csv_from_free_proxy_list_dot_net

if __name__ == '__main__':
    output_csv_path = PROJECT_DIR / 'proxy_servers_files' / 'free-proxy-list.csv'
    create_free_proxy_server_csv_from_free_proxy_list_dot_net(output_csv_path)
    print(f"[INFO] - output_csv_path: {output_csv_path}")
