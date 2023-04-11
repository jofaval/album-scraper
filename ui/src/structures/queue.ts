export interface QueueJob {
  run: () => void;
}

export interface QueueProps<T extends QueueJob> {
  initialHighPriorityItems?: Map<number, T>;
  initialLowPriorityItems?: Map<number, T>;
  startProcessing?: boolean;
  startOnInit?: boolean;
}

const sleep = async (ms: number | undefined) => {
  new Promise((resolve) => setTimeout(resolve, ms));
};

export class Queue<T extends QueueJob> {
  static CHECK_IF_PROCESSING_IN_MILLISECONDS_EVERY = 50;
  static CHECK_FOR_NEW_ITEMS_IN_MILLISECONDS_EVERY = 50;
  static DEBUG = false;

  static instance: Queue<QueueJob>;

  // TODO: refactor into LinkedLists?
  lowPriority: Map<number, T>;
  // TODO: refactor into LinkedLists?
  highPriority: Map<number, T>;
  /** Private jobId tracker */
  _jobId = Number.MIN_SAFE_INTEGER;
  /** Is the queue running? */
  processing = false;

  constructor({
    startProcessing = false,
    initialHighPriorityItems,
    initialLowPriorityItems,
    startOnInit = false,
  }: QueueProps<T> = {}) {
    this.lowPriority = new Map<number, T>();
    if (
      initialLowPriorityItems &&
      initialLowPriorityItems instanceof Map<number, T>
    ) {
      for (const [key, value] of initialLowPriorityItems.entries()) {
        this.lowPriority.set(key, value);
      }
    }

    this.highPriority = new Map<number, T>();
    if (
      initialHighPriorityItems &&
      initialHighPriorityItems instanceof Map<number, T>
    ) {
      for (const [key, value] of initialHighPriorityItems.entries()) {
        this.highPriority.set(key, value);
      }
    }

    if (startOnInit) {
      this.start();
    }

    if (startProcessing) {
      const thisQueue = this;
      // parallel job
      setTimeout(function () {
        thisQueue.process();
      }, 0);
    }
  }

  _processJobFromQueue(queue: Map<number, T>): boolean {
    const jobKey = queue.keys().next().value;
    if (!jobKey) {
      return false;
    }

    const element = queue.get(jobKey);
    if (!element) {
      return false;
    }

    try {
      element.run();
    } catch (error) {
      if (Queue.DEBUG) {
        console.error(error);
      }
    } finally {
      queue.delete(jobKey);
    }

    return true;
  }

  process() {
    const thisQueue = this;

    (async function () {
      while (true) {
        await sleep(Queue.CHECK_IF_PROCESSING_IN_MILLISECONDS_EVERY);
        if (Queue.DEBUG) {
          console.info("Checking for a new processing status");
        }

        while (thisQueue.processing) {
          const couldRunJob =
            thisQueue._processJobFromQueue(thisQueue.highPriority) ||
            thisQueue._processJobFromQueue(thisQueue.lowPriority);

          if (!couldRunJob) {
            await sleep(Queue.CHECK_FOR_NEW_ITEMS_IN_MILLISECONDS_EVERY);
            if (Queue.DEBUG) {
              console.info("Checking for new items");
            }
          }
        }
      }
    })();
  }

  static getInstance() {
    if (!Queue.instance) {
      Queue.instance = new Queue();
    }

    return Queue.instance;
  }

  jobAdded() {
    this._jobId++;
    return this._jobId;
  }

  enqueue(element: T): number {
    const jobId = this.jobAdded();
    this.lowPriority.set(jobId, element);

    return jobId;
  }

  priorityEnqueue(element: T): number {
    const jobId = this.jobAdded();
    this.highPriority.set(jobId, element);

    return jobId;
  }

  dequeue(jobId: number): boolean {
    if (this.isJobHighPriority(jobId)) {
      const previousSize = this.highPriority.size;
      this.highPriority.delete(jobId);
      return this.highPriority.size !== previousSize;
    }

    if (this.isJobLowPriority(jobId)) {
      const previousSize = this.lowPriority.size;
      this.lowPriority.delete(jobId);
      return this.lowPriority.size !== previousSize;
    }

    return false;
  }

  start(): void {
    this.processing = true;
  }

  stop(): void {
    this.processing = false;
  }

  isJobHighPriority(jobId: number): boolean {
    return this.highPriority.has(jobId);
  }

  isJobLowPriority(jobId: number): boolean {
    return this.lowPriority.has(jobId);
  }

  hasJobId(jobId: number): boolean {
    return this.isJobHighPriority(jobId) || this.isJobLowPriority(jobId);
  }

  /** Rebuilds the jobIds to use previously unused indices */
  defragment() {
    // TODO: implement
  }
}

interface ExampleJob extends QueueJob {
  helloWorld: string;
}

const queue = new Queue<ExampleJob>({ startProcessing: true });
queue.enqueue({
  helloWorld: "",
  run() {
    console.log("hello world!");
  },
});
queue.priorityEnqueue({
  helloWorld: "important!!",
  run() {
    console.log("HIGH PRIORITY!");
  },
});
queue.start();
queue.stop();
