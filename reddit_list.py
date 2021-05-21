
def main():
	reddit = open("top 100 subreddits.txt", "r")
	results = open("reddit_results.txt", "w")
	
	good_lines = []
	
	for line in reddit:
		line = line.split()
		mod_line = line[1].replace("/r/", "")
		good_lines.append(mod_line + "\n")
		
	results.writelines(good_lines)
		
		

if __name__ == "__main__":
	main()