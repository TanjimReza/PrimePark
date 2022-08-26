existing = ['11:00AM-1:00PM', '1:00PM-3:00PM', '3:00PM-5:00PM']
new = ['1:00PM-3:00PM']

# delete new from existing
for i in new:
    if i in existing:
        existing.remove(i)
print(existing)