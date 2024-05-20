from logging import getLogger

from transformers import MPNetModel, MPNetTokenizer
import os
import numpy as np

logger = getLogger("uvicorn.app")


def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


def load_model(model_path):
    model = MPNetModel.from_pretrained(model_path)
    tokenizer = MPNetTokenizer.from_pretrained(model_path)

    return model, tokenizer


def generate_text_from_data(table_name, column_name, values):
    # TODO: Implement the logic to switch between different types of columns
    values = [str(value) for value in values]
    value_set = set(values)
    max_length = max(len(value) for value in values)
    min_length = min(len(value) for value in values)
    mean_length = np.mean([len(value) for value in values])

    text = f"{table_name}.{column_name} contains {len(values)} values (max: {max_length}, min: {min_length}, mean: {round(mean_length, 1)}): {', '.join(value_set)}."
    return text
