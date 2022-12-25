from http import client
from minio import Minio
import pandas as pd
#terhubung keserver minio
minioClient = Minio('127.0.0.1:9000',
                access_key='minioadmin',
                secret_key='minioadmin',
                secure=False)
#menampilkan objeck atau data yang ada pada bucket minio
objects = minioClient.list_objects("bucket-bigdata")
for obj in objects:
    print(obj)
#mengambil object yang ada di minio
response = minioClient.get_object("bucket-bigdata", "balance-of-payments.csv")
#mengkonversi object dataset ke pandas dataframe
data = pd.DataFrame(pd.read_csv(response))
#menghubungkan ke server mongodb
clientMongo = pymongo.MongoClient("mongodb://localhost:27017")
#menginisialisasi nama database dan collection
db = clientMongo["dbBigData"]
col = db["colBigData"]
#menyimpan dataframe ke mongodb
data = data.to_dict(orient="records")
col.insert_many(data)
if col.inserted_ids is not None:
    print("Object disimpan di mongoDB !")
else:
    ("Object gagal disimpan di mongoDB !")
