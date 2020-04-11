    
from nodeeditor.utils import *
from nodeeditor.say import *


import time,re
import FreeCAD,FreeCADGui
import ssl
import urllib.request

import requests
import sys

import numpy as np


import Part
    



# https://neo4j.com/docs/api/python-driver/current/#installation
from neo4j import GraphDatabase,unit_of_work


def createNode2(tx,kid,typ,params):
        cmd="CREATE (p:"+typ+" {$params})"
        return tx.run(  "CREATE (p:"+typ+")"
                        "SET p.a='NEU' "
                       "SET p = $params " 
                        "RETURN p",                    
                       
        kid=kid,typ=typ,params=params)

from PyFlow.Core.Common import *

import requests
import html2text.html2text


def testargs(a):
    sayl()
    say(a)
    sayW("DONE")
    return("RESULT")


def isStopped(self):
    sayl("stopped")
    say(self._stopped)
    return True



        
class WWW():
    


    def _GetAdminPost(self,args):
        
        self._stopped = False
        
        
        conffn="/home/thomas/config_forum.txt"
        config=open(args['conffn'],"r").read()
        [userid,password]=config.splitlines()

        atime=time.time()
        
        postips=[]
        userips=[]
        
        fpu=open(args["filenameUserIP"],"a")
        fpp=open(args["filenamePostIP"],"a")

        site_url = 'https://forum.freecadweb.org/ucp.php?mode=login'
        file_url="https://forum.freecadweb.org/mcp.php?i=main&mode=post_details&p="

        o_file='/home/thomas/forum_scan_ip/post_'

        s = requests.Session()
        s.get(site_url)

        # login to site.
        s.post(site_url, data={
            'username': userid, 
            'password': password,
            "login":"Login",
        })

        sayW("start download",self)
        FreeCAD.Gui.updateGui()

        for p in range(args['startingPost'],args['startingPost']+args['countPosts']):

            if self._stopped:
                sayErr("Abbruch")
                return

            first=0 
            alls=[]
            counts=[-1]
            uid=None   
            name=None
            say("---POST--------",p)
            FreeCAD.Gui.updateGui()      

            atime=time.time()
            r = s.get(file_url+str(p))

            html=r.content
            dat=str(r.content,'utf-8')

            dattt=html2text.html2text.html2text(dat)
            for line in dattt.splitlines():
                if line.startswith('|'):
                    #print (line)
                    counts += [line[1:-1]]
                if line.startswith('['):
                    m=re.match("\[(\d+.\d+.\d+.\d+)\]",line)
                    if m is not None:
                        #print(line)
                        if not first:
                            first=m.group(1)
                            fpp.write("{},{}\n".format(first,str(p)))
                            postips += [[first,str(p)]]
                        alls +=[m.group(1)]
                        #else:
                        fpu.write("{},{}\n".format(m.group(1),uid))
                        userips += [[m.group(1),uid,name]]

                m=re.match('.*Posted by \[(.*)\].*\&u=(\d+)\)',line)
                if m is not None:
                    uid=m.group(2)
                    name=m.group(1)
                    sayW(uid,name)

            sayW(p,"get time ",round(time.time()-atime,2),name,uid)
            say([(a,c) for a,c, in zip(alls,counts)])
            # Download file
            with open(o_file+str(p)+'.html', 'wb') as output:
                output.write(r.content)


        
        s.close()
        sayW("# Closed session once all work done")
        rc={
            'PostIP':postips,
            'UserIP':userips,
            }
            
        return rc


    def _GetPost(self,args):
        
        self._stopped = False

        atime=time.time()

        sayW("start download",self)
        FreeCAD.Gui.updateGui()

        def store(data):
            fn="/home/thomas/forum_scan_test/data_forum_v2.txt"
            fn="/home/thomas/forum_scan_test/data_forum_v3.txt"
            fn=args['filenameHeader']
            with open(fn, "a") as myfile:
                myfile.write(str(data)+'\n')

        url='http://forum.freecadweb.org/viewtopic.php?p={}'

        # postid_a=300000 # 20:32 gestarted ab hier mit lueche


        authors={}
        users=[]
        posts=[]
        threads=[]
        
        for postid in range(args['startingPost'],args['startingPost']+args['countPosts']):


                    if self._stopped:
                        sayErr("stopped")
                        return

                    posttimea=time.time()
                    say()
                    sayW("START POST ID",postid)
                    FreeCADGui.updateGui()

                    link = url.format(postid)

                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE

                    try:
                        with urllib.request.urlopen(link, context=ctx) as f:
                            info=str(f.read(),'utf-8')
                    except:
                        continue

                    posttimeb=time.time()

                    contenttext=''
                    postid=None

                    for i,l in enumerate(info.splitlines()):
                        m=re.match('.*\s*<p class="author',l)
                        if m:
                            m2=re.match(".*u=(\d+).*>(\S+)</a>.*span>(.+)</p>",l)
                            if m2:
                                print (postid, "author ",m2.group(1),m2.group(3),thread)
                                try:
                                    authors[m2.group(2)] += [[postid,m2.group(3),thread]]
                                except:
                                    authors[m2.group(2)] = [[postid,m2.group(3),thread]]

                                store(["A",postid,m2.group(1),m2.group(2),m2.group(3),forum,thread,title])
                                user=m2.group(1)
                                users +=[[m2.group(1),m2.group(2)]]
                                posts +=[[postid,thread,user]]
                                content=False
                            continue

                        m2=re.match('.*<div id="p(\d+)" class="post',l)
                        if m2 is not None:
                            if postid is not None:
                                outPath="/home/thomas/forum_scan/pp"+postid+".html"
                                with open(outPath, 'w+') as myWrite:
                                    myWrite.write(contenttext +"</body></html>")

                            contenttext="<html><body>"+l
                            postid=m2.group(1)
                            lastpostid=postid
                            
                            continue

                        m=re.match('.*\s*<h2 class="topic-title"><a href="./viewtopic.php',l)
                        if m:
                            m2=re.match('.*f=(\d+).*amp;t=(\d+).*">(.*)</a></h2>',l)
                            forum,thread,title=m2.group(1),m2.group(2),m2.group(3)
                            say ("forum,thread,title",forum,thread,title)
                            threads +=[[thread,forum,title]]
                            content=False
                            continue

                        #neuer post
                        m=re.match('.*\s*<div id="post_content',l)
                        if m:
                            content=True
                            post='<div id="post_content374217">'
                            m=re.match('.*div id="post_content(\d+)"',l)
                            continue

                        if l.startswith('           Post Reply      </a>') and i > 200:
                            print (i,"--",l)
                            content=False

                        contenttext += l+"\n"

                        m=re.match('.*back2top',l)
                        if m:
                            outPath=args["dirnamePosts"]+"/pp"+postid+".html"
                            with open(outPath, 'w+') as myWrite:
                                myWrite.write(contenttext)

                    posttimec=time.time()
                    say(postid,"web read time",round(posttimeb-posttimea,2),"proc time",round(posttimec-posttimeb,2))

        
        sayW("Results by author")
        FreeCAD.authors=authors
        for a in authors:
            say(a)
            for ex in authors[a]:
                print("    ",ex)

        sayW("Last Post",lastpostid)
        print ("run time",time.time()-atime,"read",args['countPosts'])
        rc={
            'users':users,
            'posts':posts,
            'threads':threads,
        }

        return rc


    def _UpdateGraphDB(self,args):
        
        self._stopped = False
        
        
        driver=self.getPinObject('driver')
        
        
        cmd="MATCH (u:FoUser) return u.uid as id"
        with driver.session() as session:
                    rc = session.run(cmd)
        users=[d['id']for d in rc.data()]
        
        cmd="MATCH (a:FoThread) return a.tid as id"
        with driver.session() as session:
                    rc = session.run(cmd)
        threads=[d['id']for d in rc.data()]
        
        cmd="MATCH (a:FoPost) return a.pid as id"
        with driver.session() as session:
                    rc = session.run(cmd)
        posts=[d['id']for d in rc.data()]
        
        #--------------------------------------------
        def chain_threads():

            from neo4j import GraphDatabase
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

            '''
            with driver.session() as session:
                #rc = session.run("match (t:FoThread) return t.tid as id")
                rc = session.run("match (t:FoThread)--(:FoImport) return t.tid as id")

            threads={d['id']:1 for d in rc.data()}
            threads=['35521']
            threads=['43025']
            '''




            for tid in threads:
                say(tid)
                FreeCADGui.updateGui()
                #continue


                cmd="match (a:FoPost)-[r:in]->(t:FoThread{tid:$thread}) return a.pid as pid order by toFloat(a.pid)"
                with driver.session() as session:
                    rc = session.run(cmd,thread=tid)

                data=rc.data()
                #say(data)
                pids=[d['pid'] for d in data]
                say(pids)
                if len(pids)==0:
                    continue
                    
                for i in range(len(pids)-1):
                    with driver.session() as session:
                        cmd="Match (pa:FoPost{pid:$a}),(pb:FoPost{pid:$b}) merge (pa)-[:to]->(pb)"
                        rc=session.run(cmd,a=pids[i],b=pids[i+1])

                with driver.session() as session:
                        cmd="Match (t:FoThread{tid:$thread}),(pa:FoPost{pid:$a}) merge (t)-[:posts]->(pa) return t,pa"
                        rc=session.run(cmd,thread=tid,a=pids[0])
                        #say(rc.data())
                #return

        # match (p:FoUser{name:'cada'}) return  p
        mode=self.getData('mode')
        if mode == "chainthreads":
            chain_threads()

        
            sayW("ANNBZRXCZT!")
            return
        
        #-----------------------------------------------------
        
        sayl("USERS")
        say(len(args['users']))
        for r in args['users']:
            
            if r[0] in users:
                #sayErr("User found",r)
                continue
                
            
            
            FreeCADGui.updateGui()
            if self._stopped:
                sayErr("stopped")
                return
                
            #say(r)
            cmd="MERGE (a:FoUser{uid:$data[0]}) SET a.name=$data[1] SET a.test=10 RETURN a"
            
            cmd='''
            merge (imp:TestImport{name:'I_05'})
            MERGE (a:FoUser{uid:$data[0]}) SET a.name=$data[1] SET a.test=10
            merge (a)<-[:import]-(imp)
            return a
            '''
            
            try:
                with driver.session() as session:
                    rc = session.run(cmd,data=r)
                    #say(rc.data())
            
            except Exception as e:
                sayErr(e)
                sayErr("Record:")
                sayErr(r)

        sayl("THREADS")
        say(len(args['threads']))
        FreeCADGui.updateGui()
        for r in args['threads']:
            
            if r[0] in threads:
                continue
            
            if self._stopped:
                sayErr("stopped")
                return

            say(r)
            FreeCADGui.updateGui()


            cmd='''
            merge (imp:TestImport{name:'I_05'})
            MERGE (a:FoThread{tid:$data[0],forum:$data[1],title:$data[2]}) 
            merge (a)<-[:import]-(imp)
            RETURN a
            '''
            
            try:
                with driver.session() as session:
                    rc = session.run(cmd,data=r)
                    #say(rc.data())
            
            except Exception as e:
                sayErr(e)
                sayErr("Record:")
                sayErr(r)
        #say(threads)
        
        sayl("POSTS")
        say(len(args['posts']))
        
        for r in args['posts']:
            
            
            if self._stopped:
                sayErr("stopped")
                return

            #if r[0] in posts:
            #    continue

            say(r)
            FreeCADGui.updateGui()


            cmd='''
            
            MATCH (u:FoUser{uid:$data[2]})
            MATCH (t:FoThread{tid:$data[1]})
            merge (imp:TestImport{name:'I_05'})
            MERGE (a:FoPost{pid:$data[0]}) 
            
            MERGE (a)<-[:by]-(u)
            MERGE (t)<-[:in]-(a)

            SET a.user=$data[2]
            SET t.test=9
            merge (a)<-[:import]-(imp)
            RETURN a,u
            '''
            
            try:
                with driver.session() as session:
                    rc = session.run(cmd,data=r)
                    #say(rc.data())
            
            except Exception as e:
                sayErr(e)
                sayErr("Record:")
                sayErr(r)



        say("DONE")
        rc={}
        return rc


    def _Command(self,args):
        
        self._stopped = False
        
        driver=self.getPinObject('driver')
        cmd=args['cypher']

        @unit_of_work(timeout=1.)
        def count_person(tx):
            return tx.run("MATCH (a)  RETURN a LIMIT 16000")#.single().value()


        say("start")
        at=time.time()
        try:
            with driver.session() as session:
                node_id = session.write_transaction(count_person)
            say("FERTI",node_id)
        except Exception as e:
            sayErr(e)

            
        say(time.time()-at)


        return


         
        @unit_of_work(timeout=1.0)
        def runit():
            with driver.session() as session:
                rc = session.run(cmd)
                rc = rc.data()
                return rc
        
            
        try:

            
                rc= runit()
                return rc
        
        except Exception as e:
            sayErr(e)
            sayErr("Record:")
            sayErr(cmd)

            return None



