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
        # p=376492 #13.3.16:00
        
        p=376500
        
        
        a=self.createInputPin('startingPost', 'IntPin',p)
        
        a.annotationDescriptionDict={ "ValueRange":(p,p+1000)}
        a=self.createInputPin('countPosts', 'IntPin',2)
        a.annotationDescriptionDict={ "ValueRange":(0,1000)}
        
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
#        a=self.createInputPin('startingPost', 'IntPin',p)
        
#        a.annotationDescriptionDict={ "ValueRange":(p-1000,p+100)}
#        a=self.createInputPin('countPosts', 'IntPin',2)
#        a.annotationDescriptionDict={ "ValueRange":(0,200)}
        
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


class WWW_RemoteCSV(WWWNodeBase):
    '''
    read csv  from internet
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('url', 'StringPin')
        
        a=self.createOutputPin('results', 'StringPin',structure=StructureType.Array)



    @staticmethod
    def category():
        return 'WWW'


class WWW_SubArray(WWWNodeBase):
    '''
    read csv  from internet
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        #a=self.createInputPin('url', 'StringPin')
        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('rowStart','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}



        a=self.createInputPin('columnStart','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createInputPin('rowEnd','Integer',2)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        a=self.createInputPin('columnEnd','Integer',-1)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')


    @staticmethod
    def category():
        return 'WWW'



class WWW_SubList(WWWNodeBase):
    '''
    read csv  from internet
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        #a=self.createInputPin('url', 'StringPin')
        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('start','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}



        
        a=self.createInputPin('end','Integer',-1)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')


    @staticmethod
    def category():
        return 'WWW'

class WWW_ArrayRow(WWWNodeBase):
    '''
    read csv  from internet
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        #a=self.createInputPin('url', 'StringPin')
        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('row','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')



    @staticmethod
    def category():
        return 'WWW'

class WWW_ArrayColumn(WWWNodeBase):
    '''
    read csv  from internet
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        #a=self.createInputPin('url', 'StringPin')
        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('column','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')



    @staticmethod
    def category():
        return 'WWW'

class WWW_ArrayToFloat(WWWNodeBase):
    '''

    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('array', 'StringPin',structure=StructureType.Array)       
        a=self.createOutputPin('results', 'FloatPin',structure=StructureType.Array)


    @staticmethod
    def category():
        return 'WWW'

class WWW_ProcessArray(WWWNodeBase):
    '''
    read csv  from internet
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('url', 'StringPin')
        a=self.createInputPin('array', 'StringPin',structure=StructureType.Array)
        a=self.createInputPin('mode','String',"run")
        
        a=self.createOutputPin('results', 'StringPin',structure=StructureType.Array)



    @staticmethod
    def category():
        return 'WWW'



class WWW_SIR(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('comment', 'StringPin')
        a=self.createInputPin('kiloNO', 'Float',10000)
        a.annotationDescriptionDict={ "ValueRange":(1,1000)}
        a=self.createInputPin('IO', 'Float',1)
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        a=self.createInputPin('RO', 'Float',0)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}
        a=self.createInputPin('milliA', 'Float',50.)
        a.annotationDescriptionDict={ "ValueRange":(1,200)}
        a=self.createInputPin('milliAs', 'FloatPin',[0.1]*100,structure=StructureType.Array)
        
        
        a=self.createInputPin('invB', 'Float',14)
        a.annotationDescriptionDict={ "ValueRange":(1,1000)}
        a=self.createInputPin('days', 'Integer',300)
        a.annotationDescriptionDict={ "ValueRange":(10,300)}
        a=self.createInputPin('samples', 'IntPin',1000)
        a.annotationDescriptionDict={ "ValueRange":(10,300)}
        a=self.createInputPin('steps', 'IntPin',300)
        a.annotationDescriptionDict={ "ValueRange":(100,1000000)}

        a=self.createOutputPin('dates', 'FloatPin',[0,1,2,3],structure=StructureType.Array)
        a=self.createOutputPin('S', 'FloatPin',[10,5,3,1],structure=StructureType.Array)
        a=self.createOutputPin('I', 'FloatPin',[1,2,4,8],structure=StructureType.Array)
        a=self.createOutputPin('R', 'FloatPin',[0,3,3,1],structure=StructureType.Array)
        
        a=self.createInputPin('mode','String',"run")
        
        a=self.createOutputPin('Shape_out', 'ShapePin')



    @staticmethod
    def category():
        return 'WWW'

#

class WWW_wire2coords(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('wire', 'ShapePin')
#        a=self.createInputPin('count', 'Integer',100)
        
#        a.annotationDescriptionDict={ "ValueRange":(2,100)}
        a=self.createInputPin('scale', 'Float',100.)
        a=self.createInputPin('days', 'Integer',100.)
        a.annotationDescriptionDict={ "ValueRange":(10,1000)}
        a=self.createInputPin('samples', 'Integer',200.)
        a.annotationDescriptionDict={ "ValueRange":(10,1000)}
        a=self.createOutputPin('samples_out', 'Integer',200.)
        
        a=self.createInputPin('steps', 'Integer',300.)
        a.annotationDescriptionDict={ "ValueRange":(100,1000000)}
        a=self.createOutputPin('steps_out', 'Integer',300.)
        
        a=self.createOutputPin('x', 'FloatPin',[10.,5.,3.,1.],structure=StructureType.Array)
        a=self.createOutputPin('y', 'FloatPin',[1.,2.,4.,8.],structure=StructureType.Array)

    def category():
        return 'WWW'


class WWW_SublistByIndex(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('list', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('index', 'IntPin',structure=StructureType.Array)
        a=self.createOutputPin('list_out', 'AnyPin',structure=StructureType.Array,constraint='1')

    def category():
        return 'WWW'


class WWW_BoolOnList(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('listA', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('listB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createOutputPin('AfuseB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createOutputPin('AcommonB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createOutputPin('AcutB', 'AnyPin',structure=StructureType.Array,constraint='1')

    def category():
        return 'WWW'


class WWW_SearchList(WWWNodeBase):
    '''
    '''

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('x', 'AnyPin',structure=StructureType.Array,constraint='1')
        a=self.createInputPin('aFloat', 'Float',0.)
        a=self.createInputPin('aString', 'String',)
        
        a=self.createInputPin("datatype",'String','Float')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['Float', 'String', 'regular Expression', 'Integer']
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("Float")
        
       

        a=self.createInputPin("mode",'String','x <= a')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['x == a', 'x > a', 'x >= a', 'x <= a','x != a', 'x starts with a','x ends with a', 'x contains a' ]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("x != a")





        a=self.createOutputPin('first', 'IntPin',-1)      
        a=self.createOutputPin('found', 'IntPin',[10,5,3,1],structure=StructureType.Array)

    def category():
        return 'WWW'


def nodelist():
    return [
        WWW_GetAdminPost,
        WWW_GetPost,
        WWW_UpdateGraphDB,
        WWW_Command,

        WWW_RemoteCSV,       
        WWW_SubArray,
        WWW_SubList,
        WWW_ArrayRow,
        WWW_ArrayColumn,
        WWW_ProcessArray,
        WWW_ArrayToFloat,
        #WWW_Plot2D,
        WWW_SIR,
        WWW_wire2coords,
        WWW_SearchList,
        WWW_SublistByIndex,
        WWW_BoolOnList,

        
        
    ]
