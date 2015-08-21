import sys
import os
import collections

from veriloggen import *

led_v = '''\
module blinkled #
  (
   parameter WIDTH = 8
  )
  (
   input [0:0] CLK, 
   input [0:0] RST, 
   output reg [WIDTH-1:0] LED
  );
  reg [32-1:0] count;
  always @(posedge CLK) begin
    if(RST) begin        
      count <= 0;
    end else begin
      if(count == 1023) begin
        count <= 0;
      end else begin
        count <= count + 1;
      end
    end 
  end 
  always @(posedge CLK) begin
    if(RST) begin        
      LED <= 0;
    end else begin
      if(count == 1023) begin        
        LED <= LED + 1;
      end  
    end 
  end 
endmodule
'''

def mkLed():
    modules = read_verilog_module_str(led_v)
    m = modules['blinkled']
    
    # change the module name
    m.name = 'modified_led'
    
    # add new statements
    enable = m.Input('enable')
    busy = m.Output('busy')

    old_statement = m.always[0].statement[0].false_statement
    m.always[0].statement[0].false_statement = If(enable)(*old_statement)
    m.Assign( busy(m.variable['count'] < 1023) )
    
    return m

if __name__ == '__main__':
    led_module = mkLed()
    led_code = led_module.to_verilog()
    print(led_code)
