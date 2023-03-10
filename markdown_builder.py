import os
import uuid
import json

curr_dir = os.path.dirname(os.path.realpath(__file__))
poem_data_dir = os.path.join(curr_dir, "poem_data")


class Poem:
    def __init__(self, title, author, content, create_date):
        self.id = uuid.uuid4().hex
        self.title = title
        self.author = author
        self.content = content
        self.create_date = create_date


def load_poems(file_path):
    poem_list = []
    file_path = os.path.join(poem_data_dir, file_path)
    with open(file_path, "r") as f:
        temp_poem_list = json.loads(f.read())
        for poem in temp_poem_list:
            poem_list.append(Poem(poem["title"], poem["author"], poem["content"], poem["create_date"]))
    return poem_list


def create_markdown(poem: Poem, next_poem_id: str, next_poem_title: str):
    content = "\\\n".join(poem.content)
    page_content = f"# {poem.title}\n" \
                   f"{poem.author}\n\n" \
                   f"{content}\n" \
                   f"{poem.create_date if poem.create_date else ''}\n\n" \
                   f"[{next_poem_title}]({next_poem_id}.md)\n"
    return page_content


def write_poem(poem: Poem, next_poem_id: str, next_poem_title: str):
    with open(f"{poem.id}.md", "w") as f:
        f.write(create_markdown(poem, next_poem_id, next_poem_title))


def create_pages():
    poems = load_poems("poems_1.json")
    poem_amount = len(poems)
    for i in range(poem_amount):
        if i + 1 < poem_amount:
            write_poem(poems[i], poems[i + 1].id, poems[i + 1].title)
        if i + 1 == poem_amount:
            write_poem(poems[i], "", "")


create_pages()
