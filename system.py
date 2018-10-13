import random
import simpy
import math
#from .queue import Queue
from collections import deque

class Queue():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''
    def __init__(self, max_size = 10):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''

        self._queue = deque(maxlen=max_size)


    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''

        self._queue.append(item)


    def dequeue(self):
        '''
        Dequeues (i.e., removes) the item at the head of this queue *and*
        returns this item.

        Raises
        ----------
        IndexError
            If this queue is empty.
        '''

        return self._queue.pop()

class Process():
    def __init__(self, *args, **kwargs):
        self.gap_time = self.ExponentialRandom(1)
        self.process_time = 0
        self.exit_time = 0
        self.state = 1000
        self._timeArriveInQueue = 0
        self.random = random.seed(315)
    
    def ExponentialRandom(self, rate):
        return (-math.log10(random.random())/(rate))
    
    def SetRuntime(self):
        self.process_time = self.ExponentialRandom(1.2)


class System():
    def __init__(self, size):
        self._outerProcessesQueue = Queue(size)
        self.SetQueue(size)    
        print(self._outerProcessesQueue)
        self._outerSize = size
        self._nextProcessToInput = self._outerProcessesQueue.dequeue()
        self._serverQueue = Queue(size)
        self._clock = 0
        self._tmpclock = 0
        self._totalDelay = 0
        self._serverEndTime = 0
        self._numberInQueue = 0
        self._tmpNumberInQueue = 0
        self._customersInQueue = 0
        self._serverStatus = 0
        self._totalNumberInQueue = 0
        #self._nextEvent = 'InputOuterEvents'
        self._nextEvent = ''
        self._served = 0
        self._Wq = 0
        self._W = 0
        self._serviceTime = 0
        self._Es = 0
        self._Lq = 0
        self._Ro = 0
        self._Bt = 0
        self._L = 0
        self.Print()
        self.Main(size)

    def SetQueue(self, size):
        i = 0
        queue = Queue()
        for i in range(0, size):
            process = Process()
            self._outerProcessesQueue.enqueue(process)
            i+=1
        print('in set Queue and i : '+ str(i))

    def Server(self, process):
        print('in the server')
        self._totalDelay+=(self._clock - process._timeArriveInQueue)
        process.SetRuntime()
        self._serviceTime+=process.process_time
        self._serverEndTime = self._clock + process.process_time
        self._serverStatus = 'full'
        self._served = self._served + 1

    def SetNextEvent(self):
        if self._numberInQueue>0 and self._serverStatus == 'free':
            self._nextEvent = 'InputProcessToServer'
        elif self._nextProcessToInput.gap_time + self._clock > self._serverEndTime and self._numberInQueue>0:
            self._clock=self._serverEndTime
            self._nextEvent = 'InputProcessToServer'
        elif self._nextProcessToInput.gap_time + self._clock < self._serverEndTime:
            self._clock+=self._nextProcessToInput.gap_time
            self._nextEvent = 'InputOuterEvents'
        else: 
            self._clock+=self._nextProcessToInput.gap_time
            self._nextEvent = 'InputOuterEvents'
        if self._clock < self._serverEndTime:
            self._serverStatus = 'full'
        else:
            self._serverStatus = 'free'

    def Print(self):
        print('served: '+str(self._served))
        print('totaldelay: ' + str(self._totalDelay))
        print('number in queue: ' + str(self._numberInQueue))
        print('next process to input time: ' + str(self._clock + self._nextProcessToInput.gap_time))
        print('server end time: ' + str(self._serverEndTime))
        print('next_event: '+ self._nextEvent)
        print('--------------------------------------------------------')

    def Main(self, size):
        i = 0
        j = 0
        for j in range(0, size+size):
            self.SetNextEvent()
            self._totalNumberInQueue+=self._numberInQueue
            if self._nextEvent == 'InputOuterEvents':
                #self._clock = self._nextProcessToInput.gap_time + self._clock
                if self._outerSize > 2:
                    self._numberInQueue = self._numberInQueue + 1
                    self._customersInQueue += (self._tmpNumberInQueue) * (self._clock - self._tmpclock)
                    self._tmpclock = self._clock
                    self._tmpNumberInQueue = self._numberInQueue
                    self._nextProcessToInput._timeArriveInQueue = self._clock
                    self._serverQueue.enqueue(self._nextProcessToInput)
                    self._nextProcessToInput = self._outerProcessesQueue.dequeue()
                    self._outerSize-=1
                else: continue
            else:
                self.Server(self._serverQueue.dequeue())
                self._numberInQueue = self._numberInQueue - 1
                self._customersInQueue += (self._tmpNumberInQueue) * (self._clock - self._tmpclock)
                self._tmpclock = self._clock
                self._tmpNumberInQueue = self._numberInQueue
                i+=1
            self.Print()
            print('i: '+str(i))
            if(i == size-2):
                return
        return
            

system = System(40000)
system._Wq = system._totalDelay/system._served
system._Es = system._serviceTime/system._served
system._W = system._Wq + system._Es
Qt = system._numberInQueue/system._served
system._Lq = system._customersInQueue/system._clock
print('Wq: ' + str(system._Wq))
print('Es: ' + str(system._Es))
print('W: ' + str(system._W))
print('Lq: ' + str(system._Lq))