#----------------------------------------------------------------
# pyflow interface
#----------------------------------------------------------------
    def run_WWW_GetAdminPost(self):

        args={
            'conffn':"/home/thomas/config_forum.txt",
        }

        for p in ['startingPost', 'countPosts',"filenameUserIP","filenamePostIP"]:
            args[p]=self.getData(p)
        
        rc=eval("WWW._GetAdminPost(self,args)")
        
        say("rc",rc)
        for p in ['PostIP','UserIP']:
            self.setData(p,rc[p])



    def run_WWW_GetPost(self):
        

        args={
        }

        for p in ['startingPost', 'countPosts','filenameHeader','dirnamePosts']:
            args[p]=self.getData(p)
        
        rc=eval("WWW._GetPost(self,args)")
        
        #say("rc",rc)
        
        for p in ['users','posts','threads']:
            say(p,rc[p])
            self.setData(p,rc[p])


    def run_WWW_UpdateGraphDB(self):

        args={
        }

        #for p in ['startingPost', 'countPosts','filenameHeader','dirnamePosts']:
        for p in ['users','posts','threads']:
            args[p]=self.getData(p)
        
        rc=eval("WWW._UpdateGraphDB(self,args)")
        
        say("rc",rc)
        
        #for p in ['users','posts','threads']:
        #   say(p,rc[p])
        #   self.setData(p,rc[p])


    def run_WWW_Command(self):
        
        say(self.getData("cypher"))

        args={
        }

        for p in ['cypher']:
            args[p]=self.getData(p)
        
        rc=eval("WWW._Command(self,args)")
        
        say("rc",rc)
        
        
        #for p in ['users','posts','threads']:
        #    say(p,rc[p])
        #    self.setData(p,rc[p])



    def run_WWW_RemoteCSV(self):
    
        fn='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        
        with requests.Session() as s:
            download = s.get(fn)

            udat = download.content.decode('utf-8')
            lines=udat.split('\n')

        ln=0
        
        dat=[l.split(',') for l in lines[:-1]]
        
        #ll=[len(l) for l in lines]
        #print(ll)
        print ("\n"*1)
        print(np.array(dat).shape) 
        print(len(lines))
        tt=[]
        for l in lines[:-1]:
            tt+=[l.split(',')[:76]]
            #print(len(l.split(',')))
        print ("\n"*1)
        print(np.array(tt).shape) 
        #print (tt)


    def run_WWW_ArrayRow(self):
        arr=self.getData("array")
        row=self.getData("row")
        self.setData("results",arr[row])
        

    def run_WWW_ArrayColumn(self):
        arr=self.getData("array")
        col=self.getData("column")
        coldat=[r[col] for r in arr]
        self.setData("results",coldat)
        
    def run_WWW_ArrayToFloat(self):
        arr=self.getData("array")
        coldat=[]
        for r in arr:
            try:
                coldat += [float(r)]
            except:
                coldat +=[0.]
        self.setData("results",coldat)


    def run_WWW_SubList(self):
        arr=self.getData("array")
        start=self.getData("start")
        end=self.getData("end")
        self.setData("results",arr[start:end])
        


