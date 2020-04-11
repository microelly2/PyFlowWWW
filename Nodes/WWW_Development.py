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

if 0:
    class WWW_Driver(WWWNodeBase):
        '''
        connector to the neo4j database
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
        cypher command 
        '''

        def __init__(self, name="MyToy"):

            super(self.__class__, self).__init__(name)
            self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
            self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
            
            a=self.createInputPin('driver', 'FCobjPin')
                    
            a = self.createInputPin("command", 'StringPin',"MATCH (a)-[r]->(b) RETURN a,b")
            a.description='cypher command'

            a=self.createOutputPin('outList', 'AnyPin',structure=StructureType.Array)
            a.description='list of results'
            #a=self.createOutputPin('outDict', 'AnyPin',structure=StructureType.Dict)
            a.enableOptions(PinOptions.AllowAny)
            a.setData([])

            a=self.createOutputPin('outDict', 'AnyPin',structure=StructureType.Dict)
            a.enableOptions(PinOptions.AllowAny)
            a.setData({})
            a.description='record of data if there is only one answer of the request'

        @staticmethod
        def description():
            return WWW_Session.__doc__

        @staticmethod
        def category():
            return 'Development'


    class WWW_LoadCSV(WWWNodeBase):
        '''
        load a csv file from web or local into the database
        '''

        def __init__(self, name="MyToy"):

            super(self.__class__, self).__init__(name)
            self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
            self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

            a=self.createInputPin('driver', 'FCobjPin')
           
            a = self.createInputPin("filename", 'StringPin','https://neo4j.com/docs/WWW-manual/4.0/csv/artists.csv')
            a.description='url or path name to the csv file'

            self.process = self.createInputPin('withHeaders', 'BoolPin')
            a = self.createInputPin("fieldTerminator", 'StringPin',',')
            
            #LOAD CSV WITH HEADERS FROM 'https://neo4j.com/docs/WWW-manual/4.0/csv/artists-with-headers.csv' AS line
            #CREATE (:Artist { name: line.Name, year: toInteger(line.Year)})
            
            a = self.createInputPin("command", 'StringPin'," CREATE (a:Artist { name: line[1], year: toInteger(line[2])}) return id(a) as id ")
            a.description='subcommand executed on the record named as line'

            a=self.createOutputPin('ids', 'IntPin',structure=StructureType.Array)
            a.description='list of ids of teh created or merged objects' 

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

    @staticmethod
    def description():
        return WWW_GetAdminPost.__doc__


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

    @staticmethod
    def description():
        return WWW_GetPost.__doc__


class WWW_UpdateGraphDB(WWWNodeBase):
    '''
    update neo4j database with data
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

    @staticmethod
    def description():
        return WWW_UpdateGraphDB.__doc__


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

    @staticmethod
    def description():
        return WWW_Command.__doc__


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

    @staticmethod
    def description():
        return WWW_RemoteCSV.__doc__


class WWW_SubArray(WWWNodeBase):
    '''
    create a subarray of an array 
    '''
    
    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='input array'
        
        a=self.createInputPin('rowStart','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}

        a=self.createInputPin('columnStart','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createInputPin('rowEnd','Integer',2)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}

        a=self.createInputPin('columnEnd','Integer',-1)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='resulting array: array[rowStart:rowEnd,columnStart:columnEnd]'

    @staticmethod
    def category():
        return 'WWW'


    @staticmethod
    def description():
        return WWW_SubArray.__doc__


class WWW_SubList(WWWNodeBase):
    '''
    select a sublist of a list
    '''
    
    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='input list'

        a=self.createInputPin('start','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createInputPin('end','Integer',-1)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='resulting list: array[start:end]'

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_SubList.__doc__

class WWW_ArrayRow(WWWNodeBase):
    '''
    select a row of a matrix as list
    '''

    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='input array'
        
        a=self.createInputPin('row','Integer',0)     
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        a.description='number of row, counting starts with 0, last row is -1'
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='row as list'

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_ArrayRow.__doc__

class WWW_ArrayColumn(WWWNodeBase):
    '''
    select a column of a matrix as list
    '''

    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('array', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='input array'

        a=self.createInputPin('column','Integer',0)
        a.annotationDescriptionDict={ "ValueRange":(-10,2000)}
        a.description='number of column, counting starts with 0, last row is -1'
        
        a=self.createOutputPin('results', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='column as list'


    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_ArrayColumn.__doc__


class WWW_ArrayToFloat(WWWNodeBase):
    '''
    convert the cells of a list to floats
    '''

    videos='https://youtu.be/VpkHyqaTgh4'
    
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('array', 'StringPin',structure=StructureType.Array)  
        a.description='list of data'     
        a=self.createOutputPin('results', 'FloatPin',structure=StructureType.Array)
        a.description='np.float(array)'

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_ArrayToFloat.__doc__

class WWW_ProcessArray(WWWNodeBase):
    '''
    A TEST TOOL FOR ARRAY PROCESSING
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

    @staticmethod
    def description():
        return WWW_ProcessArray.__doc__


