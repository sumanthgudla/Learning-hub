intervals = [[1,3],[2,6],[8,10],[15,18]]
intervals=sorted(intervals,key=lambda x:x[0])
merged_intervals=[]
for interval in intervals:
    if not merged_intervals or interval[0]>merged_intervals[-1][1]:
        merged_intervals.append(interval)
    else:
        merged_intervals[-1][1]=max(merged_intervals[-1][1],interval[1])
print(merged_intervals)
