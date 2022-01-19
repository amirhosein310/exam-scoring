import numpy as np
answers = np.array([[0, 1, 1, 1, 1],
                     [0, 4, 4, 4, 4],
                     [0, 2, 0, 3, 1],
                     [0, 3, 3, 3, 3],
                     [0, 1, 1, 4, 0],
                     [0, 2, 4, 2, 2],
                     [0, 6, 4, 0, 4]])

key = np.array([[1],
                     [4],
                     [2],
                     [3],
                     [1],
                     [2],
                     [1]])

students = np.array([[0, 1, 2, 3, 4], #student code
                     [0, 1, 1, 0, 0]])   #gender ,0>>male, 1>>female

lessons = np.array([[1, 2, 3, 4],   #code
                    [0, 2, 3, 5],   #start
                    [2, 3, 5, 7],   #finish
                    [0.4, 0.3, 0.1, 0.2]])  #weight

def rankpos(rank_list, code):
    for i in range(0, len(rank_list)):
        if rank_list[i][1] == code:
            rank = i
    return rank+1

def absence(answer,stulist):
    ab = np.where(~answer.any(axis=0))[0]
    return stulist[0][ab]

def check_input(lessonarr, studentarr, answerarr):

     if int(lessonarr[3].sum()+0.0001) != 1:
         print('error: lessons weights are not equal to 1')
         return 0
     if np.shape(studentarr)[1] != np.shape(answerarr)[1]:
         print('error: answers and students are not equal')
         return 0
     for i in range(0,len(lessons[0])-1):
         if lessonarr[2][i] != lessonarr[1][i+1]:
             print('error 2')
             return 0
         break

def gender_split(ansarr, stuarr):
    ab = np.where(stuarr[1] == 1, answers, -1)
    idx = np.argwhere(np.all(ab == -1, axis=0))
    female_answers = np.delete(ansarr, idx, axis=1)

    ab = np.where(stuarr[1] == 0, answers, -1)
    idx = np.argwhere(np.all(ab == -1, axis=0))
    male_answers = np.delete(ansarr, idx, axis=1)
    return female_answers, male_answers

def lessons_marking(ansarr, keyarr, ls, code, neg):
    lesson_length = int(ls[2, code]) - int(ls[1, code])
    true_answers = ansarr == keyarr
    no_answer = np.count_nonzero(ansarr[int(lessons[1,code]):int(lessons[2,code])]==0)
    wrong_answer = np.count_nonzero(true_answers[int(lessons[1,code]):int(lessons[2,code])]==0) - no_answer
    tr = np.count_nonzero(true_answers[int(lessons[1,code]):int(lessons[2,code])])

    sc = ((tr/lesson_length)*100)-(wrong_answer*33.3*neg/lesson_length)


    return tr/np.shape(ansarr)[1], no_answer/np.shape(ansarr)[1], wrong_answer/np.shape(ansarr)[1], sc/np.shape(ansarr)[1]

def marking(ans, lesson, keyarr, code, neg):
    weighted = []
    score_list = []
    no_answer_list = []
    true_answer_list = []
    wrong_answer_list = []
    a = []
    truearr = ans == keyarr
    for i in range(0,np.shape(lesson)[1]):
        lesson_length = int(lesson[2, i])-int(lesson[1, i])

        t_ans = truearr[int(lesson[1, i]):int(lesson[2, i]), code]
        true_answer_list.append(sum(t_ans))

        no_answer = np.count_nonzero(answers[int(lesson[1,i]):int(lesson[2,i]), code]==0)
        no_answer_list.append(no_answer)

        wrong_answer = np.count_nonzero(truearr[int(lesson[1,i]):int(lesson[2,i]), code]==0) - no_answer
        wrong_answer_list.append(wrong_answer)
        score = (int(sum(t_ans))/(int(lesson[2, i]-int(lesson[1, i])))*lesson[3,i]*100)-(wrong_answer*neg*(33*lesson[3,i]))
        score_list.append(score)
        score = (((sum(t_ans))/lesson_length)*lesson[3,i]*100)-(wrong_answer*33.3*lesson[3,i]*neg/lesson_length)
        weighted.append(score)
    return weighted, true_answer_list, wrong_answer_list, no_answer_list

def total_marking(ans, lesson, std, keyarr, neg):
    total_score_list = []
    for i in range(0,np.shape(std)[1]):
        new_score = [sum(marking(ans, lesson, keyarr, i, neg)[0]), i]
        total_score_list.append(new_score)
        total_score_list.sort(reverse=True)

    return total_score_list


def main():
    print('*'*20,'EXAM MARKING PROGRAM','*'*20)

    if check_input(lessons, students ,answers) == 0:
        exit()

    print('absent students codes', absence(answers, students))

    ne = int(input('enter 1 if exam has negative marking else enter 0: '))

    xla = input('ENTER "i" FOR LESSONS PERFORMANCE REPORT OR "n" FOR STUDENTS REPORT: ')
    if xla == 'i':
        lesson_code = int(input('enter lesson code: '))
        print('(average true answers| average blank answers| average wrong answers| total performance%)')
        print('total performance: ', lessons_marking(answers, key, lessons,lesson_code, ne))
        print('females performance: ', lessons_marking(gender_split(answers, students)[0], key , lessons ,lesson_code, ne))
        print('males performance: ',lessons_marking(gender_split(answers, students)[1], key, lessons, lesson_code, ne))
    elif xla == 'n':
        ranks = total_marking(answers, lessons, students, key, ne)
        std_code = int(input('enter student code: '))
        print('total score in lessons(from 100)|  true answers, wrong answers, blanks')
        print(marking(answers, lessons, key, std_code, ne))
        print('student ranking: ', rankpos(ranks, std_code), 'out of ',np.shape(students)[1])

    command = input('to continue enter i: ')
    if command =='i':
        main()
    else: exit()


main()
















