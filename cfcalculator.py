from random import randint

#bet a set amount until fail
def flat_coinflip(start, weight, sample, *targets):

	result = []			
	for i in range(sample):			#mechanism
		bal = [start]
		temp_start = start
		while temp_start > 0:
			if randint(1, 2) == 1:
				temp_start += weight
			else:
				temp_start -= weight
			bal += [temp_start]
		result.append(bal)

	#stats
	average_max = sum(max(i) for i in result) / len(result)
	average_length = sum(len(i) for i in result) / len(result)
	
	if targets != None:
		hits = dict()
		for target in targets:
			number_of_hits = len([i for i in result if target in i])
			hits[str(target)] = number_of_hits

		success_rates = [i / sample for i in hits.values()]
		sr = dict(zip([str(i) for i in targets], success_rates))

	return f'-------Flat-------\nAverage Peak: {average_max} \nAverage Rounds: {average_length} \nNumber of times target hit: {hits} \nSuccess Rate: {sr}'

print(flat_coinflip(10, 1, 200, 20, 30, 40))


#bet a portion of current balance
def scaling_coinflip(start, scale, sample, *targets):
	result = []			
	for i in range(sample):			#mechanism
		bal = [start]
		temp_start = start
		while temp_start > 0.2:				#arbitrary stopping number
			weight = scale * temp_start
			if randint(1, 2) == 1:
				temp_start += weight
			else:
				temp_start -= weight
			bal += [temp_start]
		result.append(bal)
		return result

	#stats
	average_max = sum(max(i) for i in result) / len(result)
	average_length = sum(len(i) for i in result) / len(result)
	
	if targets != None:
		hits = dict()
		for target in targets:
			number_of_hits = len([i for i in result if target in i])
			hits[str(target)] = number_of_hits

		success_rates = [i / sample for i in hits.values()]
		sr = dict(zip([str(i) for i in targets], success_rates))

	return f'Average Peak: {average_max} \nAverage Rounds: {average_length} \nNumber of times target hit: {hits} \nSuccess Rate: {sr}'

# print(scaling_coinflip(6, 0.1, 1, 12, 15, 18))
#this model pretty much doesnt work as it hovers around the original number


#bet an increasing amount each loss. when win, set to base
def punishing_coinflip(start, base, increment, sample, *targets):

	result = []			
	for i in range(sample):			#mechanism
		bal = [start]
		temp_start = start
		while temp_start > 0:
			weight = base
			if randint(1, 2) == 1:
				temp_start += weight
				weight = base
			else:
				temp_start -= weight
				weight += increment
			bal += [temp_start]
		result.append(bal)

	#stats
	average_max = sum(max(i) for i in result) / len(result)
	average_length = sum(len(i) for i in result) / len(result)
	
	if targets != None:
		hits = dict()
		for target in targets:
			number_of_hits = len([i for i in result if target in i])
			hits[str(target)] = number_of_hits

		success_rates = [i / sample for i in hits.values()]
		sr = dict(zip([str(i) for i in targets], success_rates))

	return f'-------Punishing-------\nAverage Peak: {average_max} \nAverage Rounds: {average_length} \nNumber of times target hit: {hits} \nSuccess Rate: {sr}'

#print(punishing_coinflip(6, 1, 0.5, 200, 12, 15, 18))

#increases no matter what
def increasing_coinflip(start, base, increment, sample, *targets):

	result = []			
	for i in range(sample):			#mechanism
		bal = [start]
		temp_start = start
		while temp_start > 0:
			weight = base
			if randint(1, 2) == 1:
				temp_start += weight
			else:
				temp_start -= weight
			weight += increment
			bal += [temp_start]
		result.append(bal)

	#stats
	average_max = sum(max(i) for i in result) / len(result)
	average_length = sum(len(i) for i in result) / len(result)
	
	if targets != None:
		hits = dict()
		for target in targets:
			number_of_hits = len([i for i in result if target in i])
			hits[str(target)] = number_of_hits

		success_rates = [i / sample for i in hits.values()]
		sr = dict(zip([str(i) for i in targets], success_rates))

	return f'-------Increasing-------\nAverage Peak: {average_max} \nAverage Rounds: {average_length} \nNumber of times target hit: {hits} \nSuccess Rate: {sr}'

#print(increasing_coinflip(6, 1, 0.5, 200, 12, 15, 18))


#increases the lower success rate is
def adaptive_coinflip(start, base, karmaweight, sample, *targets):
	result = []			
	for i in range(sample):			#mechanism
		karma = 0
		bal = [start]
		temp_start = start
		weight = base
		while temp_start > 0:				#arbitrary stopping number
			weight = 1 + karma*karmaweight
			if randint(1, 2) == 1:
				temp_start += weight
				karma -= 1 #bad
			else:
				temp_start -= weight
				karma += 1 #good
			bal += [round(temp_start)]
		result.append(bal)

	#stats
	average_max = sum(max(i) for i in result) / len(result)
	average_length = sum(len(i) for i in result) / len(result)
	
	if targets != None:
		hits = dict()
		for target in targets:
			number_of_hits = len([i for i in result if target in i])
			hits[str(target)] = number_of_hits

		success_rates = [i / sample for i in hits.values()]
		sr = dict(zip([str(i) for i in targets], success_rates))

	return f'-------Adaptive-------\nAverage Peak: {average_max} \nAverage Rounds: {average_length} \nNumber of times target hit: {hits} \nSuccess Rate: {sr}'

print(adaptive_coinflip(10, 1, 1, 200, 20, 30, 40))
#IMPORTANT: in the thousands of simulations ran, this seems to have a consistently higher success rate than any other system.