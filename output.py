import os,sys
m,t='webcam recognize',''
c=[a[4:]for a in os.popen('cd {};tree'.format(os.path.join(sys.path[0],m).replace(' ','\ '))).read().split('\n')[:-2][1:]]
for d in range(len(c)):
    if(c[d][-5:]=='.dict'):
        f=open('%s/%s'%(m,c[d]),'rb')
        i=eval(f.read())
        f.close()
        for j in range(i['paragraphs_result_num']):
            if(len(i['paragraphs_result'][j]['words_result_idx'])==1):
                if(i['words_result'][i['paragraphs_result'][j]['words_result_idx'][0]]['probability']['min']<=0.4):continue
            t='%s    '%t
            for j2 in i['paragraphs_result'][j]['words_result_idx']:
                if(i['words_result'][j2]['probability']['min']>0.4):t='%s%s'%(t,i['words_result'][j2]['words'])
            if(j<i['paragraphs_result_num']):t='%s\n'%t
        if(d<len(c)):t='%s\n==========第%d页==========\n'%(t,d+1)
        else:t='%s\n==========第%d页=========='%(t,d+1)
        print('第%d页'%(d+1))
f=open('SE.txt','w+');f.write(t);f.close()
