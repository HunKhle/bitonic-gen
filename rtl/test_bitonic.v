`timescale 1ns/1ps
module test_sort;

logic [`SORT_SIZE-1:0][`DATA_WIDTH-1:0] data_in;
logic [`SORT_SIZE-1:0][`DATA_WIDTH-1:0] data_out;
logic clk;

always begin
	#10
	clk =  ~clk;
end


    bitonic_sorter bs(clk,data_in,data_out);
initial begin

    clk = 0;
    $display("testing with input size of %d", `SORT_SIZE);

    for(int i=0;i<`SORT_SIZE;i++) begin
        data_in[i] = {$random,$random};
        $display(data_in[i]);

    end

    #500000000
    $display("-----------------------------");
    for(int i=0;i<`SORT_SIZE;i++) begin
       $display(data_out[i]);
    end

    $finish;



end
endmodule