# mehr ideen
# http://hplgit.github.io/prog4comp/doc/pub/p4c-sphinx-Python/._pylight005.html

    def run_WWW_SIR(self):

        def SIR(NO,IO,a,b,days,RO=0,samples=200, steps=10000):
            L,S,I,R=[],NO-RO-IO,IO,RO
            L=[(0,NO,IO,RO)]
            Ls=[]
            Ss=[]
            Rs=[]
            step, sampleStep =days/steps, steps//samples
            #print ("step",step)
            for i in range(steps+1):
                if   i%sampleStep == 0:
                    d = i*step
                    L.append((d,S,I,R))
                S,I = S*(1.-a*I*step), I*(1.+(a*S-b)*step)
                #print(i,S,I,R)
                R = NO-S-I

            return L

        def SIR_as(NO,IO,aas,b,days,RO=0,samples=200, steps=10000):
            print ("ass variante")
            L,S,I,R=[],NO-RO-IO,IO,RO
            L=[(0,NO,IO,RO)]
            Ls=[]
            Ss=[]
            Rs=[]
            print("lne",len(aas),steps)
            step, sampleStep =days/steps, steps//samples
            #print ("step",step)
            steps  -= 1
            for i in range(steps+1):
                if   i%sampleStep == 0:
                    d = i*step
                    L.append((d,S,I,R))
                S,I = S*(1.-aas[i]*I*step), I*(1.+(aas[i]*S-b)*step)
                #print(i,S,I,R)
                R = NO-S-I

            return L

        NO=self.getData("kiloNO")*100
        IO=self.getData('IO')
        RO=self.getData('RO')*0.01*NO

        days=self.getData('days')       
        steps=self.getData('steps')
  
        
        fa=0.000001*0.01
        
        a=self.getData("milliA")*fa

        b=1.0/14
        b=1.0/(1+self.getData("invB"))

        samples=self.getData('samples')
        aas=self.getData("milliAs")
        aas=np.array(aas)
        
        print ("millias",aas[0],aas[-1])
        aasf=np.array(aas)*fa
        
        
        yf=0.0001
        yf=0.00005

        if 0:
            rc=SIR(NO,IO,a,b,days,RO,samples=100, steps=steps)
        else:
            rc=SIR_as(NO,IO,aasf,b,days,RO,samples=300, steps=steps)
        
        [dates,Ss,Is,Rs]= np.array(rc).swapaxes(0,1)
