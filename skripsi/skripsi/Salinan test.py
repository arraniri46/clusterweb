import pandas as pd
import json
from pandas import DataFrame
import collections
import numpy as np

'''df = pd.read_csv('Users/user/PycharmProjects/skripsi/SKDR/data/20132018.csv')'''


def data_kecil(filename):
    filename = 'static/upload_file/'+filename
    bulan = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[0,14])
    tahun = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[0,2,3,4,5,6,7,8,9,10,11,12,13,14])
    jan = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,3,4,5,6,7,8,9,10,11,12,13,14])
    feb = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,4,5,6,7,8,9,10,11,12,13,14])
    mar = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,5,6,7,8,9,10,11,12,13,14])
    apr = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,6,7,8,9,10,11,12,13,14])
    mei = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,7,8,9,10,11,12,13,14])
    jun = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,8,9,10,11,12,13,14])
    jul = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,7,9,10,11,12,13,14])
    agu = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,7,8,10,11,12,13,14])
    sep = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,7,8,9,11,12,13,14])
    okt = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,7,8,9,10,12,13,14])
    nov = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,7,8,9,10,11,13,14])
    des = pd.read_csv(filename, usecols=[1,2,3,4,5,6], skiprows=[1,2,3,4,5,6,7,8,9,10,11,12,14])
    t2013 = pd.read_csv(filename, usecols=[1], skiprows=[0,14])
    t2014 = pd.read_csv(filename, usecols=[2], skiprows=[0,14])
    t2015 = pd.read_csv(filename, usecols=[3], skiprows=[0,14])
    t2016 = pd.read_csv(filename, usecols=[4], skiprows=[0,14])
    t2017 = pd.read_csv(filename, usecols=[5], skiprows=[0,14])
    t2018 = pd.read_csv(filename, usecols=[6], skiprows=[0,14])
    df1 = pd.read_csv(filename, skiprows=[0], index_col=[0])

    #list_data_dasar = dasar.values.tolist()

    #df1 = dasar.apply(pd.to_numeric(list_data_dasar, downcast='float'))

    kumpulminbln = []
    kumpulminthn = []
    kumpulmaxbln = []
    kumpulmaxthn = []

    list_data_bulan = bulan.values.tolist()
    list_data_tahun = tahun.values.tolist()
    list_data_jan = jan.values.tolist()
    list_data_jan = [val for sublist in list_data_jan for val in sublist]
    kumpulminbln.append(min(list_data_jan))
    kumpulmaxbln.append(max(list_data_jan))
    list_data_feb = feb.values.tolist()
    list_data_feb = [val for sublist in list_data_feb for val in sublist]
    kumpulminbln.append(min(list_data_feb))
    kumpulmaxbln.append(max(list_data_feb))
    list_data_mar = mar.values.tolist()
    list_data_mar = [val for sublist in list_data_mar for val in sublist]
    kumpulminbln.append(min(list_data_mar))
    kumpulmaxbln.append(max(list_data_mar))
    list_data_apr = apr.values.tolist()
    list_data_apr = [val for sublist in list_data_apr for val in sublist]
    kumpulminbln.append(min(list_data_apr))
    kumpulmaxbln.append(max(list_data_apr))
    list_data_mei = mei.values.tolist()
    list_data_mei = [val for sublist in list_data_mei for val in sublist]
    kumpulminbln.append(min(list_data_mei))
    kumpulmaxbln.append(max(list_data_mei))
    list_data_jun = jun.values.tolist()
    list_data_jun = [val for sublist in list_data_jun for val in sublist]
    kumpulminbln.append(min(list_data_jun))
    kumpulmaxbln.append(max(list_data_jun))
    list_data_jul = jul.values.tolist()
    list_data_jul = [val for sublist in list_data_jul for val in sublist]
    kumpulminbln.append(min(list_data_jul))
    kumpulmaxbln.append(max(list_data_jul))
    list_data_agu = agu.values.tolist()
    list_data_agu = [val for sublist in list_data_agu for val in sublist]
    kumpulminbln.append(min(list_data_agu))
    kumpulmaxbln.append(max(list_data_agu))
    list_data_sep = sep.values.tolist()
    list_data_sep = [val for sublist in list_data_sep for val in sublist]
    kumpulminbln.append(min(list_data_sep))
    kumpulmaxbln.append(max(list_data_sep))
    list_data_okt = okt.values.tolist()
    list_data_okt = [val for sublist in list_data_okt for val in sublist]
    kumpulminbln.append(min(list_data_okt))
    kumpulmaxbln.append(max(list_data_okt))
    list_data_nov = nov.values.tolist()
    list_data_nov = [val for sublist in list_data_nov for val in sublist]
    kumpulminbln.append(min(list_data_nov))
    kumpulmaxbln.append(max(list_data_nov))
    list_data_des = des.values.tolist()
    list_data_des = [val for sublist in list_data_des for val in sublist]
    kumpulminbln.append(min(list_data_des))
    kumpulmaxbln.append(max(list_data_des))
    print(min(kumpulminbln))
    list_data_t2013 = t2013.values.tolist()
    list_data_t2013 = [val for sublist in list_data_t2013 for val in sublist]
    kumpulminthn.append(min(list_data_t2013))
    kumpulmaxthn.append(max(list_data_t2013))
    list_data_t2014 = t2014.values.tolist()
    list_data_t2014 = [val for sublist in list_data_t2014 for val in sublist]
    kumpulminthn.append(min(list_data_t2014))
    kumpulmaxthn.append(max(list_data_t2014))
    list_data_t2015 = t2015.values.tolist()
    list_data_t2015 = [val for sublist in list_data_t2015 for val in sublist]
    kumpulminthn.append(min(list_data_t2015))
    kumpulmaxthn.append(max(list_data_t2015))
    list_data_t2016= t2016.values.tolist()
    list_data_t2016 = [val for sublist in list_data_t2016 for val in sublist]
    kumpulminthn.append(min(list_data_t2016))
    kumpulmaxthn.append(max(list_data_t2016))
    list_data_t2017 = t2017.values.tolist()
    list_data_t2017 = [val for sublist in list_data_t2017 for val in sublist]
    kumpulminthn.append(min(list_data_t2017))
    kumpulmaxthn.append(max(list_data_t2017))
    list_data_t2018 = t2018.values.tolist()
    nilai_max = t2013.max()

    print(list_data_jan)

    '''
    list_minmax = []
    
    #2013
    min = min.t2013
    max = max.t2013
    list_minmax = list_minmax.append([min,max])
    
    #2014
    min = min.t2014
    max = max.t2014
    list_minmax = list_minmax.append([min,max])
    
    {[2,37], [11,25],}
    '''


    i = 0
    a = 0
    c = 0

    kolom_banding = len(df1.columns) - 1

    #perbandingan per bulan
    list_hasil_bulan_dasar = []
    while i<kolom_banding:
        j = 0
        while j<12:
            iterr = 0
            while iterr<12:

                ab = df1.iloc[j][i] - df1.iloc[iterr][i]

                if df1.iloc[j][i]>df1.iloc[iterr][i]:
                    '''print('bagus'+' ('+str(j)+','+str(i)+')'+' ('+str(i)+','+str(iterr)+') '+str(df1.iloc[j][i])+' '+str(df1.iloc[iterr][i])+' = ' +str(ab))'''
                    list_hasil_bulan_dasar.append(ab)
                elif df1.iloc[j][i]<df1.iloc[iterr][i]:
                    '''print('buruk'+' ('+str(j)+','+str(i)+')'+' ('+str(i)+','+str(iterr)+') '+str(df1.iloc[j][i])+' '+str(df1.iloc[iterr][i])+' = ' +str(ab))'''
                    list_hasil_bulan_dasar.append(ab)
                elif df1.iloc[j][i]==df1.iloc[iterr][i]:
                    '''print('sama'+' ('+str(j)+','+str(i)+')'+' ('+str(i)+','+str(iterr)+') '+str(df1.iloc[j][i])+' '+str(df1.iloc[iterr][i])+' = ' +str(ab))'''
                    list_hasil_bulan_dasar.append(ab)
                else:
                    print('dkjk')
                iterr = iterr+1
            j = j+1
        i=i+1
        list_hasil_bulan = list_hasil_bulan_dasar
        print(len(list_hasil_bulan))

    # perbandingan per tahun
    list_hasil_tahun_dasar = []

    while a<kolom_banding:
        iter = a+1
        while iter<kolom_banding:
            j=0
            while j<12:

                bc = df1.iloc[j][a] - df1.iloc[j][iter]

                if df1.iloc[j][a]<df1.iloc[j][iter]:
                    '''print('bagus'+' ('+str(j)+','+str(a)+')'+' ('+str(j)+','+str(iter)+') '+str(df1.iloc[j][a])+' '+str(df1.iloc[j][iter])+' = '+str(bc))'''
                    list_hasil_tahun_dasar.append((bc))
                elif df1.iloc[j][a]>df1.iloc[j][iter]:
                    '''print('buruk'+' ('+str(j)+','+str(a)+')'+' ('+str(j)+','+str(iter)+') '+str(df1.iloc[j][a])+' '+str(df1.iloc[j][iter])+' = '+str(bc))'''
                    list_hasil_tahun_dasar.append((bc))
                else:
                    '''print('sama'+' ('+str(j)+','+str(a)+')'+' ('+str(j)+','+str(iter)+') '+str(df1.iloc[j][a])+' '+str(df1.iloc[j][iter])+' = '+str(bc))'''
                    list_hasil_tahun_dasar.append((bc))
                j=j+1
            iter = iter+1
        a=a+1
        list_hasil_tahun = list_hasil_tahun_dasar
        """print(len(list_hasil_tahun))"""





    print('\nalalalallalalalal\n')
    print(list_hasil_tahun)
    print('\n---------------------\n')
    print(nilai_max)

    list_data_jan = json.dumps(list_data_jan)
    list_data_feb = json.dumps(list_data_feb)
    list_data_mar = json.dumps(list_data_mar)
    list_data_apr = json.dumps(list_data_apr)
    list_data_mei = json.dumps(list_data_mei)
    list_data_jun = json.dumps(list_data_jun)
    list_data_jul = json.dumps(list_data_jul)
    list_data_agu = json.dumps(list_data_agu)
    list_data_sep = json.dumps(list_data_sep)
    list_data_okt = json.dumps(list_data_okt)
    list_data_nov = json.dumps(list_data_nov)
    list_data_des = json.dumps(list_data_des)

    print(list_data_jan)
    print(kumpulminbln)
    print('-------')

    return list_hasil_tahun, list_hasil_bulan, list_data_bulan, list_data_tahun, list_data_jan, list_data_feb, list_data_mar, list_data_apr, list_data_mei, list_data_jun, list_data_jul, list_data_agu, list_data_sep, list_data_okt, list_data_nov, list_data_des, list_data_t2013, list_data_t2014, list_data_t2015, list_data_t2016, list_data_t2017, list_data_t2018, kumpulminthn, kumpulminbln, kumpulmaxbln, kumpulmaxthn




'''while i < 6:
    df1 = pd.read_csv('20132018.csv', skiprows=[0], index_col=[0])
    j=1
    while j<14:
        df2 = pd.read_csv('20132018.csv', usecols=[i])
        o = df2.iloc[j]
        old = pd.to_numeric(o, downcast='float')
        print(old)
        print("==========")
        df3 = pd.read_csv('20132018.csv', usecols=[i+1])
        n = df3.iloc[j]
        new = pd.to_numeric(n, downcast='float')
        print(new)
        j=j+1

    i=i+1'''






#while i < 6:
#	df1 = pd.read_csv('20132018.csv', usecols=[0,1,i], skiprows=[0], index_col=[0])
#	j=2
#	while j<15:
#		df2 = pd.read_csv('20132018.csv', usecols=[i])
#		o = df2.iloc[j]
#		old= pd.to_numeric(o, downcast='float')
#		df3 = pd.read_csv('20132018.csv', usecols=[i+1])
#		n = df3.iloc[j]
#		new= pd.to_numeric(n, downcast='float')
#       print(old)

