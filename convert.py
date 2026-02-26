import xml.etree.ElementTree as ET

# wczytaj XML
tree = ET.parse("XML1.xml")
root = tree.getroot()

for produkt in root.findall(".//produkt"):

    k1 = produkt.find("koszt_1")
    k2 = produkt.find("koszt_2")
    k3 = produkt.find("koszt_3")
    k4 = produkt.find("koszt_4")

    if k1 is not None:
        koszty = ET.Element("koszty_transportu")

        def add_koszt(value, platnosc):
            el = ET.SubElement(koszty, "koszt")
            el.set("wysylka", "Kurier")
            el.set("platnosc", platnosc)
            el.set("koszt-kolejna-sztuka", "0")
            el.set("ilosc-w-paczce", "1")
            el.text = value

        add_koszt(k1.text, "przelew")
        add_koszt(k2.text, "pobranie")
        add_koszt(k3.text, "e-platnosc")
        add_koszt(k4.text, "raty")

        produkt.append(koszty)

        produkt.remove(k1)
        produkt.remove(k2)
        produkt.remove(k3)
        produkt.remove(k4)

tree.write("feed_poprawiony.xml", encoding="UTF-8", xml_declaration=True)

print("Gotowe ✅ feed_poprawiony.xml utworzony")

import requests
import base64

GITHUB_TOKEN = "TU_WKLEJ_TOKEN"
REPO = "TWOJLOGIN/xml-feed"
FILE_PATH = "feed.xml"

with open("feed_poprawiony.xml", "rb") as f:
    content = base64.b64encode(f.read()).decode()

url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

data = {
    "message": "update xml feed",
    "content": content
}

requests.put(url, json=data, headers=headers)

print("✅ Upload na GitHub gotowy!")
print(f"https://rawcdn.githack.com/{REPO}/main/{FILE_PATH}")