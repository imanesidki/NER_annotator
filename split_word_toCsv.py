import os
import csv
import openai # ==0.28.0

# Set your OpenAI API key
openai.api_key = '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'

# Define the folder containing the invoice text files
txt_invoices_path = os.path.join(os.getcwd(), "text_invoices")

# Define the output CSV file
output_csv = 'invoice_words.csv'

# Define the folder to move the processed text files
labelised_text_files_path = os.path.join(os.getcwd(), "labelised_text_files")

# Create the folder if it doesn't exist
if not os.path.exists(labelised_text_files_path):
    os.makedirs(labelised_text_files_path)

# Initialize the index
index = 1

# Define the function to labelize the text using OpenAI API
def labelize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI that labels text with BIO NER tags. "
                    "Tags: O, B-NAME, I-NAME, B-EMAIL, I-EMAIL, B-ADDR, I-ADDR, "
                    "B-INV_DATE, I-INV_DATE, B-DUE_DATE, I-DUE_DATE, B-TOTAL_AMT, "
                    "I-TOTAL_AMT, B-ITEM_NAME, I-ITEM_NAME, B-UNIT_PRICE, I-UNIT_PRICE, "
                    "B-QUANTITY, I-QUANTITY, B-AMT, I-AMT, B-TAX, I-TAX, B-DISCOUNT, I-DISCOUNT. "
                    "The name is the invoice receiver name only and it can contain dots, underscores, or dashes besides letters, but cannot contain numbers. (e.g.: 'C BIS.COM' is a valid name). "
                    "Dates should contain numbers separated by dashes or slashes. ICE is a long number always preceded by 'ICE :'. "
                    "The text should be tokenized into words. each line should contain the word and its label only."
                )
            },
            {
                "role": "user",
                "content": f"Labelize the following text with BIO NER tags: {text}"
            }
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    content = response.choices[0].message['content'].strip()
    # Remove ```plaintext and ``` markers if present
    if content.startswith("```plaintext") and content.endswith("```"):
        content = content[len("```plaintext"): -len("```")].strip()
    return content

# Open the CSV file for writing
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['index', 'word', 'label'])
    
    # Loop over each file in the folder
    for filename in os.listdir(txt_invoices_path):
        if filename.endswith('.txt'):  # Process only text files
            file_path = os.path.join(txt_invoices_path, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                labeled_text = labelize_text(text)
                labeled_words = labeled_text.split('\n')
                for labeled_word in labeled_words:
                    if labeled_word:
                        parts = labeled_word.rsplit(' ', 1)
                        if len(parts) == 2:
                            word, label = parts
                            # Write each word with the current index and label
                            csvwriter.writerow([index, word, label])
            
            # Move the processed text file to the "labelised_text_files" folder
            new_file_path = os.path.join(labelised_text_files_path, filename)
            os.rename(file_path, new_file_path)
            
            # Increment the index for the next invoice text
            print(f"Processed {filename}, moved to {labelised_text_files_path} with index {index}.")
            index += 1


print(f"Words from invoice text files have been written to {output_csv}.")


# Test the function with a sample text
# file_path = os.path.join(os.getcwd(), 'text_invoices', '0b4cad85-4aac-47da-9077-e26e9080734d.txt')
# with open(file_path, 'r') as file:
#     text = file.read()
# print(labelize_text(text))