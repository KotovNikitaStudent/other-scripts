#include <QCoreApplication>
#include <QDebug>
#define TIME_LIMIT 10000
#define QUEUE_LIMIT 3
#define THREAD_COUNT 3

class TQuery{
public:
    int id,timeStart,timeLength;
};

// поток обработки заявок
class TThread{
public:
    int qid; // идентификатор заявки
    int len; // сколько тиков осталось до конца заявки
};

int main(int argc, char *argv[])
{
    QList<TQuery> list;
    int time = 0;
    int id = 0;
    int taskFailed = 0;
    int taskTotal = 0;
    while(time < TIME_LIMIT){
        TQuery query;
        time+=rand() % 1000+100;
        query.id = ++id;
        query.timeStart = time;
        query.timeLength = rand() % 10;
        ++taskTotal;
        list.append(query);
    }
    for(QList<TQuery>::const_iterator i = list.cbegin(); i<list.cend(); ++i){
        qDebug() << "Start " << i->timeStart << " length " << i->timeLength;
    }
    QList<TQuery>queue;
    QList<TThread>threads;
    for(int i = 0; i<THREAD_COUNT; ++i){
        TThread t;
        t.qid = -1;
        threads.append(t);
    }
    int listPos = 0;
    for(int tick = 0; tick < TIME_LIMIT; ++tick){
        // заявка в очередь
        if(listPos < list.length()){
            if(list[listPos].timeStart > tick){
                if(queue.length() < QUEUE_LIMIT){
                    queue.push_front(list[listPos]);
                    qDebug() << "Task queued " << list[listPos].id;
                    ++listPos;
                }else{
                    qDebug() << "Task failed " << list[listPos].id;
                    ++taskFailed;
                    ++listPos;
                }
            }
        }
        // проверяем, что есть свободный поток
        for(int th=0; th<threads.count(); ++th){
            // проверяем, есть ли кто в очереди
            if(queue.length() > 0 && threads[th].qid < 0){
                TQuery q = queue[queue.length()-1];
                queue.pop_back();
                threads[th].qid = q.id;
                threads[th].len = q.timeLength;
                qDebug() << "Task threaded " << q.id;
            }
        }
        // каждый поток обрабатывает свою заявку
        for(int th=0; th<threads.count(); ++th){
            if(threads[th].qid >= 0){
                if(--threads[th].len <= 0){
                    // задача завершена
                    qDebug() << "Task finished " << threads[th].qid;
                    threads[th].qid = -1;
                }
            }
        }
    }
    return 0;
}
