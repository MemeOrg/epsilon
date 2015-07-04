UsualCare = read.csv("UsualCare.csv",header = T)
Target15 = read.csv("15Taget.csv",header = T)
Month6 = read.csv ("6Interval.csv",header = T)
Month24 = read.csv ("24Interval.csv",header = T)
XModel = read.csv("XModel.csv",header = T)
UsualCare$Type = "UsualCare"
Target15$Type = "Target15"
Month6$Type = "Month6"
Month24$Type = "Month24"
XModel$Type = "FixedIOPandErr"
#QALY
Target15$QALY = Target15$QALY - UsualCare$QALY
Month6$QALY = Month6$QALY - UsualCare$QALY
Month24$QALY = Month24$QALY- UsualCare$QALY
XModel$QALY = XModel$QALY - UsualCare$QALY
#TotalCost
Target15$TotalCost = Target15$TotalCost - UsualCare$TotalCost
Month6$TotalCost = Month6$TotalCost - UsualCare$TotalCost
Month24$TotalCost = Month24$TotalCost- UsualCare$TotalCost
XModel$TotalCost = XModel$TotalCost- UsualCare$TotalCost

MasterData = rbind(Target15,Month6,Month24,XModel)
MasterPartial = rbind(Target15,Month6,Month24)
library(ggplot2)
qplot(QALY,TotalCost,data = MasterData,color = Type)
qplot(QALY,TotalCost,data = MasterPartial,color = Type)
