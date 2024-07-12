import requests, json

original = 'quotes.json'

def save(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def update(filename):
    data_list = read(filename)
    for idx in range(len(data_list)):
        data = data_list[idx]
        data['tag'] = '성공'
    save(data_list, 'change.json')
    data_list = None

# print(read(original))
# update(original)

register_url = "http://127.0.0.1:8000/quote/quotes/"

def regiester(filename, url):
    data = read(filename)
    for quote in data:
        content = quote['content']
        quote['registrant'] = '668e3ada749ae974677235f7'
        response = requests.post(url, data=quote)
        if response.status_code == 201:
            print(f"전송 성공: {content}")
        else:
            print("전송 실패:", content, response.status_code, response.text)

regiester('change.json', register_url)