#       self.setData('dates',list(dates))
        self.setData('S',list(np.round(Ss)*yf))
        self.setData('I',list(np.round(Is)*yf))
        self.setData('R',list(np.round(Rs)*yf))


    def run_WWW_wire2coords(self):
        
        w=FreeCAD.activeDocument().Sketch.Shape.Wires[0]
        days=self.getData('days')
        samples=self.getData('samples')
        steps=self.getData('steps')
        pts=w.discretize(days)
        
        fy=0.4

        [xs,ys,zs]=np.array(pts).swapaxes(0,1)

        from scipy import interpolate
        f = interpolate.interp1d(xs, ys)
        xnew = np.linspace(0,days,steps)
        ynew = f(xnew) *fy

#        print ("ergebnsie")
#        print(xnew)
#        print(len(ynew))     

        self.setData('x',list(xnew))
        self.setData('y',list(ynew))
        
        self.setData('steps_out',steps)
        
        
    def run_WWW_SearchList(self):
        
        mode =self.getData('mode')     
        dt=self.getData('datatype')
        
        xs=self.getData('x')
        #say(xs)
        
        if dt == 'Float':
            a=self.getData('aFloat')
            if mode == 'x > a':
                found=[]
                for i,x in enumerate(xs):
                    if float(x) > a:
                        found += [i]
            elif mode == 'x >= a':
                found=[]
                for i,x in enumerate(xs):
                    if float(x) >= a:
                        found += [i]

            elif mode == 'x <= a':
                found=[]
                for i,x in enumerate(xs):
                    if float(x) <= a:
                        found += [i]
            elif mode == 'x < a':
                found=[]
                for i,x in enumerate(xs):
                    if float(x) < a:
                        found += [i]
            elif mode == 'x == a':
                found=[]
                for i,x in enumerate(xs):
                    if float(x) == a:
                        found += [i]
            elif mode == 'x != a':
                found=[]
                for i,x in enumerate(xs):
                    if float(x) != a:
                        found += [i]
            else:
                raise Exception ("not implemeted mode:"+ mode )
        if dt == 'String':
            a=self.getData('aString').lower().strip()
            found=[]
            for i,x in enumerate(xs):
                x=x.lower().strip()
                if mode == 'x > a':
                    if x > a:
                        found += [i]
                elif mode == 'x >= a':
                    if x >= a:
                        found += [i]
                elif mode == 'x <= a':
                    if x <= a:
                        found += [i]
                elif mode == 'x < a':
                    if x < a:
                        found += [i]
                elif mode == 'x == a':
                    if x == a:
                        found += [i]
                elif mode == 'x != a':
                    if x != a:
                        found += [i]
                elif mode == 'x starts with a':
                    if x.startswith(a):
                        found += [i]
                elif mode == 'x.endswith(a)':
                    if x.endswith(a):
                        found += [i]
                elif mode == 'x contains a':
                    if a in x:
                        found += [i]

                else:
                    raise Exception ("not implemeted mode:"+ mode )


        else:
                raise Exception ("not implemented datatype:"+dt)
            
        say(found)
        self.setData('found',found)
        try:
            first=found[0]
        except:
            first=-1
        self.setData('first',first)


    def run_WWW_SublistByIndex(self):
        l=self.getData('list')
        ixs=self.getData('index')
        lout=[l[i] for i in ixs]
        self.setData('list_out',lout) 
    
    def run_WWW_BoolOnList(self):
        
        a=self.getData('listA')
        b=self.getData('listB')
        
        self.setData('AfuseB',list(set(a).union(set(b))))
        self.setData('AcommonB',list(set(a).intersection(set(b))))
        self.setData('AcutB',list(set(a).difference(set(b))))
        
        
            
