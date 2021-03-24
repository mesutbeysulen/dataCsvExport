import csv
import json
import requests

# yorumlar servis urli
urlHb = "https://reviewsapiprod.herokuapp.com/api/v1/androidreviewlist?limit=150&sorting=newest&packageName="
urlAppPag = "&nextPaginationToken="

# hepsiburada - trendyol - n11 - gittigidiyor
# appIds = ['com.pozitron.hepsiburada', 'trendyol.com', 'com.dmall.mfandroid', 'com.gittigidiyormobil']
appIds = ['com.akinon.kapida']

# servisden dönen datalar için liste
all_data = []

# filename
filename = "android_reviews.csv"

# field names
fields = ['id', 'userName', 'userImage', 'date', 'score', 'scoreText', 'url', 'title', 'text', 'replyDate', 'replyText',
          'version', 'thumbsUp', 'criterias', 'appName']

# kaç defa 150 adet yorum alınmasını belirler
dataCount = 100

pagination = ''

# writing to csv file
with open(filename, 'w') as csvfile:
    for i in range(len(appIds)):

        if pagination == '':

            pagination = 'default'
            appName = appIds[i]
            endUrl = urlHb + appName + urlAppPag + pagination
            dataset = requests.get(url=endUrl)
            data = json.loads(dataset.text)
            all_data.extend(data['data'])

            pagination = data['nextPaginationToken']
            # print(pagination)

            for count in range(dataCount):
                if(pagination != None):
                    dataset = requests.get(url=urlHb + appIds[i] + urlAppPag + pagination)
                    data = json.loads(dataset.text)
                    all_data.extend(data['data'])

                    pagination = data['nextPaginationToken']
                    # print(pagination)
                    # creating a csv dict writer object
                    writer = csv.DictWriter(csvfile, fieldnames=fields)

                    # writing headers (field names)
                    writer.writeheader()

                    for next in range(len(all_data)):
                        all_data[next]['appName'] = appName
                    # writing the data rows
                    writer.writerows(all_data)
                    all_data = []

                    print("{}. {} datası aktarıldı".format(count + 1, appName))

            pagination = ''
            print("---------------  Toplam {} x 150 data aktarıldı!  ---------------".format(dataCount))
            count = count + 1
        else:
            print("Bot hata aldı!")
