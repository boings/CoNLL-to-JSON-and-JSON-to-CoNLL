import glob
import os 
import sys
import jsonlines

#NOTES: 
#usage command line: python json_conll.py input_folder

def get_paths(input_folder):
    """
    Stores all .txt files in a list
    Returns a list of strings of filepaths from the Text (volumes) folder
    :param inputfolder: inputfolder used in main
    """
    list_files = []
    conll_folder = glob.glob(input_folder + '/*.jsonl')
    
    for filename in conll_folder:
        list_files.append(filename)

    return list_files

def load_text(txt_path):
    """
    Opens the container en reads the elements(strings)
    Returns a string
    :param txt_path: list with filepaths
    """
    with jsonlines.open(txt_path, 'r') as json_file:
        content = [json_obj for json_obj in json_file]
    
    return content

def process_and_write(loaded_dicts, input_folder, text):
    """
    Process each CONLL and write to file
    :param paths: content of json file
    :param input_folder: folder with json files
    :param text: pathname of json file
    """
    directory = 'conll-dir'
    
    #check if dir exists, if not make one
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    #get basename of path and change extension to '.conll'
    base = os.path.basename(text)[:-6]
    conll_str = '.conll'
    basename = base + conll_str
    
    # add directory with files to the input folder
    complete_name = os.path.join(directory, basename)
    
    with open(complete_name, 'w', encoding='utf-8') as conll_file:
        # Process each JSON object in the JSONL file
        for json_obj in loaded_dicts:
            for key, value in json_obj.items():
                contents = value.get('contents', '')
                tag = value.get('tag', '')

                # Split contents into tokens
                tokens = contents.split()
                
                # Write each token and tag on a separate line
                for token in tokens:
                    conll_file.write(f'{token}\t{tag}\n')
        
def main():
    
    input_folder = sys.argv[1] 
    
    txt_path = get_paths(input_folder)
    for text in txt_path:
        print(text)
        loaded_dicts = load_text(text)
        process_and_write(loaded_dicts, input_folder, text)

if __name__ == "__main__":
    main()