import Master
import DataBase

def makebbs2mongo():
    m = Master.Master_Spider()
    datalist = m.mainbbs_parse()
    a = DataBase.Data2Mongo("qichezhijia", "mainbbs_carlink")
    a.inserdata(datalist)



if __name__ == '__main__':
    pass


