`timescale 1ns/1ps
module comp_swap_asc (
    input clk,
    input [`DATA_WIDTH-1:0] a,
    input [`DATA_WIDTH-1:0] b,

    output logic [`DATA_WIDTH-1:0] a_o,
    output logic [`DATA_WIDTH-1:0] b_o

);


    logic  [`DATA_WIDTH-1:0]  a_next;
    logic [`DATA_WIDTH-1:0] b_next;


    always_comb begin

        if(b<a) begin
            a_next = b;
            b_next = a;
        end
        else begin
            a_next = a;
            b_next = b;
       end
    end


    always_ff @(posedge clk) begin

        a_o <= a_next;
        b_o <= b_next;

    end


endmodule


module comp_swap_dsc (
    input clk,
    input [`DATA_WIDTH-1:0] a,
    input [`DATA_WIDTH-1:0] b,

    output logic  [`DATA_WIDTH-1:0] a_o,
    output logic [`DATA_WIDTH-1:0] b_o
);


    logic [`DATA_WIDTH-1:0] a_next;
    logic [`DATA_WIDTH-1:0] b_next;

    always_comb begin

        if(a<b) begin
            a_next = b;
            b_next = a;
        end
        else begin 
            a_next = a;
            b_next = b;
        end


    end

    always_ff @(posedge clk) begin

        a_o <= a_next;
        b_o <= b_next;

    end


endmodule




