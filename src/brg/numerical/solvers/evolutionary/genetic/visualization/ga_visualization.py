import matplotlib,re,json,math
import matplotlib.pyplot as plt
import pylab as p
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon

__author__     = ['Tomas Mendez Echenagucia <mtomas@ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'mtomas@ethz.ch'

class GA_VIS:
    """This class is to be used for the visualization of the optimization performed by the 
    ``brg_ga.ga`` function. The function ``draw_ga_evolution`` produces a PDF that shows the
    minimum, maximum and average fitness value of the genetic population per generation. 
    """

    def __init__(self):
        """Initializes the GA_VIS object
        Parameters
        ----------
        boundaries: dict
            This dictionary contains all the max and min bounds for each optimization variable. 
            ``boundaries[index] = [min,max]``.
        color_dict: dict
            Index to color dictionary. 
        conversion_function: function
            If a function ``foo(x)`` is given, the fitness values will be displayed not as 
            originally used during optimization, but as the output of ``foo(x)``. This is 
            convinient for unit changes or general fitness value transformations. 
        generation: int
            The current generation. 
        fit_name: str
            The name assigend to the fitnness function. 
        input_path: str
            The path to the GA results file. 
        lable_size: int
            Lable size in pt. 
        num_gen: int
            The total number of generations in the GA optimization. 
        num_var: int
            The number of optimization variables. 
        number_size: int
            The size if numbers in the visualization in pt. 
        output_path: str
            The path in which the visualization PDF will be written. 
        pop: dict
            The population dictionary, contains the binary, decoded and scaled data for each 
            individual of the population, as well as their fitness values. 
        start_from_gen: int
            If this value is given, the visualization will show only from the selected 
            generation. 
        title_size: int
            The size title of the visualization in pt. 
        xtics: int
            The number of tics in the x axis or vertical lines in the visualization. 
        """
        #self.boundaries = {}
        self.color_dict = {0:'r',1:'y',2:'g',3:'c',4:'b',5:'k'}
        self.conversion_function = None
        self.generation = 0
        self.fit_name = []
        self.fit_type = ''
        self.input_path= ''
        self.lable_size = 15
        self.num_gen = 0
        self.num_pop = 0
        #self.num_var = 0
        self.number_size = 15
        self.output_path = ''
        self.pop   = {'binary':{},'decoded':{},'scaled':{},
                             'fit_value':{}}
        self.start_from_gen = 0
        self.title_size = 20
        self.xticks = None
        self.y_bounds = {'y_min':None,'y_max':None}
        self.y_caps = {'y_min':float('-inf'),'y_max':float('inf')}
        
    
    def get_ga_input_from_file(self,filename):
        with open(self.input_path+filename, 'rb') as fh:
            ga = json.load(fh)
        
        #self.num_var        = ga['num_var']
        self.num_pop        = ga['num_pop']
        #self.boundaries     = ga['boundaries']
        self.fit_name       = ga['fit_name']
        self.min_fit        = ga['min_fit']
        self.fit_type       = ga['fit_type']
        if ga['end_gen']:
            self.num_gen = ga['end_gen']
        else:
            self.num_gen        = ga['num_gen']
        if not self.start_from_gen and self.start_from_gen != 0:
            if ga['start_from_gen']:
                self.start_from_gen = ga['start_from_gen']

    def get_pop_from_pop_file(self):
        file_pop  = {'binary':{},'decoded':{},'scaled':{},'fit_value':{},
                     'pf':{}}
        filename  = 'generation '+ "%04d" % self.generation + '_population'+ ".pop"
        filename = self.input_path+filename
        pf_file = open(filename, 'r')
        lines = pf_file.readlines()
        pf_file.close()
        
        for i in range(self.num_pop):
            file_pop['scaled'][i] = {}
            file_pop['fit_value'][i] = {}
            line_scaled = lines[i+7]
            line_fit = lines[i+9+self.num_pop]
            string_scaled = re.split(',',line_scaled)
            string_fit = re.split(',',line_fit)
            string_fit = string_fit[1]
            del string_scaled[-1]
            del string_scaled[0]
            scaled = [float(j) for j in string_scaled]
            fit_value = float(string_fit)
            for j in range(len(scaled)):
                file_pop['scaled'][i][j] = scaled[j] 
            file_pop['fit_value'][i] = fit_value
        
        return file_pop
    
    def get_min_max_avg(self,pop):
        values = pop['fit_value'].values()
        #values_ = values
        values_ = []
        for value in values:
            if value <= self.y_caps['y_min'] or value >= self.y_caps['y_max']:
                continue
                #values_.append(None)
            else:
                values_.append(value)
        min_ = min(values_)
        max_ = max(values_)
        avg_ = sum(values_)/len(values_)
        return min_,max_,avg_
    
    def find_tick_size(self):
        size = self.num_gen
        size = int(math.ceil(size / 10.0)) * 10
        self.xticks = int(round(size/5.0,10))
        print 'self.xticks',self.xticks
        
    def draw_ga_evolution(self,filename):
        
        self.get_ga_input_from_file(filename)        
        
        min_list = []
        max_list = []
        avg_list = []
        for i in range(self.start_from_gen,self.num_gen+1):
            print 'reading gen ',i
            self.generation = i 
            try:
                fpop = self.get_pop_from_pop_file()
                min_,max_,avg_ = self.get_min_max_avg(fpop)
                if self.conversion_function:
                    min_ =self.conversion_function(min_)
                    max_ =self.conversion_function(max_)
                    avg_ =self.conversion_function(avg_)
                min_list.append(min_)
                max_list.append(max_)
                avg_list.append(avg_)
            except:
                self.num_gen = self.generation-1
                print 'generation ',self.generation,' pop file not found'
                print 'results plotted until generation ',self.generation -1
                break
        
        fig = plt.gcf()
        plt.clf()
        fig.set_size_inches(12,11)
        
        if not self.xticks:
            self.find_tick_size()
        
        if self.fit_type == 'max':
            plt.plot(min_list,color='black',lw=0.1,label='Min.')
            plt.plot(max_list,color='black',lw=2,label='Max.')
            loc = 4

        else:
            plt.plot(min_list,color='black',lw=2,label='Min.')
            plt.plot(max_list,color='black'  ,lw=0.1,label='Max.')  
            loc = 1          
        plt.plot(avg_list,color='red' ,lw=0.1,label='Avg.')
        
        plt.xlim((-self.xticks/2.0,self.num_gen-self.start_from_gen))
        
        if self.y_bounds['y_min']:
            y_min = self.y_bounds['y_min']
        else:
            y_min = min(min_list)
        
        if self.y_bounds['y_max']:
            y_max = self.y_bounds['y_max']
        else:
            y_max = max(max_list)

        if self.min_fit:
            plt.axhline(self.min_fit, color='red', ls= ':',lw=0.5)
            string = self.fit_type + ' fit'
            plt.text(-self.xticks/20,self.min_fit, string,horizontalalignment='right',color= 'red')
            #self.min_fit,self.num_gen-self.start_from_gen
            if self.min_fit < min(min_list):
                y_min = self.min_fit

        
        delta = y_max-y_min
        plt.ylim((y_min-(delta*0.1),y_max+delta*0.1))
        plt.title(self.fit_name + ' evolution',fontsize=self.title_size)
        plt.xlabel('generation', fontsize=self.lable_size)
        plt.ylabel(self.fit_name, fontsize=self.lable_size)
        labels = range(self.start_from_gen,self.num_gen,self.xticks)
        x = range(0,len(labels)*self.xticks,self.xticks)
        plt.xticks(x, labels)
        plt.grid(True)
        plt.legend(loc=loc)
        plt.savefig(self.output_path+self.fit_name+'_evolution.pdf')
        
        print 'done'
    
if __name__ == '__main__':
    
    vis = GA_VIS()
    vis.input_path = '../_scripts/out/'
    vis.output_path = vis.input_path 
    filename = 'fitness1.json'
    vis.conversion_function = None
    vis.start_from_gen = 0
    
    vis.draw_ga_evolution(filename)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    