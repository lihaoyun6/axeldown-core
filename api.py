import os, shutil, subprocess, time, urlparse, json, datetime, json, sys
import logging as log
import db, config

config_file = open("conf", "rb")
conf = config.Config(json.load(config_file))
config_file.close()

STATE_WAITING=1
STATE_DOWNLOADING=2
STATE_PAUSED=3
STATE_COMPLETED=4
STATE_ERROR=5

class APIError(Exception):
    ERROR_REQUEST_DATA_INVALID = 11
    
    messages = {
        ERROR_REQUEST_DATA_INVALID: 'request data invalid',
    }
    
    def __init__(self, code):
        self.errno = code
        self.message = self.messages[code]

class API(object):
    def __init__(self, curdir='.'):
        self.workdir = os.path.abspath(curdir)
    
    def serve(self, data):
        try:
            action = data['action']
            if action == 'tasks':
                options = data["options"] if data.has_key("options") else {}
                ret = self.tasks(options)
            elif action == 'pause':
                ids = data["ids"]
                ret = self.pause(ids)
            elif action == 'remove':
                ids = data["ids"]
                ret = self.remove(ids)
            elif action == 'create':
                options = data["options"]
                ret = self.create(options)
            elif action == 'cconfig':
                options = data["options"]
                ret = self.cconfig(options)
            elif action == 'resume':
                ids = data["ids"]
                for tid in ids:
                    ret = self.resume(tid)
                else:
                    return dict(success=True, result="")
            elif action == 'sort':
                ids = data["ids"]
                ret = self.sort(ids)
            elif action == 'maxspeed':
                tid = data["tid"]
                ret = self.maxspeed(tid);
            elif action == "config":
                conf = data["config"]
                ret = self.config(conf)
            elif action == "rconfig":
                ret = self.rconfig()
            else:
                raise APIError(APIError.ERROR_REQUEST_DATA_INVALID)
            
            if ret is None:
                return dict(success=True)
            return dict(success=True, result=ret)
        except KeyError:
            import traceback; traceback.print_exc()
            raise APIError(APIError.ERROR_REQUEST_DATA_INVALID)
        except APIError, e:
            return dict(success=False, errno=e.errno, errmsg=e.message)
        except Exception, e:
            # TODO log error
            import traceback; traceback.print_exc()
            return dict(success=False, errno=0, errmsg="unkown error, please check out the log")

    def download_last(self):
      tasks = db.select_tasks(state=STATE_DOWNLOADING)
      for task in tasks:
        log.debug('start to download %s' % task['id'])
        self._start(task['id'])
      self.download_more()

    def download_more(self):
      tasks = db.select_tasks(state=STATE_DOWNLOADING)
      if len(tasks) < conf.task_queue_size:
        tasks = db.select_tasks(state=STATE_WAITING)
        for task in tasks:
          log.debug('start to download %s' % task['id'])
          self._start(task['id'])

    def create(self, options):
        # just create a new task and then load_more()
        url = options["url"]
        output = options["output"] if options.has_key("output") and options["output"] else \
            os.path.basename(urlparse.urlparse(url)[2])
        if not options.has_key("immediately") or options["immediately"]: state = STATE_WAITING
        else: state = STATE_PAUSED
        thsize = options["thsize"] if options.has_key("thsize") else conf.default_thread_size
        if not thsize.strip():
          thsize = conf.default_thread_size
        maxspeed = options["maxspeed"] if options.has_key("maxspeed") else 0
        headers = options["headers"] if options.has_key("headers") else ""
        #subdir = options["subdir"] if options.has_key("subdir") else ""
        conf.downloads = os.path.expanduser(conf.downloads)
        downloads = options["downloads"] if options.has_key("downloads") else conf.downloads
        downloads = os.path.expanduser(downloads)
        if not downloads.strip():
          downloads = conf.downloads
        ua = options["ua"] if options.has_key("ua") else conf.user_agent
        if not ua.strip():
          ua = conf.user_agent
        tid = db.insert_task(url=url, output=output, state=state, thsize=thsize, maxspeed=maxspeed, headers=headers, downloads=downloads, ua=ua)

        if state == STATE_WAITING:
            self.download_more()
            
    def cconfig(self, options):
      with open('conf', 'w') as conf_file:
        json.dump(options, conf_file)
        
    def rconfig(self):
      with open('conf', 'r') as f:
        data = json.load(f)
        return data

    def _start(self, tid):
        # start a task existed
        tasks = db.select_tasks(id=tid)
        if not tasks:
            return

        db.update_tasks(tid, state=STATE_DOWNLOADING)

        #create axel task
        #print "====="
        #print os.fork()
        if os.fork(): # old process
            return # as 200 OK
        else: # sub process
            # get the options
            task = tasks[0]
            url = task["url"]
            output = task["output"]
            thsize = task["thsize"]
            maxspeed = task["maxspeed"]
            headers = task["headers"]
            #subdir = task["subdir"]
            downloads = task["downloads"]
            ua = task["ua"]

            force_download = conf.force_download
            output_file = os.path.join(downloads, output)
            if os.path.exists(output_file) and not os.path.exists(output_file + '.st'):
              if force_download:
                os.remove(output_file)
              else:
                print 'file completed already, skip download'
                exit()
            os.system("mkdir -p %s" % os.path.join(downloads))
            args = [os.path.join(os.getcwd(), "axel"), "-a", "-n", str(thsize), "-s", str(maxspeed), "-U", str(ua)]
            for header in headers.splitlines():
                args.append("-H")
                args.append(header)
            args.append("-o")
            args.append(output_file)
            args.append(url)
            axel_process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, cwd=downloads)
            #print(args)

            last_update_time = 0
            while 1:
                try:
                    line = axel_process.stdout.readline()
                    if not line:
                      break
                    line = line.strip()
                except:
                    returncode = axel_process.poll()
                    if returncode is not None:
                        # axel completed
                        if returncode:
                            db.update_tasks(tid, state=STATE_ERROR, errmsg="Error, axel exit with code: %s" % returncode)
                    break
                this_update_time = time.time()
                if line.startswith(":"):
                    done, total, thdone, speed, left, update_time = line[1:].split("|")
                    if done != total and last_update_time > 0 and this_update_time - last_update_time < 1:
                        continue
                elif line.startswith("HTTP/1."):
                    db.update_tasks(tid, state=STATE_ERROR, errmsg=line)
                    break
                else:
                    continue
                last_update_time = this_update_time
                tasks = db.select_tasks(id=tid)
                if tasks:
                    task = tasks[0]
                    state = task["state"]
                    if state == STATE_DOWNLOADING:
                        try:
                            if done == total:
                                #completed
                                db.update_tasks(tid, state=STATE_COMPLETED, left=0)
                                os.system("mkdir -p %s" % os.path.join(downloads))
                                #os.rename(output_file, os.path.join(conf.downloads, subdir, output))
                                break
                            db.update_tasks(tid, speed=speed, done=done, total=total, left=left)
                            continue
                        except Exception, e:
                            import traceback
                            traceback.print_exc()
                            db.update_tasks(tid, state=STATE_ERROR, errmsg="Error, axel exit with code: %s" % e)
                            try:
                                axel_process.terminate()
                            except:
                                pass
                    else:
                        #paused
                        axel_process.terminate()
                else:
                    #deleted
                    axel_process.terminate()
                    try:
                        os.remove(output_file)
                    except:
                        pass
                    try:
                        os.remove(output_file + ".st")
                    except:
                        pass
            returncode = axel_process.poll()
            if returncode is not None:
                # axel completed
                if returncode:
                    db.update_tasks(tid, state=STATE_ERROR, errmsg="Error, axel exit with code: %s" % returncode)
            self.download_more()
            sys.exit()

    def resume(self, tid):
        # set state to waiting and load_more()
        tid = int(tid)
        tasks = db.select_tasks(id=tid)
        if tasks:
            task = tasks[0]
            url = task["url"]
            output = task["output"]
            state = task["state"]
            thsize = task["thsize"]
            maxspeed = task["maxspeed"]
            headers = task["headers"]
            #subdir = task["subdir"]
            downloads = task["downloads"]
            ua = task["ua"]
            if state not in (STATE_WAITING, STATE_PAUSED, STATE_ERROR):
                return
            if state != STATE_WAITING:
                db.update_tasks(tid, state=STATE_WAITING)
            self.download_more()

    def tasks(self, options):
        tasks = db.select_tasks(**options)
        for task in tasks:
          if task['state'] == STATE_DOWNLOADING and task['update_time'] and task['speed']:
            nowt = datetime.datetime.now()
            parts = task['update_time'].split('.')
            dt = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
            update_time = dt.replace(microsecond=int(parts[1]))
            interval = nowt - update_time
            interval_seconds = interval.seconds + interval.microseconds*1.0/1000/1000
            if interval_seconds > 2 and interval_seconds * task['speed'] > conf.buffer_size:
              speed = conf.buffer_size * 1.0 / interval_seconds
              task['speed'] = 0 if speed < 1024 else speed
        return tasks

    def pause(self, ids):
        db.update_tasks(ids, **{'state': STATE_PAUSED})

    def remove(self, ids):
        db.delete_tasks(ids)

    def sort(self, ids):
        orders = []
        for order in range(len(ids)):
            db.update_tasks(ids[order], **{'order':order}) 

    def maxspeed(self, tid):
        return 0
        if not conf.total_maxspeed:
            return 0
        if not conf.total_max:
            return 0
        tasks = db.select_tasks(state="!=5")
        total_speed = 0
        for task in tasks:
            if task['id'] == tid:
                continue
            speed = task['speed']
            if speed:
                total_speed += task['speed']
        if total_speed > conf.total_max:
            return 1
        else:
            return conf.total_max - total_speed
    
    def config(self, conf):
        try:
            dict_conf = json.loads(conf)
            conf = json.dumps()
        except:
            raise APIError(ERROR_REQUEST_DATA_INVALID)
        with open('conf', 'wb') as configfile:
            configfile.write(conf)

