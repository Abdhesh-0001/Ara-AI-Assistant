def count_votes(votes_list):
    """Count votes for each candidate"""
    vote_count = {}
    
    for vote in votes_list:
        if vote in vote_count:
            vote_count[vote] = vote_count[vote] + 1
        else:
            vote_count[vote] = 1
    
    return vote_count

# Test
votes = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Alice"]
result = count_votes(votes)
print(result)

# Now get the winner
winner = max(result, key=result.get)
print(f"Winner: {winner}")