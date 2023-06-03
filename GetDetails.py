import requests
import pandas as pd
import os

def convert_to_excel(filename='List.txt'):
  
    books = []
    i=0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('|')
            book = {
                'Title': fields[0],
                'Author': fields[1],
                'Publisher': fields[2],
                'Date of Publication': fields[3],
                'ISBN number': fields[4]
            }
            books.append(book)

    df = pd.DataFrame(books)
    df.to_excel('List.xlsx', index=False)
    #delete the txt file
    os.remove(filename)


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
            # book_title = item['volumeInfo']['title']
            book_title = item['volumeInfo'].get('title','INVALID')
            authors = item['volumeInfo'].get('authors', [])
            publisher = item['volumeInfo'].get('publisher', '')
            pd = item['volumeInfo'].get('publishedDate', '')
            published_date = pd[:4] if len(pd) > 4 else pd
            isbn = ''
            lang = item['volumeInfo'].get('language', '')
            if 'industryIdentifiers' in item['volumeInfo']:
                for identifier in item['volumeInfo']['industryIdentifiers']:
                    if identifier['type'] == 'ISBN_13':
                        isbn = identifier['identifier']
                        break
                    elif identifier['type'] == 'ISBN_10':
                        isbn = identifier['identifier']
                        break
            #check if one of the authors is the author we are looking for, in terms of matching string (not case sensitive)
            for a in authors:
                #check if author_name is contained in string a by string matching
                if author_name.lower() in a.lower():
                    # if book_title!='INVALID' and lang=='en':
                    if book_title!='INVALID':
                        books.append((book_title, authors, publisher, published_date, isbn))
                        break
        start_index += 40
    return books



def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as file, open('List.txt', 'w', encoding='utf-8') as outfile:
        for line in file:
            author_name = line.strip()
            books = get_books_by_author(author_name)
            # outfile.write(f'\nBooks by {author_name}:\n')
            for book in books:
                title, authors, publisher, published_date, isbn = book
                author_str = ', '.join(authors)
                if isbn:
                    outfile.write(f'{title} |{author_str} |{publisher} |{published_date} |{isbn}|\n')
                else:
                    outfile.write(f'{title} |{author_str} |{publisher} |{published_date} | |\n')

def author(author_name):
    with open('List.txt', 'w', encoding='utf-8') as outfile:
        books = get_books_by_author(author_name)
        # outfile.write(f'\nBooks by {author_name}:\n')
        for book in books:
            title, authors, publisher, published_date, isbn = book
            author_str = ', '.join(authors)
            if isbn:
                outfile.write(f'{title} |{author_str} |{publisher} |{published_date} |{isbn}|\n')
            else:
                outfile.write(f'{title} |{author_str} |{publisher} |{published_date} | |\n')


def remove_dupes(filename = 'List.xlsx'):
    df = pd.read_excel('List.xlsx')
    df.drop_duplicates(subset=['Title'], inplace=True)
    # df.to_excel(filename, index=False)
    #remove rows with empty title
    df = df[df['Title'].notna()]
    df.to_excel(filename, index=False)



def main():
    while True:
        choice = input("(1) Read from File\n(2) Enter Author Name \n(3) Exit \nYour Choice: ")
        if choice == '1':
            filename = input("Enter filename containing list of Authors: ")
            readfile(filename)
            convert_to_excel()
            abc = 'List.xlsx'
            remove_dupes(abc)
            print("Done! \nCheck List.xlsx\n")
        elif choice == '2':
            author_name = input("Enter Author Name: ")
            author(author_name)
            convert_to_excel()
            abc = 'List.xlsx'
            remove_dupes(abc)
            print("Done! \nCheckout List.xlsx\n")
        elif choice == '3':
            print("Exiting...\n")
            break
        else:
            print("Invalid Choice.\n")


if __name__ == "__main__":
    main()