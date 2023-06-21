import os

print('''
通过关键字搜索指定文件夹内的内容，包括行数和该行的内容
作者：akpigs
           __                  __                    
          /  |                /  |                    
  ______  $$ |   __   ______  $$/   ______    _______ 
 /      \ $$ |  /  | /      \ /  | /      \  /       |
 $$$$$$  |$$ |_/$$/ /$$$$$$  |$$ |/$$$$$$  |/$$$$$$$/ 
 /    $$ |$$   $$<  $$ |  $$ |$$ |$$ |  $$ |$$      \ 
/$$$$$$$ |$$$$$$  \ $$ |__$$ |$$ |$$ \__$$ | $$$$$$  |
$$    $$ |$$ | $$  |$$    $$/ $$ |$$    $$ |/     $$/ 
 $$$$$$$/ $$/   $$/ $$$$$$$/  $$/  $$$$$$$ |$$$$$$$/  
                    $$ |          /  \__$$ |          
                    $$ |          $$    $$/           
                    $$/            $$$$$$/    ''')
def scan_files(folder_path, keywords):
    matched_files = []

    # 遍历文件夹内的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            # 检查文件名扩展名是否匹配，可以根据需要添加或删除扩展名
            if file_ext in ['.java', '.py', '.xml', '.sql', '.html', '.js', '.css', '.jsp', '.asp', '.md', '.log', '.php', '.txt', '.bat', '.sh', '.imi', '.conf']:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line_number, line in enumerate(lines, start=1):
                            # 检查关键字是否存在文件内容中
                            if all(keyword.lower() in line.lower() for keyword in keywords):
                                # 判断包含关键字的行数是否超过200个字符，如果超过则截断...
                                if len(line) > 200:
                                    line = line[:200] + "..."
                                matched_files.append((file_path, line_number, line.rstrip()))
                except UnicodeDecodeError:
                    print(f"Unable to decode file: {file_path}")
                except OSError:
                    print(f"Error reading file: {file_path}")

    return matched_files

while True:
    # 获取用户输入的文件夹路径，并验证路径是否存在且是文件夹，不想码字了，看不懂自己翻译....
    folder_path = input("Enter folder path（请输入文件路径）: ")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        break
    else:
        print("Invalid folder path. Please try again.")

while True:
    # 获取用户输入的关键字，并验证是否至少输入了一个关键字
    keywords_str = input("Enter keywords (separated by commas): ")
    keywords = [keyword.strip() for keyword in keywords_str.split(",")]
    if len(keywords) > 0:
        break
    else:
        print("Please enter at least one keyword.")

# 调用函数，获取匹配的文件列表
matched_files = scan_files(folder_path, keywords)
if len(matched_files) > 0:
    print("Files containing specified keywords:")
    for file_path, line_number, line_content in matched_files:
        print(f"File: {file_path}, Line: {line_number}, Content: {line_content}")
else:
    print("No files found containing specified keywords.")

input("Press Enter to exit...")
