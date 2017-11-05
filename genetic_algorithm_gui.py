from tkinter import *
from tkinter import messagebox
import random

# 유틸
class util:
    def rgb2hex(self,r,g,b):
        return '#%02x%02x%02x' % (r,g,b)

# 메인
class main(util):
    def __init__(self,root):
        self.root = root
        root.title('유전 알고리즘')
        root.resizable(0,0)
        self.generation = -1
        self.layout()
        
    def layout(self):
        root = self.root

        #1번째 프레임
        frame = Frame(self.root,height=550)
        frame.grid(row=0,column=0, padx=5, pady = 5,sticky="N")

        #1번째 프레임 위젯
        self.init_btn = Button(frame, text = '속성 초기화',command=lambda:self.initvalue(), width = 20, height = 2)
        self.init_btn.grid(row=0,column=0,pady=5,columnspan=4)
        
        self.l1 = Label(frame,text = '배경색(RGB) : ')
        self.l1.grid(row=1,column=0,pady=5)

        self.ER = Entry(frame, width=4)
        self.ER.grid(row=1,column=1,padx=5)
        self.EG = Entry(frame, width=4)
        self.EG.grid(row=1,column=2,padx=5)
        self.EB = Entry(frame, width=4)
        self.EB.grid(row=1,column=3,padx=5)

        self.l2 = Label(frame,text = '  개체수 : ')
        self.l2.grid(row=2,column=0, pady=5)

        self.Epopulation = Entry(frame, width=4)
        self.Epopulation.grid(row=2,column=1)

        self.l3 = Label(frame,text = '  변이율 : ')
        self.l3.grid(row=3,column=0,pady=5)
        
        self.Emutationrate = Entry(frame, width=4)
        self.Emutationrate.grid(row=3,column=1)

        frame.grid_rowconfigure(4,minsize=30)
    
        self.run_btn = Button(frame, text = '다음세대',command = lambda:self.next(), width = 20, height = 2)
        self.run_btn.grid(row=5,column=0,columnspan=4)

        self.l4 = Label(frame,text = '세대 : ')
        self.l4.grid(row=6,column=0)
        self.Lgeneration = Label(frame,text = 0)
        self.Lgeneration.grid(row=6,column=1,columnspan=3)

        self.l5 = Label(frame,text = '최우수 유전자 : ')
        self.l5.grid(row=7,column=0)
        self.Lbest = Label(frame,text = 0)
        self.Lbest.grid(row=7,column=1,columnspan=3)


         # 캔버스
        self.field = Canvas(root,bg='white', height=550,width=550,)
        self.field.grid(row=0, column=1, columnspan = 1, padx=5,pady=5)

        self.position = list()
        
        for i in range(0,10):
            for f in range(0,10):
                x = 50*f + 5*(f+1)
                y = 50*i + 5*(i+1)
                self.position.append([x,y])

        # 네임
        bottom = Frame(self.root)
        bottom.grid(row=1, column=0, columnspan = 2)
        self.l6 = Label(bottom,text = '김민석 제작 kcal2845')
        self.l6.grid(row=0,column=0)

    def initvalue(self):
       # try:
        # 배경색초기화
            r = int(self.ER.get())
            g = int(self.EG.get())
            b = int(self.EB.get())
            self.target = [r,g,b]
            self.bg = self.rgb2hex(r,g,b)
            self.field.configure(background=self.bg)

            # 속성 초기화
            self.mutationrate = int(self.Emutationrate.get())
            self.population = int(self.Epopulation.get())

            
            # 초기 유전자 설정
            self.initgene()

            # 무작위 위치로 개체 그리기
            self.drawrandom()
            
            self.generation = 0
            self.Lgeneration.config(text = self.generation)

        #except:
        #    self.generation = -1


    def initgene(self):
        # 초기 유전자 설정
        self.genes = list()
        for i in range(0,self.population):
            self.genes.append([random.choice(range(0,256)) for _ in range(3)])
            
    def next(self):
        if(self.generation <0):
            messagebox.showinfo('메세지', '속성값을 먼저 초기화해주세용~')
            return

        self.generation = self.generation +1 # 세대 올림
        self.Lgeneration.config(text = self.generation)
        # 선택
        parents = self.select()
        self.Lbest.config(text = str(parents[0]))
        # 교차
        crossovered = self.crossover(parents)

        # 변이
        mutated = self.mutation(crossovered)
        
        # 대치
        self.genes = mutated

        self.drawrandom()


    def drawrandom(self):

        # 배경원 초기화
        
        for i in range(0,len(self.position)):
                x = self.position[i][0]
                y = self.position[i][1]
                self.field.create_oval(x,y,x+50,y+50,fill=self.bg, outline=self.bg)
                
        # 무작위 위치로 개체 그리기
        randpos = self.position
        random.shuffle(randpos)
        
        for i in range(0,self.population):
            x = randpos[i][0]
            y = randpos[i][1]
            r = self.genes[i][0]
            g = self.genes[i][1]
            b = self.genes[i][2]
            self.field.create_oval(x,y,x+50,y+50,fill=self.rgb2hex(r,g,b))

    def select(self):
        genes = self.genes
        population = self.population
        target = self.target

        parents = list()
        fitness = list()
        
        for i in range(0,population):
            fitness.append(0)
        
            # 타겟 유전자와 비교
            for f in range(0,3):
                if(genes[i][f] != target[f]):
                    fitness[i] = fitness[i] + abs(target[f] - genes[i][f])

        # 적합도가 낮은 번호 부터 순위
        rank = sorted(range(population), key = lambda k: fitness[k])
        
        for i in range(0,population):
            parents.append(genes[rank[i]])
        
        parents = parents[0:int(population/2)]
        
        return parents

    def crossover(self, parents):
        
         population = self.population
         genes = self.genes
         
         for i in range(0,population):
            selected = list()
            # 리스트 두개 랜덤으로 고름
            selected = random.sample(parents,2)

            # 랜덤으로 부모유전자 물려받음
            for f in range(0,3):
                if(random.choice(range(0,2)) == 0):
                    genes[i][f] = selected[0][f]
                else:
                    genes[i][f] = selected[1][f]
                    
         return genes
        
    def mutation(self,genes):

        population = self.population
        mutationrate = self.mutationrate
        
        for i in range(0,population):
            for f in range(0,3):

                if(random.randrange(0,mutationrate) == 0):
                    # 원래 유전자값을 제외한 값만 랜덤으로 고르기
                    lst = list(filter( lambda x: x != genes[i][f], list( range(0,256) )))
                    genes[i][f] = random.choice(lst)

        return genes
            
        
window = Tk()
main(window)
window.mainloop()
