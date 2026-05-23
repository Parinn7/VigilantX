import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

second_to_run = 30


alerts = []
class OnMyWatch:
    
    watchDirectory = "test_files/" 
    
    def __init__(self):
        self.observer = Observer()

    def run(self):
        start_time = time.time()
        print("🔍 IntegrityX started watching...")
        print(f"   Watching: {self.watchDirectory}")
        print(f"   Duration: {second_to_run} seconds\n")
    
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
    
        try:
            while (time.time() - start_time) <= second_to_run:
                pass
        except Exception as e:
            print(f"Error: {e}")
            self.observer.stop()
            print("Observer Stopped")
    
        print(f"\n Monitoring finished after {second_to_run} seconds")
        self.observer.stop()
        self.observer.join()

        count = 0
        for alert in alerts:
            count += 1

        if count >= 10 :
            ransomware_alert = {
                "type": "RANSOMWARE",
                "file_affected": [a['filename'] for a in alerts],
                "count": count,
                "start_time":alerts[0]['timestamp']
            }
            alerts.append(ransomware_alert)
        return alerts
class Handler(FileSystemEventHandler):

    
    @staticmethod
    def on_any_event(event):
        
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            
            alert = {
    "filename": event.src_path,
    "event_type": "created",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "raw_time" : time.time()
}
            alerts.append(alert)
            
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            alert = {
    "filename": event.src_path,
    "event_type": "modified",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "raw_time" : time.time()
            }
            alerts.append(alert)
        elif event.event_type == 'deleted':
            alert = {
                "filename": event.src_path,
                "event_type" : "deleted",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "raw_time" : time.time()
            }
            alerts.append(alert)
        elif event.event_type == 'rename':
            alert = {
                "filename": event.src_path, 
                "event_type" : "rename",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "raw_time" : time.time()
            }

            
            
            alerts.append(alert)

if __name__ == '__main__':
    watch = OnMyWatch()
    alerts = watch.run()

    for alert in alerts:
        if alert.get('type') == 'RANSOMWARE':
            print(f" RANSOMWARE DETECTED!")
            print(f"   Files affected: {alert['count']}")
            print(f"   Started at: {alert['start_time']}")
        else:
            print(f" {alert['event_type'].upper()}")
            print(f"   File: {alert['filename']}")
            print(f"   Time: {alert['timestamp']}\n")

