#!/usr/bin/env python3.12

class SumTable:

   def __init__(self,arr):
       self.matrix = arr
   
   def __setitem__(self,index,value):
       	row = index[0]
       	column = index[1]
        self.matrix[row][column] = value

   def __getitem__(self,index):
        result = 0
        row_start = int(str(index[0])[6:7])
        row_end = int(str(index[0])[9:10]) 
        col_start = int(str(index[1])[6:7])
        col_end = int(str(index[1])[9:10])

        
        for i in range(row_start,row_end):
            for j in range(col_start,col_end):
                result = result + self.matrix[i][j]

        return result

arr = [[1,2,3],[4,5,6]]

#arr = [[-1,1],[1,-1]]
my_table = SumTable(arr)

s = my_table[0:2,1:3]
print(s)
my_table[0,1] = 10
s = my_table[0:2,1:3]
print(s)
