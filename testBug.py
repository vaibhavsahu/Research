import arrow

timeNow = arrow.utcnow()
print timeNow
timePST = timeNow.to('US/Pacific')
timeMST = timeNow.to('US/Mountain')
    
