intervals = [[1,3],[2,6],[8,10],[11,18]]
intervals=sorted(intervals,key=lambda x:x[0])
merged_intervals=[intervals[0]]
print(merged_intervals)
for interval in intervals:
    if merged_intervals[-1][1]>interval[0]:
        merged_intervals[-1][1]=interval[1]
    else:
        merged_intervals.append(interval)
print(merged_intervals)


