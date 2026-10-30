import requests
from bs4 import BeautifulSoup
import schedule
import time
import csv
import smtplib
from email.mime.text import MIMEText 

# ------------------------------- 
# STEP 1: SCRAPE DATA FROM WEBSITE 
# ------------------------------- 
def scrape_books(): 
    print("Scraping data...") 
  
    url = "https://books.toscrape.com" 
    response = requests.get(url) 
  
    soup = BeautifulSoup(response.text, "html.parser") 
  
    books = [] 
  
    # Loop through each book 
    for article in soup.find_all("article", class_="product_pod"): 
        title = article.h3.a["title"] 
        price = article.find("p", class_="price_color").text 
  
        books.append({ 
            "title": title, 
            "price": price 
        }) 
  
 
    print(f"Scraped {len(books)} books") 
    return books
def save_to_csv(books):
    with open("books.csv","w",newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price"])
        writer.writeheader() 
        writer.writerows(books)
        print("Books details added")
def send_email(books):
    sender="fatimatabassum743@gmail.com"
    reciever="ft3286215@gmail.com"
    app_password="vgaf nzyj nnfo tzvk"
    
    message = "All Books for Today:\n\n" 
    for book in books: 
        message += f"{book['title']} - {book['price']}\n" 
    msg = MIMEText(message) 
    msg["Subject"] = "Daily Book Report" 
    msg["From"] = sender 
    msg["To"] = reciever 
  
    # Send email 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server: 
        server.login(sender, app_password) 
        server.send_message(msg) 
  
    print("Email sent successfully!")
def job():
    books=scrape_books()
    save_to_csv(books)
    send_email(books)
schedule.every().days.at("21:15").do(job)  

while True:
    schedule.run_pending()
