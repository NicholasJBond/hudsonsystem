def calculate_score(rate1, rate2, winner, a, e):
	#0 is draw
	
	ratingdifference = float(rate1)-float(rate2)
	if winner == 0:
		player1_change_in_rating = -25*(1/(1+e**(-1*a*ratingdifference)))+12.5
		player2_change_in_rating = -25*(1/(1+e**(a*ratingdifference)))+12.5

	elif winner == 1:
		player1_change_in_rating = (5*(1/(1+e**(-1*a*ratingdifference)))-5)**2
		player2_change_in_rating = -1*(5*(1/(1+e**(a*ratingdifference))))**2
		
	elif winner == 2:
		player2_change_in_rating = (5*(1/(1+e**(a*ratingdifference)))-5)**2
		player1_change_in_rating = -1*(5*(1/(1+e**(-1*a*ratingdifference))))**2
	
	new_rating = [round(float(rate1)+float(player1_change_in_rating)), round(float(rate2)+float(player2_change_in_rating))]

	return new_rating


