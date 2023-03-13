import os
import uuid
import json

curr_dir = os.path.dirname(os.path.realpath(__file__))
poem_data_dir = os.path.join(curr_dir, "poem_data")
markdowns_dir = os.path.join(curr_dir, "markdowns")


class Poem:
    def __init__(self, poem_dict):
        self.id = poem_dict["id"]
        self.title = poem_dict["title"]
        self.author = poem_dict["author"]
        self.content = poem_dict["content"]
        self.create_date = poem_dict["create_date"]


def load_poems(file_path):
    file_path = os.path.join(poem_data_dir, file_path)
    with open(file_path, "r") as f:
        return json.loads(f.read())


def load_poems_as_obj(file_path):
    poem_list = []
    file_path = os.path.join(poem_data_dir, file_path)
    with open(file_path, "r") as f:
        temp_poem_list = json.loads(f.read())
        for poem in temp_poem_list:
            poem_list.append(Poem(poem))
    return poem_list


def update_poems_ids(file_path):
    poems = load_poems(file_path)
    for poem in poems:
        poem["id"] = uuid.uuid4().hex

    with open(file_path, "w", encoding='utf8') as f:
        f.write(json.dumps(poems, indent=2, ensure_ascii=False))


def create_markdown(poem, previous_poem, next_poem):
    content = "\\\n".join(poem.content) + "\n"
    if previous_poem and next_poem:
        return f"# {poem.title}\n" \
               f"{poem.author}\n\n" \
               f"{content}\n" \
               f"{poem.create_date if poem.create_date else ''}\n\n" \
               f"上一篇：[{previous_poem.title}]({previous_poem.id}.md)  " \
               f"下一篇：[{next_poem.title}]({next_poem.id}.md)\n"
    if not next_poem:
        return f"# {poem.title}\n" \
               f"{poem.author}\n\n" \
               f"{content}\n" \
               f"{poem.create_date if poem.create_date else ''}\n\n" \
               f"上一篇：[{previous_poem.title}]({previous_poem.id}.md)"
    if not previous_poem:
        return f"# {poem.title}\n" \
               f"{poem.author}\n\n" \
               f"{content}\n" \
               f"{poem.create_date if poem.create_date else ''}\n\n" \
               f"下一篇：[{next_poem.title}]({next_poem.id}.md)\n"
    if not previous_poem and next_poem:
        return f"# {poem.title}\n" \
               f"{poem.author}\n\n" \
               f"{content}\n" \
               f"{poem.create_date if poem.create_date else ''}\n\n"
    return ""


def write_poem(poem, previous_poem, next_poem):
    file_path = os.path.join(markdowns_dir, f"{poem.id}.md")
    with open(file_path, "w") as f:
        f.write(create_markdown(poem, previous_poem, next_poem))


def create_content_list_page(poems):
    file_path = os.path.join(markdowns_dir, "目录.md")
    lines = ["# 砂砾\n\n", "一小撮坏分子\n\n"]
    for poem in poems:
        lines.append(f"[{poem.title}]({poem.id}.md)\\\n")

    with open(file_path, "w") as f:
        f.writelines(lines)


def create_pages():
    poems = load_poems_as_obj("poems_1.json")
    create_content_list_page(poems)
    poems.insert(0, None)
    poems.append(None)
    poem_amount = len(poems)
    for i in range(poem_amount):
        if 2 < i < poem_amount - 1:
            write_poem(poems[i], poems[i - 1], poems[i + 1])


# update_poems_ids("poems_1.json")
create_pages()
