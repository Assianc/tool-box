import subprocess


def export_database(db_url, output_file):
    dump_command = [
        'pg_dump',
        f'--dbname={db_url}',
        '-F', 'c',  # 导出为自定义格式
        '-f', output_file  # 输出文件
    ]

    subprocess.run(dump_command, check=True)


def import_database(db_url, input_file):
    restore_command = [
        'pg_restore',
        f'--dbname={db_url}',
        '-c',  # 清除目标数据库中的对象
        '-F', 'c',  # 使用自定义格式
        input_file
    ]
    subprocess.run(restore_command, check=True)


backup_file = "./backup.sql"
source_url = ""
target_url = ""
# 导出源数据库
export_database(source_url, backup_file)

# 导入到目标数据库
import_database(target_url, backup_file)
