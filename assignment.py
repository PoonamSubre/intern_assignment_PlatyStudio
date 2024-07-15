# Step 1: Define a list of words
words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]  # Extend this list as needed

# Step 2: Generate the word-to-index mapping dynamically
word_to_number = {word: index for index, word in enumerate(words)}

# Now, use this mapping in the script
def process_ass_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extracting events and unique lines without formatting
    unique_lines = {}
    events = []
    
    # First pass: Collect unique lines
    for line in lines:
        if line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            text = parts[-1].strip()
            clean_text = text.replace('{\\rH}', '').replace('{\\r}', '')
            if clean_text not in unique_lines:
                unique_lines[clean_text] = len(unique_lines) + 1
    
    # Sorting the unique lines by the order they appeared in
    sorted_unique_lines = sorted(unique_lines.items(), key=lambda x: x[1])
    unique_lines_dict = {id: line for line, id in sorted_unique_lines}
    
    # Second pass: Process each line
    for line in lines:
        if line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            text = parts[-1].strip()
            
            prefix = line[:line.find('0,,') + 3]
            
            # Determine which unique line to add
            unique_line = "..."
            for word, index in word_to_number.items():
                if word in text:
                    unique_line = unique_lines_dict.get(index, "...")
                    break
            
            unique_line1 = "..."
            for word, index in word_to_number.items():
                if word in text:
                    unique_line1 = unique_lines_dict.get(index + 2, "...")
                    break

            # Add the unique line, prefix, and original line
            events.append(f'{prefix}{unique_line}\n')
            events.append(line)
            events.append(f'{prefix}{unique_line1}\n\n')

        else:
            events.append(line)

    # Constructing the output ASS content
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(events)


# Specify the input and output file paths
input_ass_file = 'input_subtitles.ass'
output_ass_file = 'output.ass'

# Process the ASS file
process_ass_file(input_ass_file, output_ass_file) 