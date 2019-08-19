from bs4 import BeautifulSoup
import requests

def scrape_data():
    ptr = open('data.csv','w+')
    ptr.write("Product" + "," + "Cpu" + "," + "Memory" + "," + "Gpu" + "," + "OpSys" + "ScreenResolution" + "," + "Inches" + "," + "Price_euros")  

    urls = []
    url = "https://www.flipkart.com/hp-15q-core-i3-7th-gen-4-gb-1-tb-hdd-windows-10-home-15q-ds0007tu-laptop/p/itmf8ccgtvzuphgf?pid=COMF8CCGGPVNYQJT&srno=s_1_1&otracker=search&otracker1=search&lid=LSTCOMF8CCGGPVNYQJTZ07GDI&fm=SEARCH&iid=3e85cf45-93d0-4a56-be64-491c59a3a71a.COMF8CCGGPVNYQJT.SEARCH&ppt=sp&ppn=sp&ssid=g1vj90kecw0000001566218303031&qH=b71fcf18630c6f16"
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        spec = soup.find_all('div', attrs={'class':'_2RngUh'})

        spec_test = []
        for item in spec:
            spec_test += [item.text + '\n']

        model_no = spec_test[0].split("Model Number")[1].split("Part Number")[0]

        cpu = spec_test[1].split("Processor Brand")[1].split("Processor Name")[0]
        cpu += " " + spec_test[1].split("Processor Name")[1].split("Processor Generation")[0]
        cpu += " " + spec_test[1].split("Processor Generation")[1].split("SSD")[0]

        ram = spec_test[1].split("RAM")[1].split("RAM Type")[0]

        memory = spec_test[1].split("HDD Capacity")[1].split("Processor Variant")[0]

        gpu = spec_test[1].split("Graphic Processor")[1].split("Number of Cores")[0]

        op_sys = spec_test[2].split("Operating System")[1].split("System Architecture")[0]

        screen = spec_test[4].split("Screen Resolution")[1].split("Screen Type")[0]
        inches = spec_test[4].split("Screen Size")[1].split("Screen Resolution")[0]

        price = soup.find('div', attrs={'class':'_1vC4OE _3qQ9m1'}).text[1::]

        ptr.write(model_no+","+cpu+","+ram+","+memory+","+gpu+","+op_sys+","+screen+","+inches+","+price)

    ptr.close()
    
