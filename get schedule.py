def find_talk_session_time(guest_availabilities, min_duration=2):
    all_intervals = []
    
    for guest, intervals in guest_availabilities.items():
        for start, end in intervals:
            all_intervals.append((start, 'start', guest))  
            all_intervals.append((end, 'end', guest))    

    all_intervals.sort(key=lambda x: (x[0], x[1] == 'end'))

    max_guests = 0
    session_interval = None
    guest_indices = []  
    active_guests = set()  

    for i in range(len(all_intervals)):
        start_time = all_intervals[i][0]
        
        end_time = start_time + min_duration
        
        active_guests.clear()

        for guest, intervals in guest_availabilities.items():
            is_available = False
            for interval_start, interval_end in intervals:
                if interval_start <= start_time and interval_end >= end_time:
                    is_available = True
                    break
            
            if is_available:
                active_guests.add(guest)
        
        guest_count_in_window = len(active_guests)
        
        if guest_count_in_window > max_guests:
            max_guests = guest_count_in_window
            session_interval = (start_time, end_time)
            guest_indices = list(active_guests)

    return session_interval, guest_indices

def create_schedules(guest_availabilities):
    guest_schedule = {}
    
    interval_size={}
    all_intervals=[]
    
    time_spot=[]

    for guest in guest_availabilities:
        time = 0
        for i in guest_availabilities[guest]:
            time += i[1]-i[0]
        interval_size.update({guest:time})
    
    for guest, intervals in guest_availabilities.items():
        for start, end in intervals:
            all_intervals.append((interval_size[guest], start, end, guest))
            
    all_intervals.sort(key=lambda x: (x[0], x[1], x[2]))
    
    for i in all_intervals:
        if i[3] not in guest_schedule:
            for j in range(i[1],i[2]):
                if j not in time_spot:
                    guest_schedule.update({i[3]:(j,j+1)})
                    time_spot.append(j)
                    
    return guest_schedule

def modify_availabilities(guest_availabilities, talk_session):
    start = talk_session[0]
    end = talk_session[1]
    
    for guest in guest_availabilities:
        for i in guest_availabilities[guest]:
            if i[0]<start and i[1]>end:
                guest_availabilities[guest].append((i[0],start))
                guest_availabilities[guest].append((end,i[1]))
                guest_availabilities[guest].remove(i)
            elif start<=i[0]<=end:
                guest_availabilities[guest].append((end,i[1]))
                guest_availabilities[guest].remove(i)
            elif start<=i[1]<=end:
                guest_availabilities[guest].append((i[0],start))
                guest_availabilities[guest].remove(i)
    for guest in guest_availabilities:
        sorted(guest_availabilities[guest], key=lambda x: x[0])

def get_schedule(guest_availabilities):
    talk_session, guest_indices = find_talk_session_time(guest_availabilities)
    
    modify_availabilities(guest_availabilities, talk_session)
    
    guest_schedule = create_schedules(guest_availabilities)
    
    print(f"The Talk Session will be held between {talk_session[0]} and {talk_session[1]}")

    for i in range(len(guest_availabilities)):
        if i not in guest_schedule:
            print(f"Guest {i} will not speak")
        else:
            print(f"Guest {i} will speak between {guest_schedule[i]}")
        
"""
guest_availabilities = {
    0: [(9, 20)],
    1: [(9, 10)],
    2: [(10, 13)], 
    3: [(10, 13), (16, 17)], 
    4: [(13, 17)], 
    5: [(17, 19)],
    6: [(9, 10)]
}
    
get_schedule(guest_availabilities)
"""