def split_and_duplicate_keys(dictionary, max_chunk_size):
    """
    Splits the values of a given dictionary into chunks of a specified size and duplicates the keys.
    
    Parameters:
    - dictionary (dict): The input dictionary where keys are strings and values are strings to be split.
    - max_chunk_size (int): The maximum size for each chunk of the string values.

    Returns:
    dict: A new dictionary with duplicated keys and split values. The original values in the input
          dictionary remain unchanged. The keys for the split values include the original key for
          the first chunk, and additional keys with a suffix ' part_' and the chunk index for the
          subsequent chunks.
    """
    new_dict = {}

    for key, value in dictionary.items():
        chunks = [value[i:i + max_chunk_size] for i in range(0, len(value), max_chunk_size)]
        
        # Duplicate the key for each chunk (excluding the first chunk)
        keys = [key] + [key + f' part_{i + 1}' for i in range(len(chunks) - 1)]
        
        # Assign each key its corresponding chunk
        new_dict.update({k: v for k, v in zip(keys, chunks)})

    return new_dict