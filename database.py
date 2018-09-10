class Login:
    def __init__(self):
        self.user = {}
        self.user['test'] = 'test123'
        self.user['admin'] = 'admin'

class Employees():
    def __init__(self):

        self.workers = {}

        try:
            self.file = open('setup.txt', 'r+')
        except:
            self.file = open('setup.txt', 'w')
            self.file.write('LIST OF EMPLOYEES')
            self.add_employee('Test', 'Test')
            self.file.close()
        finally:
            self.file = open('setup.txt', 'r+')

        self.dictWorkers()

    def add_employee(self, name, surname, age=None, birthday=None, extInfo=None):
        # Add employee to dictionary self.workers and to file
        if age == '': age='None'
        if birthday == '' or birthday == 'dd/mm/yyyy': birthday='None'
        if extInfo == '': extInfo='None'
        ret = "\n" + str(name) + ";" + str(surname) + ";" + str(age) + ";" + str(birthday) + ";" + str(extInfo)
        self.file.write(ret)
        self.workers[name + " " + surname] = (age, birthday, extInfo)

    def dictWorkers(self):
        # From file to dict self.workers
        text = self.file.readlines()
        for i in range(1, len(text)):
            self.workers[text[i].split(';')[0] + " " + text[i].split(';')[1]] = (text[i].split(';')[2],
                                                                                 text[i].split(';')[3],
                                                                                 text[i].split(';')[4].replace('\n', ''))
    def delete(self, name):
        # Delete worker from file and dictionary self.workers
        del self.workers[name]
        self.file.truncate(0)
        self.file.write('LIST OF EMPLOYEES')
        for work in self.workers:
            name = work.split(" ")
            sw = self.workers[work]
            self.file.write("\n{};{};{};{};{}".format(name[0],name[1],sw[0],sw[1],sw[2]))

    def close(self):
        self.file.close()


class Notes():
    def __init__(self):

        self.notes = {}

        try:
            self.file = open('notes.txt', 'r+')
        except:
            self.file = open('notes.txt', 'w')
            self.file.close()
        finally:
            self.file = open('notes.txt', 'r+')

    def add_note(self, date, text):
        self.notes[date] = text
        self.file.write(date+";"+text+"\n")


if __name__ == "__main__":
    test = Employees()
    test.delete('test test')
