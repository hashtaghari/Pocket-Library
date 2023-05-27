import requests

def get_books_by_author(author_name):
    books = []
    start_index = 0
    while True:
        url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author_name}&maxResults=40&startIndex={start_index}'
        response = requests.get(url)
        data = response.json()
        if 'items' not in data:
            break
        for item in data['items']:
            book_title = item['volumeInfo']['title']
            authors = item['volumeInfo'].get('authors', [])
            publisher = item['volumeInfo'].get('publisher', '')
            published_date = item['volumeInfo'].get('publishedDate', '')
            isbn = ''
            if 'industryIdentifiers' in item['volumeInfo']:
                for identifier in item['volumeInfo']['industryIdentifiers']:
                    if identifier['type'] == 'ISBN_13':
                        isbn = identifier['identifier']
                        break
                    elif identifier['type'] == 'ISBN_10':
                        isbn = identifier['identifier']
                        break
            books.append((book_title, authors, publisher, published_date, isbn))
        start_index += 40
    return books



def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as file, open('List.txt', 'w', encoding='utf-8') as outfile:
        for line in file:
            author_name = line.strip()
            books = get_books_by_author(author_name)
            outfile.write(f'\nBooks by {author_name}:\n')
            for book in books:
                title, authors, publisher, published_date, isbn = book
                author_str = ', '.join(authors)
                if isbn:
                    outfile.write(f'{title};{author_str};{publisher};{published_date};{isbn};\n')
                else:
                    outfile.write(f'{title};{author_str};{publisher};{published_date};;\n')

def author(author_name):
    with open('List.txt', 'w', encoding='utf-8') as outfile:
        books = get_books_by_author(author_name)
        outfile.write(f'\nBooks by {author_name}:\n')
        for book in books:
            title, authors, publisher, published_date, isbn = book
            author_str = ', '.join(authors)
            if isbn:
                outfile.write(f'{title};{author_str};{publisher};{published_date};{isbn};\n')
            else:
                outfile.write(f'{title};{author_str};{publisher};{published_date};;\n')

def main():
    while True:
        choice = input("(1) Read from File\n(2) Enter Author Name \n(3) Exit \nYour Choice: ")
        if choice == '1':
            filename = input("Enter filename containing list of Authors: ")
            readfile(filename)
            print("Done! \nCheck List.txt\n")
        elif choice == '2':
            author_name = input("Enter Author Name: ")
            author(author_name)
            print("Done! \nCheckout List.txt\n")
        elif choice == '3':
            print("Exiting...\n")
            break
        else:
            print("Invalid Choice.\n")


if __name__ == "__main__":
    main()