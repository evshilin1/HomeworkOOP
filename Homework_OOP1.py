class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            print('Ошибка: можно оценивать только лекторов')
            return
        if course not in self.courses_in_progress:
            print('Ошибка: студент не изучает этот курс')
            return
        if course not in lecturer.courses_attached:
            print('Ошибка: лектор не читает этот курс')
            return
        if not 1 <= grade <= 10:
            print('Ошибка: оценка должна быть от 1 до 10')
            return

        if course in lecturer.grades:
            lecturer.grades[course].append(grade)
        else:
            lecturer.grades[course] = [grade]

    def __str__(self):
        avg_grade = self.calculate_average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else "Нет активных курсов" #conditional expression увидел генератор в одну строку на лекции - решил изучить и использовать только с условным оператором
        finished_courses = ', '.join(self.finished_courses) if self.finished_courses else "Нет завершенных курсов"
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {avg_grade:.1f}\nКурсы в процессе изучения: {courses_in_progress}\nЗавершенные курсы: {finished_courses}"

    def calculate_average_grade(self):
        if not self.grades:
            return 0.0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades)

    def __lt__(self, other):
        if not isinstance(other, Student):#Посмотрел в документации про проверку отношения объекта к классу, далее в программе часто использую для чистоты кода
            return NotImplemented
        return self.calculate_average_grade() < other.calculate_average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_average_grade() == other.calculate_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self.calculate_average_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade:.1f}"

    def calculate_average_grade(self):
        if not self.grades:
            return 0.0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.calculate_average_grade() < other.calculate_average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.calculate_average_grade() == other.calculate_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            print('Ошибка: можно оценивать только студентов')
            return
        if course not in self.courses_attached:
            print('Ошибка: проверяющий не прикреплен к этому курсу')
            return
        if course not in student.courses_in_progress:
            print('Ошибка: студент не изучает этот курс')
            return

        if course in student.grades:
            student.grades[course].append(grade)
        else:
            student.grades[course] = [grade]

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def calculate_avg_hw_grade(students, course):
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    if not total_grades:
        return 0.0
    return sum(total_grades) / len(total_grades)


def calculate_avg_lecture_grade(lecturers, course):
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    if not total_grades:
        return 0.0
    return sum(total_grades) / len(total_grades)


# Создаем экземпляры классов
student1 = Student('Elisey', 'Shilin', 'male')
student1.courses_in_progress = ['Python', 'Git']
student1.finished_courses = ['Введение в программирование']

student2 = Student('NotElisey', 'NotShilin', 'female')
student2.courses_in_progress = ['Python', 'Java']
student2.finished_courses = ['Основы ООП']

lecturer1 = Lecturer('Some', 'Buddy')
lecturer1.courses_attached = ['Python', 'Git']

lecturer2 = Lecturer('Another', 'SomeBuddy')
lecturer2.courses_attached = ['Python', 'Java']

reviewer1 = Reviewer('Harry', 'Potter')
reviewer1.courses_attached = ['Python', 'Git']

reviewer2 = Reviewer('John', 'Smith')
reviewer2.courses_attached = ['Python', 'Java']

# Оцениваем студентов
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student1, 'Git', 10)
reviewer2.rate_hw(student2, 'Python', 7)
reviewer2.rate_hw(student2, 'Java', 9)

# Оцениваем лекторов
student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Git', 9)
student2.rate_lecture(lecturer2, 'Python', 8)
student2.rate_lecture(lecturer2, 'Java', 7)

# Выводим информацию
print("Студенты:")
print(student1)
print()
print(student2)
print("\nЛекторы:")
print(lecturer1)
print()
print(lecturer2)
print("\nПроверяющие:")
print(reviewer1)
print()
print(reviewer2)

# Сравниваем студентов и лекторов
print("\nСравнение студентов:")
print(f"{student1.name} < {student2.name}: {student1 < student2}")
print(f"{student1.name} == {student2.name}: {student1 == student2}")

print("\nСравнение лекторов:")
print(f"{lecturer1.name} < {lecturer2.name}: {lecturer1 < lecturer2}")
print(f"{lecturer1.name} == {lecturer2.name}: {lecturer1 == lecturer2}")

# Подсчет средних оценок по курсу
python_students_avg = calculate_avg_hw_grade([student1, student2], 'Python')
python_lecturers_avg = calculate_avg_lecture_grade([lecturer1, lecturer2], 'Python')

print("\nСредние оценки по курсу Python:")
print(f"Средняя оценка студентов за домашние задания: {python_students_avg:.1f}")#Округление до одного знака после запятой
print(f"Средняя оценка лекторов за лекции: {python_lecturers_avg:.1f}")