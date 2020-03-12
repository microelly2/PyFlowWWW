    
from nodeeditor.utils import *
from nodeeditor.say import *

from nodeeditor.say import *

import time,re
import FreeCAD,FreeCADGui
import ssl
import urllib.request



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

        for r in args['users']:
            #say(r)
            cmd="MERGE (a:FoUser{uid:$data[0]}) SET a.name=$data[1] SET a.test=10 RETURN a"
            
            try:
                with driver.session() as session:
                    rc = session.run(cmd,data=r)
                    say(rc.data())
            
            except Exception as e:
                sayErr(e)
                sayErr("Record:")
                sayErr(r)
                
                
        for r in args['threads']:
            #say(r)
            cmd='''
            MERGE (a:FoThread{tid:$data[0],forum:$data[1],title:$data[2]}) 
            SET a.test=9
            RETURN a
            '''
            
            try:
                with driver.session() as session:
                    rc = session.run(cmd,data=r)
                    say(rc.data())
            
            except Exception as e:
                sayErr(e)
                sayErr("Record:")
                sayErr(r)

        for r in args['posts']:
            cmd='''
            MATCH (u:FoUser{uid:$data[2]})
            MATCH (t:FoThread{tid:$data[1]})
            MERGE (a:FoPost{pid:$data[0]}) 
            
            MERGE (a)<-[:by]-(u)
            MERGE (t)<-[:in]-(u)

            SET a.user=$data[2]
            SET t.test=9
            RETURN a,u
            '''
            
            try:
                with driver.session() as session:
                    rc = session.run(cmd,data=r)
                    say(rc.data())
            
            except Exception as e:
                sayErr(e)
                sayErr("Record:")
                sayErr(r)




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

