options(digits=2)

require(likert)
data(pisaitems)

##### Item 24: Reading Attitudes
items24 <- pisaitems[,substr(names(pisaitems), 1,5) == 'ST24Q']
head(items24); ncol(items24)
mylevels <- c('Disagree', 'Somewhat Disagree', 'Neutral', 'Somewhat Agree', 'Agree')
part1 <- c( "Somewhat Disagree", "Somewhat Agree", "Somewhat Agree", "Agree", "Agree", "Somewhat Agree","Somewhat Agree","Agree","Agree")
part2 <- c( "Neutral", "Somewhat Agree", "Agree", "Agree", "Somewhat Disagree", "Somewhat Disagree","Neutral","Somewhat Disagree","Agree")
part3 <- c( "Somewhat Disagree", "Somewhat Agree", "Somewhat Agree", "Agree", "Somewhat Disagree", "Neutral","Somewhat Agree","Somewhat Disagree","Somewhat Agree")
q1 <-c("Somewhat Disagree", "Neutral", "Somewhat Disagree")
q2 <-c("Somewhat Agree","Somewhat Agree","Somewhat Agree")
q3 <-c("Somewhat Agree", "Agree", "Agree")
q4 <-c("Agree","Agree","Agree")
q5 <-c("Agree", "Somewhat Disagree",  "Somewhat Disagree")
q6 <-c("Somewhat Agree", "Somewhat Disagree", "Neutral")
q7 <-c("Somewhat Agree", "Neutral", "Somewhat Agree")
q8 <-c("Agree", "Somewhat Disagree", "Somewhat Disagree")
q9 <-c("Agree", "Agree", "Somewhat Agree")

qq1 <-c("Agree","Somewhat Disagree","Neutral")
qq2<-c("Somewhat Agree","Somewhat Agree","Somewhat Agree")
qq3<-c("Agree","Somewhat Disagree","Agree")
qq4<-c("Agree","Agree","Somewhat Agree")
qq5<-c("Somewhat Agree","Somewhat Disagree","Somewhat Agree")

edf2<-data.frame("Question 1"=qq1,
		"Question 2"=qq2,
		"Question 3"=qq3,
		"Question 4"=qq4,
		"Question 5"=qq5)

edf <- data.frame( "Question 1" = q1,
                   "Question 2" = q2,
                   "Question 3" = q3,
                   "Question 4" = q4,
                   "Question 5" = q5,
                   "Question 6" = q6,
                   "Question 7" = q7,
                   "Question 8" = q8,
                   "Question 9" = q9)

names(edf2)<-c(
	ST24Q01="Question 1",
	ST24Q02="Question 2",
	ST24Q03="Question 3",
	ST24Q04="Question 4",
	ST24Q05="Question 5")

names(edf) <- c(
  ST24Q01="Question 1",
  ST24Q02="Question 2",
  ST24Q03="Question 3",
  ST24Q04="Question 4",
  ST24Q05="Question 5",
  ST24Q06="Question 6",
  ST24Q07="Question 7",
  ST24Q08="Question 8",
  ST24Q09="Question 9")
str(edf)

sapply(edf, class) #Verify that all the columns are indeed factors
sapply(edf2, class)
sapply(edf, function(x) { length(levels(x)) } ) # The number of levels in each factor
sapply(edf2, function(x) {length(levels(x))})
# edf<-lapply(edf, ordered, levels=0:5)
for(i in seq_along(edf)) {
  edf[,i] <- factor(edf[,i], levels=mylevels)
}

for(i in seq_along(edf2)){
	edf2[,i]<-factor(edf2[,i], levels=mylevels)
}
l2 <-likert(edf2)
l24 <- likert(edf)
l24 #print(l24)
summary(l24)
summary(l24, center=1.5)
summary(l24, center=2)
summary(l2)
summary(l2, center=1.5)
summary(l2, center=2)
# xtable
xtable(l24)
# Plots
plot(l24)
pdf('q1plot.pdf')
plot(l24, ordered=FALSE, group.order=names(edf)) #Specify the exact order of the y-axis
xtable(l2)
pdf('q2plot.pdf')
plot(l2, ordered=FALSE, group.order=names(edf2))

dev.off()
