class Student:
    top_student=''
    top_student_average=0

    def __init__(self,name,scores=None):
        self.name=name
        if(scores is None):
            self.scores=[]
        else:
            self.scores=scores
    def addScore(self,marks):
        self.scores.append(marks)
    def average_marks1(self):
        average_marks= sum(self.scores)/len(self.scores)
        if average_marks>Student.top_student_average:
            Student.top_student_average=average_marks
            Student.top_student=self.name
        return average_marks    
    def __str__(self):
        return f"The student {self.name} with average {self.average_marks1()}"

if __name__ =='__main__':
    s1=Student("Sumanth")
    s1.addScore(20)
    s1.addScore(30)
    s1.addScore(40)
    s2=Student("Bhjarath")
    s2.addScore(50)
    s2.addScore(67)
    print(s1)
    print(s2)
    print(Student.top_student)
    
    