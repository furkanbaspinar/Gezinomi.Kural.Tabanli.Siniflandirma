## GEZİNOMİ
# - Soru1 : miuul_gezinomi.xlsx dosyasını okutalım ve veri seti ile ilgili genel bilgileri göstermiş olalım.
import pandas as pd
pd.set_option("display.float_format", lambda x: '%2.f' % x)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
df = pd.read_excel(r"C:\Users\furka\Desktop\miuul_gezinomi.xlsx")
df.head()
df.info
df.shape

# - Soru 2: Kaçunique şehir vardır? Frekansları nedir?
df["SaleCityName"].nunique()
df["SaleCityName"].value_counts()

# - Soru 3: Kaç unique Concept vardır?
df["ConceptName"].unique()

# - Soru 4: Hangi Concept’den kaçar tane satış gerçekleşmiş?
df["ConceptName"].value_counts()

# - Soru 5:  Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})

# - Soru 6:  Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price": "sum"})

# - Soru 7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})

# - Soru 8: Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName").agg({"Price": "mean"})

# Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?
df.groupby(by=["SaleCityName", "ConceptName"]).agg({"Price": "mean"})

################################################################################
# Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çevirdik.
# • SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
# • Aralıkları ikna edici şekilde oluşturduk.
# Örneğin: ‘0_7’, ‘7_30', ‘30_90', ‘90_max’ aralıklarını kullandık.
# • Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullandık.

bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]

df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)
df.head(50)

# Görev 3: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
# Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden
# inceleyiniz?
df.groupby(["SaleCityName", "ConceptName", "EB_Score"]).agg({"Price": ["mean", "count"]})

# Şehir-Concept-Sezon
df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})

# Şehir - Concept - CInDay
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})

# Görev 4: City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.

# Elde ettiğiniz çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)
agg_df.head()

# Görev 5: Indekste yer alan isimleri değişken ismine çeviriniz.
# • Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çevirelim
agg_df.reset_index(inplace=True)
agg_df.head() # çıktımızı daha temiz almış olduk.

# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
# • Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
# • Yeni eklenecek değişkenin adı: sales_level_based
# • Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_based değişkenini oluşturmanız gerekmektedir.

agg_df["sales_level_based"] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: "_".join(x).upper(), axis=1)
agg_df.head()

# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
# • Yeni personaları PRICE’a göre 4 segmente ayırınız.
# • Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# • Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head()
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})

# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
# • Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
# • Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?

agg_df.sort_values(by="Price").head()
new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]

new_user1 = "GIRNE_YARIM PANSIYON_HIGH"
agg_df[agg_df["sales_level_based"] == new_user1]