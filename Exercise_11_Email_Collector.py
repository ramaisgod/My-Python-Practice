# Python Exercise 11: Regex Email Extractor 
# text should be in txt file

import re

try:
    def email_extractor(file):
        output_file = open("Emails_Extracted_from_" + file, "a")
        email_count = 0
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                pattern = re.compile(r'([a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z]+)')
                matches = pattern.finditer(line)
                for match in matches:    
                    email_count += 1
                    output_file.write("Email_"+ str(email_count) + ": " + match.group() + "\n")
        output_file.close()
        print(email_count, "emails found !!!")

except Exception as e:
    print("Invalid contents in file. Please check text file.")


if __name__ == "__main__":
    email_extractor("ram.txt")







