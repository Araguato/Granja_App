import os

def clean_null_bytes(directory):
    print(f"Cleaning null bytes in {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        if b'\x00' in content:
                            # Remove null bytes
                            clean_content = content.replace(b'\x00', b'')
                            
                            # Write cleaned content
                            with open(filepath, 'wb') as outfile:
                                outfile.write(clean_content)
                            
                            print(f"Cleaned null bytes from: {filepath}")
                except Exception as e:
                    print(f"Error cleaning {filepath}: {e}")

if __name__ == "__main__":
    clean_null_bytes('.')
