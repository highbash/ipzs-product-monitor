from bs4 import BeautifulSoup
import time
import requests
import discord

productUrl = "https://www.shop.ipzs.it/2021-5e-ag-eccellitaliane-trittnutella48-2ms10-21f010.html"
webhookUrl = "https://discord.com/api/webhooks/807761661489840178/QD4bGwzMFOcAG1t_O6p4-FTVC8yaLvQQcbAmhCGXZg_t1HaF2VHz0nStn686aV61JIrC"

PLACEHOLDER_FOR_IMAGE_URL = "https://www.shop.ipzs.it/media/catalog/product/cache/3340c06c5a318733a9d40568377189d8/2/0/2021_ri_5e_nutella_trittico_02.jpg"


def sendEmbed(productTitle, productStock, productImageUrl):
    data = {
        "embeds" : [
            {
                "description" : productStock,
                "title" : productTitle,
                "url" : productUrl,
                "image": {'url' : productImageUrl},
                "footer": {'text' : 'IPZS Monitor c\o @tommibrega - 2021'}
            }
        ]
    }
    wh_reply = requests.post(webhookUrl, json = data)
    try:
        wh_reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
    else:
        print("Webhook Sent!")    

def getProductData():
    productPage_reply = requests.get(productUrl)
    try:
        zuppa = BeautifulSoup(productPage_reply.text, 'html.parser')
        productTitle = zuppa.find('title').text.strip()
        productStock = zuppa('div', {'class':'product-info-stock-sku'})[0].getText().strip()
        productImageUrl = PLACEHOLDER_FOR_IMAGE_URL
        data = [productTitle, productStock, productImageUrl]
        return data
    except:
        print("[Error] -  Retrying in 10 seconds...")
        time.sleep(10)
        return False


while True:
    productData = getProductData()
    if productData == False:
        continue
    else:
        if productData[1] == 'Esaurito':
            print("[Out of Stock] -  Rechecking...")
            #sendEmbed(productData[0], productData[1], productData[2])
            time.sleep(0)
            continue
        else:
            print("[IN STOCK!] -  GOGOGO!!!")
            sendEmbed(productData[0], productData[1], productData[2])
            continue







