import os
class directory:
    def __init__(self, round_winner, date, path='/Users/nims/Desktop/CAGMon_LIGO'):
        self.winner = round_winner
        self.date   = date
        self.path   = path if path[-1] == '/' else path + '/'
    def make_directory(self):
        print("Making Directory...")
        if os.path.isdir(self.path + f'{self.date}') == True : pass
        else : os.mkdir(self.path + f'{self.date}')
        print(f"  - {self.path + self.date}/")
        path = self.path + self.date + '/'
        for name in ["round_trigger", "coefficient", "data", "plot"]:
            print(f"  - {path + name}/")
            if os.path.isdir(path + name) == True : pass
            else : os.mkdir(path + name)

            if name == "data":
                for data_type in ["trigger", "normal"]:
                    print(f"  - {path + name}/{data_type}/")
                    if os.path.isdir(path + name + '/' + data_type) == True: pass
                    else :
                        os.mkdir(path + name + '/' + data_type)
    def check_list(self):
        print("Checking files...")
        if os.path.isfile(self.path + 'H1-raw-safe.txt') == True : print("  - H1-raw-safe.txt : True")
        else : print("  - H1-raw-safe.txt : False")

        if os.path.isfile(self.path + f'{self.date}/' + 'round_trigger/'
                          + f'{self.winner}_vetoed_primary_triggers.txt') == True:
            print("  - Round1 trigger list : True")
        else : print("  - Round1 trigger list : False")