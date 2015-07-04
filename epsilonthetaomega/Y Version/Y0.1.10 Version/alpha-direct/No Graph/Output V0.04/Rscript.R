A22R1 = read.csv("A 22 risk 1.csv",header = T)
A22R05 = read.csv("A 22 risk 0.5.csv",header = T)
A22R2 = read.csv ("A 22 risk 2.csv",header = T)
B22R1= read.csv("B 22 risk 1.csv",header = T)
B22R05= read.csv("B 22 risk 0.5.csv",header = T)
B22R2= read.csv ("B 22 risk 2.csv",header = T)
Month24 = read.csv ("V003-24.csv",header = T)
UsualCare$Type = "UsualCare"
Target15$Type = "Target15"
Month6$Type = "Month6"
Month24$Type = "Month24"

#QALY
Target15$QALY = Target15$QALY - UsualCare$QALY
Month6$QALY = Month6$QALY - UsualCare$QALY
Month24$QALY = Month24$QALY- UsualCare$QALY
#TotalCost
Target15$TotalCost = Target15$TotalCost - UsualCare$TotalCost
Month6$TotalCost = Month6$TotalCost - UsualCare$TotalCost
Month24$TotalCost = Month24$TotalCost- UsualCare$TotalCost

MasterData = rbind(Target15,Month6,Month24)
library(ggplot2)
qplot(QALY,TotalCost,data = MasterData,color = Type)
