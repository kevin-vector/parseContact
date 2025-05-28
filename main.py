import csv
import re
from pathlib import Path

def parse_contact_info(contact_text):
    # Initialize dictionary for contact info
    contact_info = {
        'Name': '',
        'LinkedIn': '',
        'Website': '',
        'Phone': '',
        'Address': '',
        'Email': '',
        'Connected': ''
    }
    
    # Split text into lines
    lines = contact_text.strip().split('\n')
    
    # Current field being processed
    current_field = None
    
    # Regular expressions for common patterns
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    phone_pattern = r'\+?\d[\d\s-]+(?:\(Mobile\))?'
    url_pattern = r'(?:https?://)?[\w\.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!$&\'()*+,;=]+'
    date_pattern = r'\d{2}-[A-Za-z]{3}-\d{2}'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for field headers
        if line.lower() == 'contact info':
            continue
        elif 'profile' in line.lower():
            current_field = 'Name'
            # Extract name from "Name's Profile"
            contact_info['Name'] = line.split("’")[0].strip()
        elif 'linkedin' in line.lower():
            contact_info['LinkedIn'] = line
        elif line.lower() == 'website':
            current_field = 'Website'
        elif line.lower() == 'phone':
            current_field = 'Phone'
        elif line.lower() == 'address':
            current_field = 'Address'
        elif line.lower() == 'email':
            current_field = 'Email'
        elif line.lower() == 'connected':
            current_field = 'Connected'
        elif line.lower() == 'birthday':
            current_field = 'Birthday'
        else:
            # Handle data based on current field
            if current_field and line:
                if current_field == 'Website':# and ('http' in line or 'Portfolio' in line):
                    contact_info['Website'] = line.split(' (')[0].strip()
                elif current_field == 'Phone':# and re.match(phone_pattern, line):
                    contact_info['Phone'] = line.split(' (')[0].strip()
                elif current_field == 'Address':
                    contact_info['Address'] = line
                elif current_field == 'Email':# and re.match(email_pattern, line):
                    contact_info['Email'] = line
                elif current_field == 'Connected':# and re.match(date_pattern, line):
                    contact_info['Connected'] = line
                elif current_field == 'Birthday':# and re.match(date_pattern, line):
                    contact_info['Birthday'] = line
                current_field = None
    
    return contact_info

def save_to_csv(contact_info, output_file='contacts.csv'):
    # Define CSV headers
    headers = ['Name', 'LinkedIn', 'Website', 'Phone', 'Address', 'Email', 'Connected', 'Birthday']
    
    # Check if file exists to determine if we need to write headers
    file_exists = Path(output_file).exists()
    
    # Write to CSV
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write contact info
        writer.writerow(contact_info)

def main():
    while True:
        print("\nEnter contact information (or 'quit' to exit):")
        contact_text = ""
        while True:
            line = input()
            if line.strip().lower() == 'quit':
                return
            if line.strip() == "":
                break
            contact_text += line + "\n"
        
        if contact_text.strip():
            # Parse contact info
            contact_info = parse_contact_info(contact_text)
            
            # Save to CSV
            save_to_csv(contact_info)
            print(f"Contact information saved to contacts.csv")
        else:
            print("No contact information entered.")

if __name__ == "__main__":
    main()