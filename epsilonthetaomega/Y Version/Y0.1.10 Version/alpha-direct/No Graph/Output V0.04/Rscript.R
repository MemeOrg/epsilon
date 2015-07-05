A22R1 = read.csv("A 22 risk 1.csv",header = T)
A22R05 = read.csv("A 22 risk 0.5.csv",header = T)
A22R2 = read.csv ("A 22 risk 2.csv",header = T)
B22R1= read.csv("B 22 risk 1.csv",header = T)
B22R05= read.csv("B 22 risk 0.5.csv",header = T)
B22R2= read.csv ("B 22 risk 2.csv",header = T)

A22R1$Type = "DirectR1"
A22R05$Type = "DirectR05"
A22R2$Type = "DirectR2"

B22R1$Type = "WaitR1"
B22R05$Type = "WaitR05"
B22R2$Type = "WaitR2"

#QALY
A22R1$QALY = A22R1$QALY - B22R1$QALY
A22R05$QALY = A22R05$QALY - B22R05$QALY
A22R2$QALY = A22R2$QALY- B22R2$QALY
#TotalCost
A22R1$TotalCost = A22R1$TotalCost - B22R1$TotalCost
A22R05$TotalCost = A22R05$TotalCost - B22R05$TotalCost
A22R2$TotalCost = A22R2$TotalCost- B22R2$TotalCost

MasterData = rbind(A22R1,A22R05,A22R2)
library(ggplot2)
qplot(QALY,TotalCost,data = MasterData,color = Type)