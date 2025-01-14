from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import os


def build_index(data_folder, index_folder):
    # Define the schema for the first level
    schema = Schema(folder=ID(stored=True), content=TEXT)

    if not os.path.exists(index_folder):
        print(f"Creating index folder at {index_folder}")
        os.makedirs(index_folder)

    # Create the index for the first level
    ix = create_in(index_folder, schema)

    # Open the index for writing
    writer = ix.writer()

    # Index all <folder>/<folder>.txt files in the data folder
    for tag_folder in os.listdir(data_folder):
        tag_folder_path = os.path.join(data_folder, tag_folder)
        if os.path.isdir(tag_folder_path):
            for sub_folder in os.listdir(tag_folder_path):
                sub_folder_path = os.path.join(tag_folder_path, sub_folder)
                if os.path.isdir(sub_folder_path):
                    txt_file_path = os.path.join(sub_folder_path, f"{sub_folder}.txt")
                    if os.path.exists(txt_file_path):
                        with open(txt_file_path, "r", encoding="utf-8") as file:
                            content = file.read()
                            writer.add_document(folder=sub_folder, content=content)

    # Commit the changes
    writer.commit()

    return ix


def build_all_sub_indices(data_folder):
    sub_indices_folder = "sub_indices"
    if not os.path.exists(sub_indices_folder):
        os.makedirs(sub_indices_folder)

    for tag_folder in os.listdir(data_folder):
        tag_folder_path = os.path.join(data_folder, tag_folder)
        if os.path.isdir(tag_folder_path):
            for sub_folder in os.listdir(tag_folder_path):
                sub_folder_path = os.path.join(tag_folder_path, sub_folder)
                if os.path.isdir(sub_folder_path):
                    tag_index_folder = os.path.join(sub_indices_folder, f"{tag_folder}/{sub_folder}")
                    build_sub_index(sub_folder_path, tag_index_folder)


def build_sub_index(folder_path, index_folder):
    # Define the schema for the second level
    schema = Schema(file=ID(stored=True), content=TEXT)

    if not os.path.exists(index_folder):
        print(f"Creating index folder at {index_folder}")
        os.makedirs(index_folder)

    # Create the index for the second level
    ix = create_in(index_folder, schema)

    # Open the index for writing
    writer = ix.writer()

    # Index all pairs of .png and .txt files in the folder, excluding <folder>.txt
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") and filename != f"{os.path.basename(folder_path)}.txt":
            base_name = filename[:-4]
            txt_file_path = os.path.join(folder_path, filename)
            with open(txt_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                writer.add_document(file=base_name, content=content)

    # Commit the changes
    writer.commit()

    return ix


def search_first_level(query_str, ix):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            print(result['folder'])


def search_second_level(query_str, ix):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            print(result['file'])


def search_from_existing_index(query_str):
    index_folder = "index"
    ix = open_dir(index_folder)
    search_first_level(query_str, ix)

def search_from_existing_sub_index(query_str, tag_folder):
    sub_indices_folder = "sub_indices"
    tag_index_folder = os.path.join(sub_indices_folder, tag_folder)
    ix = open_dir(tag_index_folder)
    search_second_level(query_str, ix)


if __name__ == "__main__":
    # # Build the first level index
    # data_folder = "data"
    # index_folder = "index"
    # ix = build_index(data_folder, index_folder)

    # # Build the second level indices
    # build_all_sub_indices(data_folder)

    search_from_existing_index("machine learning")
    search_from_existing_sub_index("Imperial COllege London", "rl/Lab 1")
