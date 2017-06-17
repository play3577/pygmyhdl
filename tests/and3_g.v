// File: and3_g.v
// Generated by MyHDL 1.0dev
// Date: Fri Jun 16 12:56:07 2017


`timescale 1ns/10ps

module and3_g (
    a,
    b,
    c,
    o
);


input a;
input b;
input c;
output o;
wire o;

wire o_a_b;




assign o = (c & o_a_b);



assign o_a_b = (a & b);

endmodule
