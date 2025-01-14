from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import os
import yaml

# TODO: add option for incremental indexing
def build_index(data_folder, index_folder):
    # Define the schema for the first level
    schema = Schema(folder=ID(stored=True), content=TEXT, tag=ID(stored=True))

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
                            writer.add_document(folder=sub_folder, tag=tag_folder, content=content)

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


def just_search(query_str, ix, retrieves: list):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        return [dict(result) for result in results]

def search_from_existing_index(query_str):
    index_folder = "index"
    ix = open_dir(index_folder)
    return just_search(query_str, ix, "folder")

def search_from_existing_sub_index(query_str, tag_folder):
    sub_indices_folder = "sub_indices"
    tag_index_folder = os.path.join(sub_indices_folder, tag_folder)
    ix = open_dir(tag_index_folder)
    return just_search(query_str, ix, "file")

def retrieve_pdf_path(tag, folder, data_folder="data"):
    yaml_file_path = os.path.join(data_folder, tag, folder, f"{folder}.yaml")
    if os.path.exists(yaml_file_path):
        with open(yaml_file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data.get("pdf_path", None)
    return None

def retrieve_img_path(tag_folder, img_base_name, data_folder="data"):
    img_path = os.path.join(data_folder, tag_folder, f"{img_base_name}.png")
    if os.path.exists(img_path):
        return img_path
    return None


if __name__ == "__main__":
    # Build the first level index
    data_folder = "data"
    index_folder = "index"
    ix = build_index(data_folder, index_folder)
    # Build the second level indices
    build_all_sub_indices(data_folder)

    # results = search_from_existing_index("machine learning")
    # print(results)
    # results = search_from_existing_sub_index("Imperial COllege London", "RL_Probabilities/RL 1.1 - Introduction")
    # print(results)
    # print(retrieve_img_path("RL_Probabilities", "RL 1.1 - Introduction", "RL 1.1 - Introduction_p14"))
