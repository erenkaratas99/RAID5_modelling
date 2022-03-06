# RAID5_modelling

In this repository, I've wrote down a Python code that models RAID5 configuration.

Steps can be described as follows;

1) Data splitted into 3 sectors
2) Data converted into binary form
3) XOR gate applied vertically
   sector 1 --> 1001 ...
   sector 2 --> 0011 ...
   sector 3 --> 1010 ...
   sector 4 --> 0000 ...
   
   (sector 1) XOR (sector 2) XOR (sector 3) => sector 4
   
4) Crash test;
  --> sector 2 crashed (could be even physically burned) 
  --> looking up to other 3 sectors and creating the exact sector 2 again (getting data back)
  
In this structure, even a sector crashes, you can get your data back
   
   
      
