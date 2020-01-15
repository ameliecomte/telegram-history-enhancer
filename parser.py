from bs4 import BeautifulSoup
import glob
from datetime import datetime

cssdelimiter = """
.delimiter {
    color: red;
    padding: 20;
    background-color: #fa6f9281;
    border-radius: 10px;
}
"""

indexhtml = """"
    <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Exported Data</title>
            <meta content="width=device-width, initial-scale=1.0" name="viewport" />
            <link href="css/style.css" rel="stylesheet" />
            <script src="js/script.js" type="text/javascript"></script>
        </head>

        <body onload="CheckLocation();">
            <div class="page_wrap">
                <div class="page_body chat_page">
                    <div class="history"></div>
                </div>
            </div>
        </div>    
"""

def addCSS():
    with open('css/style.css', 'a+') as css:
        if '.delimiter' in css.read():
            css.write(cssdelimiter)

def parseMesssages(index):
    soup = BeautifulSoup(open("messages"+ str(index) +".html", encoding="utf8"), "html.parser")
    history = soup.find('div', {'class': 'history'}).find_all('div', recursive=False)

    # soup.select(".text") # get the text. sleep, goodbye, good night, see you, tomorrow, hi, hey, hello

    #div = soup.new_tag("div")
    
    if history != None:
        new_soup = BeautifulSoup(indexhtml, features="html.parser")
        new_history = new_soup.find('div', {'class': 'history'})

        date_format = "%d.%m.%Y %H:%M:%S"
        dt = datetime.strptime("20.10.2000 00:00:00", date_format) # 27.04.2018 17:49:59

        for child in history:
            text_tag = child.find(attrs={'class':"text"})
            date_tag = child.find(attrs={'class':"date"})

            if date_tag != None:
                date = datetime.strptime(date_tag['title'], date_format)
                
                diff = date - dt
                #cut = str(diff)[0]
                hours = (diff.days * 24) + diff.seconds / (60*60)
                if hours > 1:
                    d = soup.new_tag("div", attrs={ 'class': 'delimiter' })
                    
                    d.string = "###############" + " conversation paused for " + "%.1f" % hours + ' hours'
                    new_history.append(d)         
                dt = date
            new_history.append(child)

        with open('index.html', 'a+', encoding="utf8") as output:
            output.write(new_soup.prettify()) 



def main():
    addCSS()
    htmls_pages = glob.glob("messages*.html")
    for page in range(len(htmls_pages)):
        index = page + 1        
        if page == 0:
            parseMesssages('')
        #else:
            #parseMesssages(index)

main()
