INDEX_FILE = "build/site/index.html"

def main():
    # Delete the noindex meta tag
    with open(INDEX_FILE, 'r') as f:
        processed_content = []
        for line in f:
            if not "noindex" in line:
                processed_content.append(line)

    with open(INDEX_FILE, 'w') as f:
        f.writelines(processed_content)

if __name__ == '__main__':
    main()