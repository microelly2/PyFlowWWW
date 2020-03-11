'''
nodes under development
nodes for debugging and test data 
some stuff to play and new prototypes in very alpha state
'''

from PyFlow.Packages.PyFlowWWW.Nodes import *
from PyFlow.Packages.PyFlowWWW.Nodes.WWW_Base import WWWNodeBase


'''
ideen
https://github.com/community-graph/twitter-import/blob/master/twitter-import.py

'''


class WWW_Driver(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        

        a = self.createInputPin("uri", 'StringPin',"bolt://localhost:7687")
        a = self.createInputPin("user", 'StringPin',"neo4j")
        a = self.createInputPin("password", 'StringPin',"password")

        

        a=self.createOutputPin('driver', 'FCobjPin')
        


    @staticmethod
    def description():
        return WWW_Driver.__doc__

    @staticmethod
    def category():
        return 'Development'

class WWW_Session(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        
        a=self.createInputPin('driver', 'FCobjPin')
        
                
        a = self.createInputPin("command", 'StringPin',"MATCH (a)-[r]->(b) RETURN a,b")
#        self.process = self.createInputPin('process', 'Boolean')
        

        
#        a=self.createOutputPin('resultObject', 'FCobjPin')
#        a=self.createOutputPin('resultString', 'String')
        #a=self.createOutputPin('ids', 'IntPin',structure=StructureType.Array)
        a=self.createOutputPin('outList', 'AnyPin',structure=StructureType.Array)
        #a=self.createOutputPin('outDict', 'AnyPin',structure=StructureType.Dict)
        a.enableOptions(PinOptions.AllowAny)
        a.setData([])

        a=self.createOutputPin('outDict', 'AnyPin',structure=StructureType.Dict)
        a.enableOptions(PinOptions.AllowAny)
        a.setData({})
        
        
        #FCobjPin


    @staticmethod
    def description():
        return WWW_Session.__doc__

    @staticmethod
    def category():
        return 'Development'


class WWW_LoadCSV(WWWNodeBase):
    '''
    a connection to a database
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        a = self.createInputPin("filename", 'StringPin','https://neo4j.com/docs/WWW-manual/4.0/csv/artists.csv')

        self.process = self.createInputPin('withHeaders', 'BoolPin')
        a = self.createInputPin("fieldTerminator", 'StringPin',',')
        
        #LOAD CSV WITH HEADERS FROM 'https://neo4j.com/docs/WWW-manual/4.0/csv/artists-with-headers.csv' AS line
        #CREATE (:Artist { name: line.Name, year: toInteger(line.Year)})
        
        a = self.createInputPin("command", 'StringPin'," CREATE (a:Artist { name: line[1], year: toInteger(line[2])}) return id(a) as id ")
        

        #self.process = self.createInputPin('process', 'Boolean')
        #a=self.createOutputPin('resultObject', 'FCobjPin')
        #a=self.createOutputPin('resultString', 'StringPin')
        a=self.createOutputPin('ids', 'IntPin',structure=StructureType.Array)
        
        

    @staticmethod
    def description():
        return WWW_LoadCSV.__doc__

    @staticmethod
    def category():
        return 'Development'



class WWW_GetAdminPost(WWWNodeBase):
    '''
    download posts as admin
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        p=375528
        a=self.createInputPin('startingPost', 'IntPin',p)
        
        a.annotationDescriptionDict={ "ValueRange":(p-1000,p+100)}
        a=self.createInputPin('countPosts', 'IntPin',3)
        a.annotationDescriptionDict={ "ValueRange":(0,200)}
        
        a=self.createInputPin('filenameUserIP', 'StringPin',"/home/thomas/forum_scan_test/ip_user.txt")
        a=self.createInputPin('filenamePostIP', 'StringPin',"/home/thomas/forum_scan_test/ip_post.txt")
        

        a=self.createOutputPin('UserIP', 'StringPin',structure=StructureType.Array)
        a=self.createOutputPin('PostIP', 'StringPin',structure=StructureType.Array)
        
        self.inExec = self.createInputPin('stop', 'ExecPin', None, self.stop)


    @staticmethod
    def category():
        return 'WWW'


class WWW_GetPost(WWWNodeBase):
    '''
    anonymious download posts
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        p=375528
        p=375650 # 10.3. 17:00
        p=375952 # 11.3 16:00
        a=self.createInputPin('startingPost', 'IntPin',p)
        
        a.annotationDescriptionDict={ "ValueRange":(p-1000,p+100)}
        a=self.createInputPin('countPosts', 'IntPin',2)
        a.annotationDescriptionDict={ "ValueRange":(0,200)}
        
        a=self.createInputPin('filenameHeader', 'StringPin',"/home/thomas/forum_scan_test/data_forum_v4.txt")
        a=self.createInputPin('dirnamePosts', 'StringPin',"/home/thomas/forum_scan_v4/")
        

        a=self.createOutputPin('users', 'StringPin',structure=StructureType.Array)
        a=self.createOutputPin('posts', 'StringPin',structure=StructureType.Array)
        
        a=self.createOutputPin('threads', 'StringPin',structure=StructureType.Array)
        
        self.inExec = self.createInputPin('stop', 'ExecPin', None, self.stop)
        

        a=self.createInputPin('cypher', 'StringPin')    
        a.setInputWidgetVariant("MultilineWidget")


    @staticmethod
    def category():
        return 'WWW'



class WWW_UpdateGraphDB(WWWNodeBase):
    '''
    update database by data
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        p=375528
        p=375650 # 10.3. 17:00
        a=self.createInputPin('startingPost', 'IntPin',p)
        
        a.annotationDescriptionDict={ "ValueRange":(p-1000,p+100)}
        a=self.createInputPin('countPosts', 'IntPin',2)
        a.annotationDescriptionDict={ "ValueRange":(0,200)}
        
        mode=self.createInputPin('mode','StringPin')
        

        a=self.createInputPin('users', 'StringPin',structure=StructureType.Array)
        a=self.createInputPin('posts', 'StringPin',structure=StructureType.Array)
        a=self.createInputPin('threads', 'StringPin',structure=StructureType.Array)
        
        self.inExec = self.createInputPin('stop', 'ExecPin', None, self.stop)


    @staticmethod
    def category():
        return 'WWW'


class WWW_Command(WWWNodeBase):
    '''
    single cypher command to database
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('driver', 'FCobjPin')
        
        a=self.createOutputPin('results', 'StringPin',structure=StructureType.Array)

        a=self.createInputPin('cypher', 'StringPin')    
        a.setInputWidgetVariant("MultilineWidget")

        self.inExec = self.createInputPin('stop', 'ExecPin', None, self.stop)

    @staticmethod
    def category():
        return 'WWW'



def nodelist():
    return [
        WWW_GetAdminPost,
        WWW_GetPost,
        WWW_UpdateGraphDB,
        WWW_Command
    ]