class WWW_SIR(WWWNodeBase):
    '''
    simulation of the SIR model 
    '''

    videos='https://youtu.be/Hg5Pv4jyRcY'
    
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('comment', 'StringPin')
        a=self.createInputPin('kiloNO', 'Float',10000)
        a.annotationDescriptionDict={ "ValueRange":(1,1000)}
        a.description='size of population at start / 1000' 
        
        a=self.createInputPin('IO', 'Float',1)
        a.annotationDescriptionDict={ "ValueRange":(1,100)}
        a.description='number of infected at start'
        
        a=self.createInputPin('RO', 'Float',0)
        a.annotationDescriptionDict={ "ValueRange":(0,100)}
        a.description='number of recoverd/removed at start'
        
        a=self.createInputPin('milliA', 'Float',50.)
        a.annotationDescriptionDict={ "ValueRange":(1,200)}
        a.description='factor alpha * 1.000.000'
        
        a=self.createInputPin('milliAs', 'FloatPin',[0.1]*100,structure=StructureType.Array)
        a.description='list of alphas  to simulate a changing alpha over time'
        
        
        a=self.createInputPin('invB', 'Float',14)
        a.annotationDescriptionDict={ "ValueRange":(1,1000)}
        a.description='1/beta - number of days'
         
        a=self.createInputPin('days', 'Integer',300)
        a.annotationDescriptionDict={ "ValueRange":(10,300)}
        a.description='how long the simulation should run'
        
        a=self.createInputPin('samples', 'IntPin',1000)
        a.annotationDescriptionDict={ "ValueRange":(10,300)}
        a.description='length of the output lists'
        
        a=self.createInputPin('steps', 'IntPin',300)
        a.annotationDescriptionDict={ "ValueRange":(100,1000000)}
        a.description='number of intervals for the Euler Cauchy method'

        a=self.createOutputPin('dates', 'FloatPin',[0,1,2,3],structure=StructureType.Array)
        a.description='calculated timestamps'
        a=self.createOutputPin('S', 'FloatPin',[10,5,3,1],structure=StructureType.Array)
        a.description='Sensitives'
        
        a=self.createOutputPin('I', 'FloatPin',[1,2,4,8],structure=StructureType.Array)
        a.description='infected'
        a=self.createOutputPin('R', 'FloatPin',[0,3,3,1],structure=StructureType.Array)
        a.description='Recovered'
        
        a=self.createInputPin('mode','String',"run")
        a.description='not implemented'

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_SIR.__doc__


class WWW_wire2coords(WWWNodeBase):
    '''
    creates for a 2D wire a list of points on the wire. The points have all the same x-distances
    '''

    videos='https://youtu.be/Hg5Pv4jyRcY'
    
    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        a=self.createInputPin('wire', 'ShapePin')
        a.description='function like wire: there is only one y for each x '

        #a=self.createInputPin('scale', 'Float',100.)
        a=self.createInputPin('days', 'Integer',100.)
        a.description='number of points on the wire used for inerpolation'
        a.annotationDescriptionDict={ "ValueRange":(10,1000)}

        a=self.createInputPin('samples', 'Integer',200.)
        a.description='number of x values'

        a.annotationDescriptionDict={ "ValueRange":(10,1000)}
              
        a=self.createInputPin('steps', 'Integer',300.)
        a.annotationDescriptionDict={ "ValueRange":(100,1000000)}
        a.description='number of computed points'

        #a=self.createOutputPin('samples_out', 'Integer',200.)
        a=self.createOutputPin('steps_out', 'Integer',300.)
        a.description='the value of steps as outputpin'
        
        a=self.createOutputPin('x', 'FloatPin',[10.,5.,3.,1.],structure=StructureType.Array)
        a.description='x values of the interplation'
        a=self.createOutputPin('y', 'FloatPin',[1.,2.,4.,8.],structure=StructureType.Array)
        a.description='y values of the interplation'

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_wire2coords.__doc__


class WWW_SublistByIndex(WWWNodeBase):
    '''
    extract a sublist by given indices
    '''

    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('list', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='list of data'
        
        a=self.createInputPin('index', 'IntPin',structure=StructureType.Array)
        a.description='list of indices'
        
        a=self.createOutputPin('list_out', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='reduced list' 

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_SublistByIndex.__doc__


class WWW_BoolOnList(WWWNodeBase):
    '''
    boolean set operations on two list: union, intersection, difference
    '''

    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('listA', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='first list fo data'
        
        a=self.createInputPin('listB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='2nd list fo data'
        
        a=self.createOutputPin('AfuseB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description=' union of the sets: a or b, a + b'
        a=self.createOutputPin('AcommonB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description=' intersection of the sets: a and b, a * b'
        a=self.createOutputPin('AcutB', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description=' difference of the sets: a without b, a - b'

    @staticmethod
    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_BoolOnList.__doc__


class WWW_SearchList(WWWNodeBase):
    '''
    compare the elements of a list with a given value and return the list of matching indices
    '''

    videos='https://youtu.be/VpkHyqaTgh4'

    def __init__(self, name="MyToy"):

        super(self.__class__, self).__init__(name)
        
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

        a=self.createInputPin('x', 'AnyPin',structure=StructureType.Array,constraint='1')
        a.description='list of values'

        a=self.createInputPin('aFloat', 'Float',0.)
        a.description='value to compare if datatype is Float or Integer '

        a=self.createInputPin('aString', 'String',)
        a.description='value to compare if datatype is String or regualr Expression'
        
        a=self.createInputPin("datatype",'String','Float')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['Float', 'String', 'regular Expression', 'Integer']
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("Float")
        a.description='which datatype should be used  form comparsion'

        a=self.createInputPin("mode",'String','x <= a')
        a.annotationDescriptionDict={ 
                "editable": False,
                "ValueList":['x == a', 'x > a', 'x >= a', 'x < a ','x <= a','x != a', 'x starts with a','x ends with a', 'x contains a' ]
            }
        a.setInputWidgetVariant("EnumWidget")
        a.setData("x != a")
        a.description='condition to check (depends on datatype) '

        a=self.createOutputPin('first', 'IntPin',-1)      
        a.description='index of the first matching value. -1 if not found'

        a=self.createOutputPin('found', 'IntPin',[10,5,3,1],structure=StructureType.Array)
        a.description='list of indexes of matching values'  

    def category():
        return 'WWW'

    @staticmethod
    def description():
        return WWW_SearchList.__doc__


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
