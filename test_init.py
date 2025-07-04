import shutil
from pathlib import Path

def dir_clear(target_dir):
    if target_dir.exists() and target_dir.is_dir():
        # 删除整个目录（包括内容）
        shutil.rmtree(target_dir, ignore_errors=True)  # ignore_errors忽略权限等问题
        # 重新创建目录
        target_dir.mkdir()
    else:
        target_dir.mkdir(exist_ok=True)

if __name__ == "__main__":
    # 定义目标目录
    chat_dir = Path("chat")
    vote_dir = Path("vote")
    against_dir = Path("against")
    revote_dir = Path("revote")

    # 清空目标目录
    dir_clear(chat_dir)
    dir_clear(vote_dir)
    dir_clear(against_dir)
    dir_clear(revote_dir)