import math
from params import *


class CompareAndSwap:

    #input wires
    a = "";
    b = "";

    #operation: either comp_swap_asc or comp_swap_dsc
    op = "";

    #output wires
    a_out = ""
    b_out = ""

    #instance name
    name = ""

    def __init__(self, op, name, a, b, a_out, b_out):
        self.op = op
        self.a = a
        self.b = b
        self.a_out = a_out
        self.b_out = b_out
        self.name = name

    def getStr(self):
        return "{0} {1}(clk, {2},{3},{4},{5});".format(self.op, self.name, self.a,self.b,self.a_out,self.b_out)



comparators = []


def bitonic_sort(up, x):
    if len(x) <= 1:
        return x
    else: 
        first = bitonic_sort(True, x[:len(x) / 2])
        second = bitonic_sort(False, x[len(x) / 2:])
        return bitonic_merge(up, first + second)
 
def bitonic_merge(up, x): 
    # assume input x is bitonic, and sorted list is returned 
    if len(x) == 1:
        return x
    else:
        bitonic_compare(up, x)
        first = bitonic_merge(up, x[:len(x) / 2])
        second = bitonic_merge(up, x[len(x) / 2:])
        return first + second
 
def bitonic_compare(up, x):

    dist = len(x) / 2
    for i in range(dist):  
        if(up):
            csw = CompareAndSwap(op="comp_swap_asc", 
                                name="comp_swap_asc"+str(len(comparators)), 
                                a=str(x[i]),  b=str(x[i+dist]), a_out="", b_out="")

            comparators.append(csw)
            #print "comp_swap_asc(a[" + str(x[i]) + "],a["  + str(x[i + dist]) + "])"
        else:
            csw = CompareAndSwap(op = "comp_swap_dsc", 
                                name = "comp_swap_dsc"+str(len(comparators)) , 
                                a=str(x[i]),  b=str(x[i+dist]), a_out="", b_out="")

            comparators.append(csw)
            #print "comp_swap_dsc(a[" + str(x[i]) + "],a["  + str(x[i + dist]) + "])"

        #if (x[i] > x[i + dist]) == up:
        #    x[i], x[i + dist] = x[i + dist], x[i] #swap


def get_pipeline_positions(comparator_stages, pipeline_stages):

    internal_stages = math.ceil( float(comparator_stages)/pipeline_stages )

    pos = []
    current_stage = internal_stages


    while(current_stage < comparator_stages):
        pos.append(current_stage)
        current_stage = current_stage + internal_stages;

    return pos



def interconnect(comparators, inputSize, dataWidth):
    wires = []
    assignments = []
    ports = {}

    
    pipeline_regs = []


    #note that in a single stage we have (SORT_SIZE/2) comparators
    sort_stages = len(comparators)/(SORT_SIZE/2)

    pipeline_reg_positions = get_pipeline_positions(sort_stages ,PIPELINE_STAGES) 

    print "Stages:" + str( pipeline_reg_positions )

    for i in range(inputSize):
        ports[str(i)] = 0
        
        #connect input to the first stage input wires
        assignments.append("assign wire{0}_0 = data_in[{0}]".format(i))


    
    for cmp in comparators:
        a = cmp.a
        b = cmp.b

        cmp.a = 'wire' + a + '_' + str(ports[a])
        cmp.b = 'wire' + b + '_' +  str(ports[b])

        wires.append('wire' + a + '_' +  str(ports[a]))
        wires.append('wire' + b + '_' +  str(ports[b]))

        ports[a] += 1;
        ports[b] += 1;

        cmp.a_out = 'wire' + a + '_' + str(ports[a])
        cmp.b_out = 'wire' + b + '_' + str(ports[b])

        wires.append('wire' + a + '_' +  str(ports[a]))
        wires.append('wire' + b + '_' + str(ports[b]))

        #we add pipeline registers at the right place
        # n_out->{cmp_swap}->n+1_out becomes:
        # n_out_pipe_reg_in -> {reg} -> n_out -> 

        if(int(ports[a]) in pipeline_reg_positions):
            new_a_out = cmp.a_out + "_pipe_reg_in"
            new_b_out = cmp.b_out + "_pipe_reg_in"

            wires.append(new_a_out)
            wires.append(new_b_out)
            
            #pipe_out_a = cmp.a_out + "_pipe_reg_out"
            #pipe_out_b = cmp.b_out + "_pipe_reg_out"

            #reg = add_pipeline_reg( [new_a_out , new_b_out], [cmp.a_out, cmp.b_out] )

            reg = "{0} <= {1}".format(cmp.a_out, new_a_out);
            pipeline_regs.append(reg);

            reg = "{0} <= {1}".format(cmp.b_out, new_b_out)
            pipeline_regs.append(reg)

            cmp.a_out = new_a_out
            cmp.b_out = new_b_out



        #print cmp.getStr()

    #connect output port to last stages
    for i in range(inputSize):
        assignments.append("assign data_out[{0}] = wire{0}_{1}".format(i,ports[str(i)] ))



    wires = set(wires)
    wireDef = "logic [`DATA_WIDTH-1:0] "
    body = "";

    for w in wires:
        body += wireDef + w + ';\n' 


    body += "\n\n\n";

    for a in assignments:
        body += a + ";\n"

    body += "\n\n\n";

    body += "always @(posedge clk) begin\n"  

    for reg in pipeline_regs:
        body += "    " + reg + ";\n"

    body += "end"

    body += "\n\n\n";
    
    for cmp in comparators:
        body += cmp.getStr() + '\n';

    return body


if __name__ == '__main__':

    moduleHeader = "module bitonic_sorter (input clk, input [`SORT_SIZE-1:0][`DATA_WIDTH-1:0] data_in, //data to be sorted \n \
                    output logic [`SORT_SIZE-1:0][`DATA_WIDTH-1:0] data_out);"

    sortIn = range(0,SORT_SIZE)
    bitonic_sort(True, sortIn)
    body = interconnect( comparators, len(sortIn) ,DATA_WIDTH)

    fileName = 'bitonic.v'

    f = open(fileName, 'w+')

    f.write(moduleHeader + '\n' + body + '\n' + 'endmodule')

    f.close()

    fileName = "sys_defs.vh"
    f = open(fileName , 'w+')
    f.write("`define SORT_SIZE\t" + str( SORT_SIZE ) + "\n`define DATA_WIDTH\t" + str(DATA_WIDTH) + "\n")
    f.close()
